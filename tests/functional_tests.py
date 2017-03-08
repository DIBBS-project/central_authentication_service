#!/usr/bin/env python
"""
Test the Django service
"""
# import argparse
# import contextlib
# import errno
import pathlib
# import socket
# import subprocess
import sys
# import threading
# import time

import requests

from common_dibbs.names import AUTHORIZATION_HEADER

# from sham_cas import app as sham_cas
# from helpers import DjangoRunserverManager, FlaskAppManager

TEST_DIR = pathlib.Path(__file__).resolve().parent
BASE_DIR = TEST_DIR.parent
MANAGE_PY = BASE_DIR / 'manage.py'


def assertStatus(response, expected, message=None):
    try:
        start, stop = expected
    except TypeError:
        if response.status_code == expected:
            return
    else:
        if start <= response.status_code < stop:
            return
        expected = '[{}, {})'.format(start, stop)

    if message:
        print(message, file=sys.stderr)

    print('Received status {}, expected {}\n-------------\n{}'
        .format(response.status_code, expected, response.content),
        file=sys.stderr)

    raise AssertionError(message or "bad status code")


def test():
    ROOT = 'http://localhost:7000'
    TOKEN_ENDPOINT = ROOT + '/auth/tokens'

    DA_HEADER = 'Dibbs-Authorization'

    # sanity check
    requests.get(ROOT)

    response = requests.post(TOKEN_ENDPOINT, json={
        'username': 'alice',
        'password': 'incorrect',
    })
    assertStatus(response, 403)

    response = requests.post(TOKEN_ENDPOINT, json={
        'username': 'alice',
        'password': 'ALICE',
    })
    assertStatus(response, 200)

    token = response.json()['token']

    response = requests.get(TOKEN_ENDPOINT, headers={
        DA_HEADER: token,
    })
    assertStatus(response, 200)

    response = requests.get(TOKEN_ENDPOINT, headers={
        DA_HEADER: token[::-1],
    })
    assertStatus(response, 403)


def main(argv=None):
    # if argv is None:
    #     argv = sys.argv
    #
    # parser = argparse.ArgumentParser(description=__doc__)
    #
    # parser.add_argument('-v', '--verbose', action='store_true')
    #
    # args = parser.parse_args(argv[1:])

    result = test()

    return result

if __name__ == '__main__':
    sys.exit(main(sys.argv))
