from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework.exceptions import AuthenticationFailed


class CustomJWTAuthentication(JWTAuthentication):

    def authenticate(self, request):
        try:
            return super().authenticate(request)
        except InvalidToken as e:
            # Catch token error and use custom error message
            raise AuthenticationFailed("The token has expired or is invalid. Please login again.")