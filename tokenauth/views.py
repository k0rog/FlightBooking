from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CustomAuthTokenSerializer
from .utils import logout_user


class LoginView(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        response = Response({
            'user_id': user.pk,
            'email': user.email
        })

        response.set_cookie(key='token', value=token.key)

        return response


class LogoutView(APIView):
    def post(self, request):
        response = logout_user(request)

        return response
