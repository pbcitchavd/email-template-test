from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required

from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from smtplib import SMTPRecipientsRefused
from django.core.mail import EmailMessage
from django.template import Context
from django.template.loader import get_template
from django.http import  HttpResponseRedirect, BadHeaderError

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

    users = User.objects.all()

    for user in users:
        test_email_template(request, user)



    return render(request, 'app_phishing/employees.html', context={
        "users": users
    })


def test_email_template(request, employee):

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
            'user_email': employee.user_email,
            'uid': urlsafe_base64_encode(force_bytes(employee.pk)),
            'token': generate_token.make_token(employee)
        })

        new_user = UserMailTemplate(username=employee, email_template=email_template)
        new_user.save()


def show_template_from_db(request,  employee_id):
        employee = User.objects.get(pk=employee_id)
        user = UserMailTemplate.objects.filter(username=employee)[0]

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

        return HttpResponseRedirect(reverse('employees'))


    return render(request,'app_phishing/get_password.html', context= {
        'user_email': email,
        'user_id': user_id
    })


def send_email_to_all(request):
    current_site = get_current_site(request)
    if request.method == 'POST':
        current_site = get_current_site(request)
        # send_to_email = ['asan.chavdarliev@pbconsult.de']

        email_subject = "Einführung der neuen E-Mail-Vorlage für interne Anfragen"

        #todo: get  asan
        # users = User.objects.filter(username='CHAVD')

        users = User.objects.all()

        for user in users:

            message = get_template("app_phishing/email_template.html").render({
                # todo: user
                # 'toEmail': user.email,
                # todo user pbc user_email
                'toEmail': user.user_email,
                'domain': current_site,
                'user': user,
                'user_email': user.user_email,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': generate_token.make_token(user)
            })

            try:
                mail = EmailMessage(
                    subject=email_subject,
                    body=message,
                    from_email="Thomas Kahn | Geschäftsführug | PB Consult GmbH <thomas.kahn@pbconsult.info>" ,# "thomas.kahn@pbconsult.de",
                    # bcc=[],# "thomas.kahn@pbconsult.de",
                    # todo: user
                    #to=[user.email],
                    # todo: pbc user
                    to=[user.user_email],
                    reply_to=["thomas.kahn@pbconsult.de"],

                    headers={'From': 'Thomas Kahn | Geschäftsführug | PB Consult GmbH | Teams <thomas.kahn@pbconsult.info>'},
                )
                mail.content_subtype = "html"
                # mail.send()
            except BadHeaderError:
                messages.error(request, f"Die Nachricht an {user.username} konnte nicht gesendet werden. Bitte versuche es noch einmal.")
                return HttpResponse('Invalid header found.')

            except SMTPRecipientsRefused:
                messages.error(request, f"Die Nachricht an {user.username} konnte nicht gesendet werden. Bitte versuche es noch einmal.")
                return HttpResponse('Invalid header found.')

            messages.success(request,
                             f"Die Nachricht an {user.username} wurde versendet.")
        return HttpResponseRedirect(reverse('employees'))
    else:
        messages.error(request, "Sie haben nicht alle Pflichtfelder(*) ausgefüllt. Bitte überprüfen Sie Ihre Angaben.")

        return render(request, 'app_phishing/email_template.html', context={
            'toEmail': get_user_model().objects.first().email,
            'domain': current_site,
            'user': get_user_model().objects.first(),
            'uid': urlsafe_base64_encode(force_bytes(get_user_model().objects.first().pk)),
            'token': generate_token.make_token(get_user_model().objects.first())

        })


def send_email_to_user(request, employee_id):
    if request.method == "POST":
        current_site = get_current_site(request)
        user = User.objects.get(pk=employee_id)
        if user:
            user_template = UserMailTemplate.objects.filter(username=user).first()
            email_subject = "Einführung der neuen E-Mail-Vorlage für interne Anfragen"
            message = user_template.email_template

            user_template.is_active = True
            user_template.save()

            # todo: einkommentieren
            try:
                mail = EmailMessage(
                    subject=email_subject,
                    body=message,
                    from_email="Thomas Kahn | Geschäftsführug | PB Consult GmbH <thomas.kahn@pbconsult.info>",
                    # "thomas.kahn@pbconsult.de",
                    # bcc=[],# "thomas.kahn@pbconsult.de",
                    # todo: user
                    # to=[user.email],
                    # todo: pbc user
                    to=[user.user_email],
                    reply_to=["thomas.kahn@pbconsult.de"],

                    headers={
                        'From': 'Thomas Kahn | Geschäftsführug | PB Consult GmbH | Teams <thomas.kahn@  pbconsult.info>'},
                )
                mail.content_subtype = "html"
                # mail.send()

            except BadHeaderError:
                messages.error(request, f"Die Nachricht an {user.username} konnte nicht gesendet werden. Bitte versuche es noch einmal.")

                return HttpResponse('Invalid header found.')

            except SMTPRecipientsRefused:
                messages.error(request, f"Die Nachricht an {user.username} konnte nicht gesendet werden. Bitte versuche es noch einmal.")
                return HttpResponse('Invalid header found.')

            messages.success(request, f"Die Nachricht an {user.username} wurde versendet.")

        return HttpResponseRedirect(reverse('employees'))

    return HttpResponseRedirect(reverse('employees'))


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
        user.save()

        # send mail Email verified, you can now login
                                                # TODO: Spaeter pbc mitarbeiter user_email
                                                # todo: django user have email
        return redirect(reverse('get_pwd', args=(user.user_email, user.id, )))

    return HttpResponse('Activation link is invalid!')