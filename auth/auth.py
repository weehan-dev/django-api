from django.contrib.auth import get_user_model


UserModel = get_user_model()

class UserBackend(object):
    def authenticate(self, username=None, password=None):
        try:
            user = UserModel.objects.get(username=username)
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

        except UserModel.DoesNotExist:
            return None

    @staticmethod
    def user_can_authenticate(self, user):
        is_active = getattr(user, 'is_active', None)
        return is_active or is_active is None

    @staticmethod
    def get_user(self, user_id):
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
