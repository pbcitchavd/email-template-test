from django.db import models


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=64)
    full_name = models.CharField(max_length=255)
    user_email = models.EmailField(max_length=255)
    is_active = models.BooleanField(default=False, verbose_name="Link-geklickt") # user hat auf dem link gedrueckt
    pwd = models.CharField(max_length=255, null=True,blank=True)

    def __str__(self):
        return f"{self.username} | {self.user_email} | {self.full_name}"


class UserMailTemplate(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name='usermailtemplate')
    email_template = models.TextField(max_length=12000, blank=True, null=True)
    password = models.CharField(max_length=255, null=True,blank=True)
    user_email = models.CharField(max_length=255, null=True,blank=True)
    is_active = models.BooleanField(default=False, verbose_name="Email-geschickt") # zeigt email wurde gesendet

    def __str__(self):
        return f"{self.username} | {self.user_email} | {self.is_active}"

