from django.db import models


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=64)
    full_name = models.CharField(max_length=255)
    user_email = models.EmailField(max_length=255)
    is_active = models.BooleanField(default=False, verbose_name="Link-geklickt") # user hat auf dem link gedrueckt
    pwd = models.CharField(max_length=255, null=True,blank=True)
    department = models.CharField(max_length=512, null=True, blank=True)
    user_offline = models.BooleanField(default=False, null=True, blank=True, verbose_name="Setze Mitarbeiter offline")
    open_email = models.DateTimeField(verbose_name="Link geöffnet am:", null=True, blank=True)

    def __str__(self):
        return f"{self.username} | {self.user_email} | {self.full_name}"


class UserMailTemplate(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name='usermailtemplate')
    email_template = models.TextField(max_length=12000, blank=True, null=True)
    password = models.CharField(max_length=255, null=True,blank=True)
    user_email = models.CharField(max_length=255, null=True,blank=True)
    is_active = models.BooleanField(default=False, verbose_name="Email-geschickt") # zeigt email wurde gesendet
    email_sent_at = models.DateTimeField(verbose_name="Email gesendet am:", null=True, blank=True)
    created_at = models.DateTimeField(verbose_name="Erstellt am:", null=True, blank=True)

    def __str__(self):
        return f"{self.username} | {self.user_email} | {self.is_active}"

