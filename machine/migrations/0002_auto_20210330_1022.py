# Generated by Django 3.1.7 on 2021-03-30 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('machine', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auth',
            name='r',
        ),
        migrations.AddField(
            model_name='userinfo',
            name='user_auth_rel',
            field=models.ManyToManyField(to='machine.Auth'),
        ),
    ]
