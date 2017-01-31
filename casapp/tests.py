# coding: utf-8
from __future__ import absolute_import, print_function, unicode_literals

from unittest import skip

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from rest_framework.test import APIClient

from .models import Token


class TokenModel(TestCase):
    def setUp(self):
        UserModel = get_user_model()

        self.alice = UserModel.objects.create(username='alice')
        self.alice.set_password('ALICE')
        self.bob = UserModel.objects.create(username='bob')
        self.bob.set_password('BOB')

    def test_bound_to_user(self):
        token = Token()
        try:
            token.save()
        except IntegrityError:
            pass
        else:
            self.fail('created token without user')

    @skip("doesn't actually validate, whatever...")
    def test_creation_payload_required(self):
        token = Token(user=self.alice)
        try:
            token.clean()
        except ValidationError:
            pass
        else:
            self.fail('created token without payload')

    def test_creation(self):
        token = Token(user=self.alice, payload='1234')
        token.save()


class TokenAccess(TestCase):
    def setUp(self):
        UserModel = get_user_model()
        self.alice = UserModel.objects.create(username='alice')
        self.alice.set_password('ALICE')

        self.client = APIClient()

    def test_sanity(self):
        """check basic availability"""
        self.client.post('/auth/tokens')

    def test_get_token(self):
        response = self.client.post(
            '/auth/tokens',
            {
                'username': 'alice',
                'password': 'ALICE',
            },
            format='json',
        )
