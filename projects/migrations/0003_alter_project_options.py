# Generated by Django 3.2.9 on 2022-04-28 21:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_auto_20220428_2106'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'permissions': [('can_create_a_project', 'As a user I can create an project'), ('can_read_all_the_project', 'As a user I can read all the project'), ('can_update_project', 'As a user I can update a project'), ('can_delete_project', 'As a user I can delete a project')]},
        ),
    ]