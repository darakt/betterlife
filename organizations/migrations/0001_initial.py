# Generated by Django 3.2.9 on 2022-04-28 10:29

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=280)),
                ('description', models.CharField(max_length=400)),
                ('language', models.CharField(choices=[('aa', 'Afar'), ('ab', 'Abkhazian'), ('af', 'Afrikaans'), ('ak', 'Akan'), ('sq', 'Albanian'), ('am', 'Amharic'), ('ar', 'Arabic')], default='aa', max_length=2)),
                ('admins', models.ManyToManyField(related_name='administrated_by', to=settings.AUTH_USER_MODEL)),
                ('members', models.ManyToManyField(related_name='member_of_organization', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
