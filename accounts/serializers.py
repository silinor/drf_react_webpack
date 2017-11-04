import datetime

from decimal import Decimal

from rest_framework import serializers

from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.utils import timezone

from django.contrib.auth.models import User
from .models import Profile


class UserSerializer(serializers.ModelSerializer):
    inn = serializers.CharField(source='profile.inn')
    balance = serializers.DecimalField(source='profile.balance', max_digits=9, decimal_places=2)

    class Meta:
        model = User
        read_only_fields = (
            'id',
            'username',
            'inn',
            'balance',
        )
        fields = read_only_fields
