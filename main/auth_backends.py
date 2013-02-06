# ~*~ encoding: utf-8 ~*~

from main.models import User
from django.core.validators import email_re

class UserBasicBackend:
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class UserEmailBackend(UserBasicBackend):
    def authenticate(self, email=None, password=None):
        #If username is an email address, then try to pull it up
        user = None
        if email_re.search(email):
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return None
        if user and user.check_password(password):
            return user
        return None


class VerificationCodeBackend(UserBasicBackend):
    def authenticate(self, code=None):
        try:
            profile = Profile.objects.get(verification_code=code)
        except Profile.DoesNotExist:
            return None
        return profile.user

