from django.contrib import admin
from .models import User, UserMailTemplate
# Register your models here.
admin.site.register(User)
admin.site.register(UserMailTemplate)