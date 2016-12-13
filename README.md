# Central Authentication Service

## Implementation

The implementation is based on the [**django-allauth**](https://github.com/pennersr/django-allauth) plugin, which provides advanced authentication mechanisms that can be used in Django.

## Implementation of the Authentication

### First-time visitor

The workflow is illustrated in the following figure:
[docs/first_time_user.png](docs/first_time_user.png)

#### (1) A user request is intercepted by CAS middleware

A user requests a view of a service that uses the Central Authentication Service (CAS). The request is intercepted by the CAS middleware. The middleware implements a behaviour (A), which checks if the user's session contains a *"session_key"* attribute, or if the user provided a username and a password. 

If it is the case, the user is known by the system, and behaviour (A) will act as described in the section ***Already identified visitor*** section.

If it is not the case, behaviour (A) will act as described in ***CAS middleware redirect to the CAS service***

#### (2) CAS middleware redirects to the CAS service

The CAS middleware redirects the user to the index view of the CAS service and behaviour (B) will be executed. Behaviour (B) basically associates the user's session (on the CAS service) with a redirect URL (in the original service), and a cookie is created on the user's browser to identify the user if the user access the index view for the first time.

##### non_authenticated_visitor_index

If (B) finds that the user is not authenticated, the user requests is routed to the ***"non_authenticated_visitor_index"*** method, which memorizes the user and the page he was trying to reach on the original service. The user is then redirected to a login webpage provided by the *all_auth* plugin.

Once the User is logged via *all_auth*, he is now authenticated and redirected again to the index view of the CAS service. The ***"authenticated_visitor_index"*** section describes what happens next.

##### authenticated_visitor_index

If (B) finds that the user is authenticated, the user requests is routed to the ***"authenticated_visitor_index"*** method, which fetches the redirection information associated to the authenticated user. Once one redirection URL is found, the user is redirected to this URL (on the original service), and behaviour described in section ***Already identified visitor*** will be executed this time. If not redirection URL could be found, the user is redirected to a simple webpage that displays that he is connected.

### Already identified visitor

The workflow is illustrated in the following figure:
[docs/authenticated_user.png](docs/authenticated_user.png)

#### (1) A user request is intercepted by CAS middleware

A user requests a view of a service that uses the Central Authentication Service (CAS). The request is intercepted by the CAS middleware. The middleware implements a behaviour (A), which checks if the user's session contains a "session_key" attribute, or if the user provided a username and a password. 

If it is the case, the user is known by the system, and behaviour (A) will act as described in the section ***Already identified visitor*** section.

If it is not the case, behaviour (A) will act as described in ***CAS middleware redirect to the CAS service***

#### (2) CAS middleware checks with the CAS service if the user's request is genuine

During its request on the Service, the user provided a set of credentials (username/password) or behaviour (A) identified a *"session_key"* attribute in the user's session. In this case, behaviour (A) tries to check with the CAS service if the request is genuine. To do so, (A) calls the [CentralAuthenticationBackend](https://github.com/DIBBS-project/common-dibbs/blob/master/common_dibbs/auth/auth.py).authenticate method : if transmits the some data (credentials or session_key value) to (C), which checks if it corresponding to an existing user. If it is the case, the service serves the user's request, otherwise the user is considered as unknown and the behaviour ***First-time visitor*** is executed.

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

