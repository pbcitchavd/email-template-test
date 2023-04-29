import csv
import os
import sys
import csv
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core_phishing.settings")
django.setup()

from app_phishing.models import User


def main():
    with open("src/beUser.csv", encoding="ISO-8859-1") as file:
        rows = csv.DictReader(file)

        for row in rows:
            username = row['strUser'].strip()
            full_name = row['strNameDisplay'].strip()
            if row['strMail']:
                user_email = row['strMail'].strip()
            else:
                user_email = row['strMail']

            user = User(username=username, full_name=full_name, user_email=user_email)
            user.save()
            print(user)

if __name__ == '__main__':


    main()

