# Generated by Django 4.0 on 2023-04-29 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_phishing', '0007_user_user_offline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_offline',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Setze Mitarbeiter offline'),
        ),
    ]
