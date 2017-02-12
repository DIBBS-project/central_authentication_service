# Central Authentication Service

## Implementation

~~The implementation is based on the [**django-allauth**](https://github.com/pennersr/django-allauth) plugin, which provides advanced authentication mechanisms that can be used in Django.~~

## Authentication Flow

> *See [docs/README.md](docs/README.md)* for some message sequence diagrams

DIBBs services require a token that must be obtained from the CAS. The client is responsible for storing and relaying this token to the services they wish to interact with.

### Getting the Token

The user `POST`s a JSON object containing their `username` and `password` as keys to `/auth/tokens`. The server replies with a JSON object containing a key named `token` with a string value.

### Using the Token

Requests to other DIBBs services must be made by placing that string as the value of an HTTP header named `Dibbs-Authorization`.

### Validating the Token

`GET` against `/auth/tokens` with the token string in the aforementioned HTTP header.

## Integrating the CAS with DIBBs services

Add the [CASUserBridgeMiddleware](https://github.com/DIBBS-project/common-dibbs/blob/master/common_dibbs/django.py) from the [common_dibbs](https://github.com/DIBBS-project/common-dibbs) project to the *settings.py* file, as in the following example:

```
MIDDLEWARE_CLASSES = [
  # ...
  'common_dibbs.django.CASUserBridgeMiddleware',
  # CASUserBridgeMiddleware *must be before* the below two
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'django.contrib.auth.middleware.RemoteUserMiddleware',
  # ...
]

AUTHENTICATION_BACKENDS = [
  'django.contrib.auth.backends.RemoteUserBackend',
]
```
