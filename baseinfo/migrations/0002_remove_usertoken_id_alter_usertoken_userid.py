# Generated by Django 4.0.3 on 2022-03-18 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baseinfo', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usertoken',
            name='id',
        ),
        migrations.AlterField(
            model_name='usertoken',
            name='userid',
            field=models.CharField(max_length=30, primary_key=True, serialize=False, verbose_name='用户登录账号'),
        ),
    ]
