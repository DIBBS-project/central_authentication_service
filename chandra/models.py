import base64
import math
import os

from django.conf import settings
from django.db import models


def random_token(bits=256):
    bytes_ = int(math.ceil(bits // 8))
    rand_bytes = os.urandom(bytes_) # CSPRNG
    return base64.urlsafe_b64encode(rand_bytes)


class SiteCredentials(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='token',
    )
    site = models.CharField(max_length=256)
    created = models.DateTimeField(auto_now_add=True)
    credentials = models.TextField()


class Token(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='token',
    )
    token = models.CharField(max_length=256, blank=False, default=random_token)
    created = models.DateTimeField(auto_now_add=True)
