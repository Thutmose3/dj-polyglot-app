from django.core.management.base import BaseCommand
from django.utils import timezone
from translation_api.models import SourceProject, TranslatableString

class Command(BaseCommand):
    """Management command to change the system_brand field of the SystemInfo model."""

    help = "Changes the system_brand field of the SystemInfo model."

    def handle(self, *args, **options):
        """Handle the command."""
        source_project = SourceProject.objects.get_or_create(
            name="Test Project",
        )[0]

        TranslatableString.objects.get_or_create(
            source_project=source_project,
            string="Hello, World!",
        )

