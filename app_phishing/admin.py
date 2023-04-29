from django.contrib import admin
from .models import User, UserMailTemplate


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "full_name", "user_email", "is_active", "department", "user_offline", "open_email", "id")
    ordering = ["username"]


class UserMailTemplateAdmin(admin.ModelAdmin):
    list_display = ("username", "password", "user_email", "is_active", "email_sent_at", "created_at", )
    ordering = ["username"]

admin.site.register(User, UserAdmin)
admin.site.register(UserMailTemplate, UserMailTemplateAdmin)
