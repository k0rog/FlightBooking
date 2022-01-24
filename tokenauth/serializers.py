from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(
        label=_('Email'),
        write_only=True
    )

    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = get_user_model().objects.filter(email=email).first()

        if not user:
            raise serializers.ValidationError(_('Provided email not found'), code='authorization')

        if not user.check_password(password):
            raise serializers.ValidationError(_('Wrong password'), code='authorization')

        attrs['user'] = user

        return attrs
