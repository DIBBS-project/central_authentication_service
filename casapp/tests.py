# coding: utf-8
from __future__ import absolute_import, print_function, unicode_literals

import json
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
        self.alice.save()
        self.bob = UserModel.objects.create(username='bob')
        self.bob.set_password('BOB')
        self.bob.save()

    def test_bound_to_user(self):
        token = Token()
        try:
            token.save()
        except IntegrityError:
            pass
        else:
            self.fail('created token without user')

    def test_creation(self):
        token = Token(user=self.alice, token='1234')
        token.save()


class TokenAccess(TestCase):
    def setUp(self):
        UserModel = get_user_model()
        self.alice = UserModel.objects.create(username='alice')
        self.alice.set_password('ALICE')
        self.alice.save()

        self.client = APIClient()

    def test_sanity(self):
        """check basic availability"""
        self.client.get('/auth/tokens')

    def test_get_token(self):
        response = self.client.post(
            '/auth/tokens',
            {
                'username': 'alice',
                'password': 'ALICE',
            },
            format='json',
        )
        assert response.status_code == 200
        data = json.loads(response.content)
        assert 'token' in data

    def test_invalid_user(self):
        response = self.client.post(
            '/auth/tokens',
            {
                'username': 'eve',
                'password': 'EVE',
            },
            format='json',
        )
        assert response.status_code == 403

    def test_garbage(self):
        response = self.client.post(
            '/auth/tokens',
            [2, 3, 4, {
                'heqr': 'fwe',
                'fqe': 'fwefqwe',
            }],
            format='json',
        )


class TokenVerify(TestCase):
    def setUp(self):
        UserModel = get_user_model()
        self.alice = UserModel.objects.create(username='alice')
        self.alice.set_password('ALICE')
        self.alice.save()

        token = Token.objects.create(user=self.alice)
        self.token_string = token.token

        self.client = APIClient()

    def test_verify_token(self):
        response = self.client.get(
            '/auth/tokens',
            HTTP_DIBBS_AUTHORIZATION=self.token_string,
        )
        assert response.status_code == 200
        data = json.loads(response.content)
        assert 'username' in data
        assert data['username'] == self.alice.username

    def test_reject_token(self):
        response = self.client.get(
            '/auth/tokens',
            HTTP_DIBBS_AUTHORIZATION=reversed(self.token_string),
        )
        assert response.status_code == 403
