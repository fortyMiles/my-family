#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    setting_url = 'maili.settings'
    if 'test' in sys.argv:
        setting_url =  "test.settings"

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", setting_url)

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
