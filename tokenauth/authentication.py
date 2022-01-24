from rest_framework.authentication import TokenAuthentication, get_authorization_header
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions


class CustomTokenAuthentication(TokenAuthentication):
    def validate_header(self, header):
        header = header.split()

        if len(header) == 1:
            msg = _('Invalid token header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(header) > 2:
            msg = _('Invalid token header. Token string should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        keyword, token = header

        if keyword.lower() != self.keyword.lower().encode():
            return None

        try:
            token = token.decode()
        except UnicodeError:
            msg = _('Invalid token header. Token string should not contain invalid characters.')
            raise exceptions.AuthenticationFailed(msg)

        return token

    def authenticate(self, request):
        header = get_authorization_header(request)

        if header:
            token = self.validate_header(header)
        else:
            token = request.COOKIES.get('token', None)

            if not token:
                return None

        try:
            return self.authenticate_credentials(token)
        except exceptions.AuthenticationFailed:
            return None
