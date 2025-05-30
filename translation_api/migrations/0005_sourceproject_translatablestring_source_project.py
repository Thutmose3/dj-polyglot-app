# Generated by Django 5.0.7 on 2024-08-04 08:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("translation_api", "0004_translatablestring_string_fr_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="SourceProject",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=500, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name="translatablestring",
            name="source_project",
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to="translation_api.sourceproject"
            ),
        ),
    ]
