# Central Authentication Service

## Implementation

The implementation is based on the [**django-allauth**](https://github.com/pennersr/django-allauth) plugin, which provides advanced authentication mechanisms that can be used in Django.

## Implementation of the Authentication

### First-time visit

### Already logged-in user

## How to integrate the Central Authentication Service with a new DIBBs project?

Add the [CentralAuthenticationMiddleware](https://github.com/DIBBS-project/common-dibbs/blob/master/common_dibbs/auth/auth.py) from the [common_dibbs](https://github.com/DIBBS-project/common-dibbs) project, as in the following example:

```
MIDDLEWARE_CLASSES = [
    [...]
    'common_dibbs.auth.auth.CentralAuthenticationMiddleware'
]
```

In the following link, you will find an example of CAS integration in a DIBBs project:
https://github.com/DIBBS-project/operation_manager/blob/master/operation_manager/settings.py#L58

