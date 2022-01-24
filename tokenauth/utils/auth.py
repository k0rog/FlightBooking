from rest_framework import status
from rest_framework.response import Response


def logout_user(request):
    request.user.auth_token.delete()

    response = Response(data={'message': 'success'}, status=status.HTTP_200_OK)
    response.delete_cookie('token')

    return response
