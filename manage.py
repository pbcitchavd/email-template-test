#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import dotenv
import pathlib
# from core_phishing.settings import base


def main():
    """Run administrative tasks."""

    # todo: Dev Local Testing
    # DOT_ENV_PATH = pathlib.Path() / '.env.dev'
    # if DOT_ENV_PATH.exists():
    #    env_test = dotenv.load_dotenv(dotenv_path=DOT_ENV_PATH)

    # if base.DEBUG:
    #     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core_phishing.settings.dev')
    #     print("DEV LOCAL")
    # else:
    #     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core_phishing.settings.prod')
    #     print("PRODUCTION")

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core_phishing.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
