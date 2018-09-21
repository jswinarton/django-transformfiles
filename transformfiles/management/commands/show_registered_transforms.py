import textwrap

from django.core.management.base import BaseCommand
from transformfiles.transforms import get_registry


class Command(BaseCommand):
    help = ""

    def handle(self, **options):
        registry = get_registry()
        message = "Available transforms:\n\n"

        for key, value in registry.items():
            message += "{}\n".format(key)

        self.stdout.write(message)
