import logging
import json

from django.conf import settings
from django.utils import timezone
from rest_framework.exceptions import MethodNotAllowed, NotFound, \
    ValidationError
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

    # @list_route(['get'])
    # def my(self, request):
    #     serializer = BookingListSerializer(
    #         Booking.objects.my_frontend(request.user).exclude(status=Booking.DELETED).order_by('-created_at'),
    #         many=True,
    #         context={'request': self.request}
    #     )
    #     return Response(serializer.data)

    # @list_route(['post'])
    # def my_set_viewed(self, request):
    #     Booking.objects.my_not_viewed(request.user).update(viewed=True)
    #     return Response({'not_viewed_count': 0})
