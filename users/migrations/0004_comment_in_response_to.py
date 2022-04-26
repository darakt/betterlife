# Generated by Django 3.2.9 on 2022-04-25 14:57

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_comment_written_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='in_response_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=models.SET(users.models.get_deleted_comment), to='users.comment'),
        ),
    ]
