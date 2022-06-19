from django.contrib.auth.backends import BaseBackend
from .models import User
from django.core.exceptions import ObjectDoesNotExist


class UserBackend(BaseBackend):
    def authenticate(self, request, **kwargs):
        email = kwargs.get('email')
        password = kwargs.get('password')
        try:
            user = User.objects.get(email__iexact=email)
            pass_validator = user.check_password(password)
            if pass_validator:
                return user
        except ObjectDoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except:
            return None
