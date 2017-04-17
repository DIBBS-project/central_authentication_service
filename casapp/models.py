import base64
import json
import math
import os
import uuid

from django.conf import settings
from django.db import models


def deobfuscate(serialized_data):
    return json.loads(base64.b64decode(serialized_data.encode('utf-8')).decode('utf-8'))


def random_token(bits=256):
    bytes_ = int(math.ceil(bits // 8))
    rand_bytes = os.urandom(bytes_) # crypto-secure PRNG
    return base64.urlsafe_b64encode(rand_bytes)


class Credential(models.Model):
    """
    Credentials that DIBBs users have with cloud (e.g. OpenStack) service
    providers. Stored HACK in plaintext TODO with reversable encryption as we must be
    able to pull out the plaintext credentials to interact with the cloud
    service.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    site = models.CharField(max_length=2048)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='credentials', on_delete=models.CASCADE)
    credentials = models.TextField()

    @property
    def deobfuscated_credentials(self):
        """Reverse the base64-encoded JSON."""
        return deobfuscate(self.credentials)


class Token(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='token',
    )
    token = models.CharField(max_length=256, blank=False, default=random_token)
    created = models.DateTimeField(auto_now_add=True)
