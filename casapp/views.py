# coding: utf-8
from __future__ import absolute_import, print_function, unicode_literals

import json
import logging
import uuid

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Token
from .serializers import TokenSerializer

logger = logging.getLogger(__name__)


class TokenViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions
    """
    queryset = Token.objects.all()
    serializer_class = TokenSerializer
