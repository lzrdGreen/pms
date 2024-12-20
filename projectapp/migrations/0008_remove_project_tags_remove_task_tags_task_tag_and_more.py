# Generated by Django 5.1 on 2024-10-19 22:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("projectapp", "0007_tag_project_tags_task_tags"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="project",
            name="tags",
        ),
        migrations.RemoveField(
            model_name="task",
            name="tags",
        ),
        migrations.AddField(
            model_name="task",
            name="tag",
            field=models.CharField(blank=True, max_length=127, null=True),
        ),
        migrations.AddField(
            model_name="project",
            name="tags",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name="Tag",
        ),
    ]
