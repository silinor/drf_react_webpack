import logging
from decimal import *

from rest_framework.decorators import list_route, detail_route
from rest_framework.viewsets import mixins
from rest_framework.response import Response
from rest_framework import viewsets, status

from django.contrib.auth.models import User
from .models import Profile
from .serializers import UserSerializer

logger = logging.getLogger(__name__)


class UserViewSet(mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):

    serializer_class = UserSerializer
    queryset = User.objects.all()

    @list_route(['post'])
    def money_transfer(self, request):
        try:
            user = User.objects.get(pk=request.data['usersSelect'])
        except User.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'user does not exist'})
        if user.profile.balance < Decimal(request.data['amount']):
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'not enough funds on user balance'})
        # check inn input
        inn_request_list = [x.strip() for x in request.data['inn'].split(sep=',')]
        inn_profiles = Profile.objects.filter(inn__in=inn_request_list).exclude(user=user)
        inn_db_list = [profile.inn for profile in inn_profiles]
        if not all(x in inn_db_list for x in inn_request_list):
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'wrong INN'})
        user.profile.balance -= Decimal(request.data['amount'])
        user.save()
        total_amount = Decimal(request.data['amount'])
        amount = round(Decimal(request.data['amount']) / len(inn_db_list), 2)
        for inn_profile in inn_profiles:
            if total_amount < amount:
                # transfer remainder, to avoid funds overruns
                amount = total_amount
            inn_profile.balance += amount
            inn_profile.save()
            total_amount -= amount
        return Response({'success'})
