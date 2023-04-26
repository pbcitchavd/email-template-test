from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six


class TokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        print(f"user {user}")
        print(f"timestamp {timestamp}")
        return (six.text_type(user.pk) + six.text_type(timestamp)) + six.text_type(user)


generate_token = TokenGenerator()


def send_mail():
    print('email-gesendet ')