import json
import uuid

from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User

LOCAL_REDIRECT_SESSION_DICT = {}
UUID_SESSION_REQUEST_INDEX = {}
UUID_SESSION__REMOTE_SESSION_INDEX = {}
REMOTE_SESSION__USER_INDEX = {}
REMOTE_SESSION_UUID_SESSION_INDEX = {}


@csrf_exempt
def index(request, auth_token=None):

    # The following block will force the "request.session.sessionkey" to be set with a value
    if not request.session.exists(request.session.session_key):
        request.session.create()

    uuid_session = request.COOKIES["uuid_session"] if "uuid_session" in request.COOKIES else str(uuid.uuid4())
    print("> uuid_session: %s" % (uuid_session))

    remote_session_key = None
    if "session_key" in request.POST:
        remote_session_key = request.POST["session_key"]
        REMOTE_SESSION_UUID_SESSION_INDEX[uuid_session] = remote_session_key
        UUID_SESSION__REMOTE_SESSION_INDEX[remote_session_key] = uuid_session

    if not request.user.is_authenticated():
        if uuid_session in REMOTE_SESSION_UUID_SESSION_INDEX:
            if remote_session_key is None:
                remote_session_key = REMOTE_SESSION_UUID_SESSION_INDEX[uuid_session]
            if uuid_session in UUID_SESSION__REMOTE_SESSION_INDEX:
                del UUID_SESSION__REMOTE_SESSION_INDEX[uuid_session]
        if remote_session_key in UUID_SESSION__REMOTE_SESSION_INDEX:
            del UUID_SESSION__REMOTE_SESSION_INDEX[remote_session_key]

    redirect_url = None
    if "redirect_url" in request.POST:
        redirect_url = request.POST["redirect_url"]

    if redirect_url:
        LOCAL_REDIRECT_SESSION_DICT[uuid_session] = redirect_url

        print(redirect_url)
    else:
        if uuid_session in LOCAL_REDIRECT_SESSION_DICT:
            redirect_url = LOCAL_REDIRECT_SESSION_DICT[uuid_session]
            del LOCAL_REDIRECT_SESSION_DICT[uuid_session]
            remote_session_key = REMOTE_SESSION_UUID_SESSION_INDEX[uuid_session]
            REMOTE_SESSION__USER_INDEX[remote_session_key] = request.user
            UUID_SESSION_REQUEST_INDEX[remote_session_key] = request
            return redirect(redirect_url)

    if request.user.is_authenticated():
        response = render_to_response("casapp/index.html", RequestContext(request))
    else:
        response = redirect('/accounts/login/')

    print("> uuid_session: %s" % (uuid_session))
    response.set_cookie("uuid_session", uuid_session)
    return response


@csrf_exempt
def authenticate(request):
    authenticated = False
    username = None
    if "session_key" in request.REQUEST:
        session_key = request.REQUEST["session_key"]
        if session_key in REMOTE_SESSION__USER_INDEX:
            user = REMOTE_SESSION__USER_INDEX[session_key]
            if user.is_authenticated():
                authenticated = True
                username = user.username
    if "username" in request.REQUEST and "password" in request.REQUEST:
        username = request.REQUEST["username"]
        password = request.REQUEST["password"]
        result = User.objects.filter(username=username)
        if len(result) > 0:
            authenticated = result[0].check_password(password)
            if not authenticated:
                username = "unauthorized_user"
    token = None
    if not authenticated:
        token = str(uuid.uuid4())
    response = {
        "response": authenticated,
        "token": token,
        "username": username
    }
    return HttpResponse(json.dumps(response))


@csrf_exempt
def session_logout(request):
    if "session_key" in request.REQUEST:
        session_key = request.REQUEST["session_key"]
    else:
        session_key = request.session.session_key
    if session_key in UUID_SESSION_REQUEST_INDEX:
        logout(UUID_SESSION_REQUEST_INDEX[session_key])
        del UUID_SESSION_REQUEST_INDEX[session_key]
    if session_key in UUID_SESSION__REMOTE_SESSION_INDEX:
        del UUID_SESSION__REMOTE_SESSION_INDEX[session_key]
    if session_key in REMOTE_SESSION__USER_INDEX:
        del REMOTE_SESSION__USER_INDEX[session_key]
    logout(request)
    response = {
        "response": True,
    }
    return HttpResponse(json.dumps(response))
