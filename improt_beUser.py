import csv
import os
import sys
import csv
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core_phishing.settings")
django.setup()

from app_phishing.models import User


def main():

    # with open("src/beUser.csv", encoding="ISO-8859-1") as file:
    # with open("src/PBC_Users-latest.csv", encoding="utf-8-sig") as file:
    with open("src/PBC_Users-latest.csv", encoding="utf-8-sig") as file:
        rows = csv.DictReader(file, delimiter=";")

        for row in rows:
            username = row['strUser'].strip()
            full_name = row['strNameDisplay'].strip()
            if row['strMail']:
                user_email = row['strMail'].strip().lower()
            else:
                user_email = row['strMail']

            department = row['Department']

            user = User(username=username, full_name=full_name, user_email=user_email, department=department)
            user.save()
            print(user)


if __name__ == '__main__':
    main()

