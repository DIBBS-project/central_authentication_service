#!/usr/bin/env python
"""
Test the Django service
"""
import pathlib
import sys

import requests


TEST_DIR = pathlib.Path(__file__).resolve().parent
BASE_DIR = TEST_DIR.parent
MANAGE_PY = BASE_DIR / 'manage.py'


ROOT = 'http://localhost:7000'
DA_HEADER = 'Dibbs-Authorization'

TOKEN_ENDPOINT = ROOT + '/auth/tokens'
SITE_CREDS_ENDPOINT = ROOT + '/credentials'

VALID_TOKEN_HEADER = None


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
    # sanity check
    requests.get(ROOT)

    test_tokens()
    test_site_creds()


def test_tokens():
    global TOKEN_HEADER

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
    VALID_TOKEN_HEADER = {DA_HEADER: token}

    response = requests.get(TOKEN_ENDPOINT, headers={
        DA_HEADER: token,
    })
    assertStatus(response, 200)

    response = requests.get(TOKEN_ENDPOINT, headers={
        DA_HEADER: token[::-1], # mangled header
    })
    assertStatus(response, 403)


def test_site_creds():
    response = requests.get(SITE_CREDS_ENDPOINT, headers=VALID_TOKEN_HEADER)
    assertStatus(response, 200)




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
