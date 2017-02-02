# coding: utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import base64
import math
import os

from django.conf import settings
from django.db import models


def random_token(bits=256):
    bytes_ = int(math.ceil(bits // 8))
    rand_bytes = os.urandom(bytes_) # crypto-secure PRNG
    return base64.urlsafe_b64encode(rand_bytes)


class Token(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='token',
    )
    token = models.CharField(max_length=256, blank=False, default=random_token)
    created = models.DateTimeField(auto_now_add=True)
