from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        response = (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_email_confirmed)
        )
        return response

account_activation_token = AccountActivationTokenGenerator()

