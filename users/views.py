from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from .serializers import UserRegisterSerializer, UserUpdateSerializer
from rest_framework import viewsets
from .permissions import IsAdmin, IsOwner
from tokenauth.utils import logout_user
from .models import Passenger, BaseUser


class SelfUserViewSet(RetrieveAPIView):
    queryset = BaseUser.objects.all()
    serializer_class = UserRegisterSerializer

    def get_object(self):
        return BaseUser.objects.get(pk=self.request.user.id)


class UserViewSet(viewsets.ModelViewSet):
    queryset = Passenger.objects.all()
    permission_classes = [IsAdmin | IsOwner, ]
    serializer_class = UserUpdateSerializer

    def update(self, request, *args, **kwargs):
        serializer = UserUpdateSerializer(instance=self.get_object(), data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, self_user=False):
        if self_user:
            logout_user(request)

        return super().destroy(request, pk)


class UserRegister(CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
