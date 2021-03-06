# Generated by Django 3.2.9 on 2022-04-28 22:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0002_alter_organization_options'),
        ('projects', '0003_alter_project_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='organization',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='organizations.organization'),
        ),
    ]
