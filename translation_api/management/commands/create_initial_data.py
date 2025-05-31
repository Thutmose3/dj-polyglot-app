from django.core.management.base import BaseCommand

from translation_api.models import SourceProject
from translation_api.models import TranslatableString


class Command(BaseCommand):

    help = "Changes the system_brand field of the SystemInfo model."

    def handle(self, *args, **options):
        source_project = SourceProject.objects.get_or_create(
            name="Test Project",
        )[0]

        TranslatableString.objects.get_or_create(
            source_project=source_project,
            string="Hello, World!",
        )
