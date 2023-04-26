# Generated by Django 4.0 on 2023-04-11 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=64)),
                ('full_name', models.CharField(max_length=255)),
                ('user_email', models.EmailField(max_length=255)),
            ],
        ),
    ]
