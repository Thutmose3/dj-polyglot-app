# Generated by Django 5.0.7 on 2025-05-24 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('translation_api', '0018_sourceproject_admins_alter_sourceproject_users'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='translatablestring',
            unique_together=set(),
        ),
        migrations.AddConstraint(
            model_name='translatablestring',
            constraint=models.UniqueConstraint(fields=('source_project', 'string', 'context'), name='unique_translation_key'),
        ),
    ]
