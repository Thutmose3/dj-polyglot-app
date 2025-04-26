#!/usr/bin/env python
import os
import sys

from decouple import config
from django.core.management import execute_from_command_line

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", config("DJANGO_SETTINGS_MODULE", "settings.settings.production"))

    execute_from_command_line(sys.argv)
