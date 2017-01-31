# coding: utf-8
from __future__ import absolute_import, print_function, unicode_literals

from django.conf import settings
from django.db import models


class Token(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='token',
    )
    payload = models.CharField(max_length=50, blank=False)
    created = models.DateTimeField(auto_now_add=True)
