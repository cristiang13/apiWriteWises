from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import User

class CustomTokenAuthentication(BaseAuthentication):

    def authenticate(self, request):
        token = request.META.get("HTTP_AUTHORIZATION")
        if not token:
            return None

        try:
            user = User.get_by_id(token)
            if user is None:
                raise AuthenticationFailed("Usuario no encontrado")
        except Exception as e:
            raise AuthenticationFailed(str(e))

        return (user, token)
