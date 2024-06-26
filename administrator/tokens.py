from django.contrib.auth.tokens import PasswordResetTokenGenerator
import uuid

class generate_token(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            str(uuid.uuid4().hex) + str(user.pk) + str(timestamp)
        )


account_activation_token = generate_token()