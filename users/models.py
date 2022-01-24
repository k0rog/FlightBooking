from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.utils import timezone


class BaseUser(AbstractUser):
    date_updated = models.DateTimeField(default=timezone.now)
    username = None
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        self.date_updated = timezone.now()
        super().save(*args, **kwargs)


class Passenger(BaseUser):
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        student_group = Group.objects.get(name='passenger')
        self.groups.add(student_group)


class Admin(BaseUser):
    def save(self, *args, **kwargs):
        self.is_staff = True
        self.is_superuser = True
        super().save(*args, **kwargs)
        student_group = Group.objects.get(name='admin')
        self.groups.add(student_group)
