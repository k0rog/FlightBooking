from users.utils import create_passenger, get_token, create_admin
from django.contrib.auth.models import Group


class TestAuthenticatePassengerMixin:
    def setUp(self):
        Group.objects.get_or_create(name='admin')
        Group.objects.get_or_create(name='passenger')
        self.user = create_passenger()
        self.token = get_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)


class TestAuthenticateAdminMixin(TestAuthenticatePassengerMixin):
    def setUp(self):
        super().setUp()
        self.user = create_admin()
        self.token = get_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
