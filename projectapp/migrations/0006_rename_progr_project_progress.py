# Generated by Django 5.1 on 2024-10-17 09:31

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("projectapp", "0005_project_progr"),
    ]

    operations = [
        migrations.RenameField(
            model_name="project",
            old_name="progr",
            new_name="progress",
        ),
    ]
