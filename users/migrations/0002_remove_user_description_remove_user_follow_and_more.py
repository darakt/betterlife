# Generated by Django 4.0.4 on 2022-04-25 14:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='description',
        ),
        migrations.RemoveField(
            model_name='user',
            name='follow',
        ),
        migrations.RemoveField(
            model_name='user',
            name='followers_count',
        ),
        migrations.RemoveField(
            model_name='user',
            name='profil_img_url',
        ),
    ]
