from rest_framework.authtoken.models import Token
from users.models import Admin
from users.serializers import UserRegisterSerializer


PASSENGER_DATA = {
                'first_name': "Ilya",
                'last_name': 'Auramenka',
                'email': 'c@c.com',
                'password': 'c'
            }


def create_passenger():
    serializer = UserRegisterSerializer(data=PASSENGER_DATA)

    if serializer.is_valid():
        return serializer.save()


def create_admin():
    return Admin.objects.create(email='admin@admin.com', password='admin')


def get_token(user):
    token, created = Token.objects.get_or_create(user=user)
    return token
