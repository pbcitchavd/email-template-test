# Generated by Django 4.0 on 2023-04-29 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_phishing', '0006_user_department_user_open_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_offline',
            field=models.BooleanField(blank=True, null=True, verbose_name='Setze Mitarbeiter offline'),
        ),
    ]
