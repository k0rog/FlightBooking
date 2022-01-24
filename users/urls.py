from django.urls import path
from . import views


urlpatterns = [
    path('register', views.UserRegister.as_view(), name='registration'),
    path('<int:pk>/', views.UserViewSet.as_view({'patch': 'update', 'delete': 'destroy', 'get': 'retrieve'}),
         name='user_exact'),
    path('me/', views.SelfUserViewSet.as_view()),
]
