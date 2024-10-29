# Generated by Django 5.1 on 2024-10-19 15:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("projectapp", "0006_rename_progr_project_progress"),
    ]

    operations = [
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=63, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name="project",
            name="tags",
            field=models.ManyToManyField(
                blank=True, related_name="projects", to="projectapp.tag"
            ),
        ),
        migrations.AddField(
            model_name="task",
            name="tags",
            field=models.ManyToManyField(
                blank=True, related_name="tasks", to="projectapp.tag"
            ),
        ),
    ]