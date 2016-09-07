from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import redirect

import re
import json
import uuid

from django.template import RequestContext
from django.shortcuts import render_to_response

LOCAL_REDIRECT_SESSION_DICT = {}
LOCAL_USER_SESSION_DICT = {}
UUID_SESSION_REMOTE_SESSION_INDEX = {}
REMOTE_SESSION_UUID_SESSION_INDEX = {}


@csrf_exempt
def index(request, auth_token=None):

    # The following block will force the "request.session.sessionkey" to be set with a value
    if not request.session.exists(request.session.session_key):
        request.session.create()

    if not "uuid_session" in request.COOKIES:
        uuid_session = str(uuid.uuid4())
    else:
        uuid_session = request.COOKIES["uuid_session"]

    print("> uuid_session: %s" % (uuid_session))

    remote_session_key = None
    if "session_key" in request.POST:
        remote_session_key = request.POST["session_key"]
        REMOTE_SESSION_UUID_SESSION_INDEX[uuid_session] = remote_session_key
        UUID_SESSION_REMOTE_SESSION_INDEX[remote_session_key] = uuid_session

    if not request.user.is_authenticated():
        if uuid_session in REMOTE_SESSION_UUID_SESSION_INDEX:
            if remote_session_key is None:
                remote_session_key = REMOTE_SESSION_UUID_SESSION_INDEX[uuid_session]
            if uuid_session in UUID_SESSION_REMOTE_SESSION_INDEX:
                del UUID_SESSION_REMOTE_SESSION_INDEX[uuid_session]
            if uuid_session in LOCAL_USER_SESSION_DICT:
                del LOCAL_USER_SESSION_DICT[uuid_session]
        if remote_session_key in UUID_SESSION_REMOTE_SESSION_INDEX:
            del UUID_SESSION_REMOTE_SESSION_INDEX[remote_session_key]
        if remote_session_key in LOCAL_USER_SESSION_DICT:
            del LOCAL_USER_SESSION_DICT[remote_session_key]

    redirect_url = None

    if request.user.username != "anonymous" and uuid_session not in LOCAL_USER_SESSION_DICT:
        LOCAL_USER_SESSION_DICT[uuid_session] = request.user

    # # Extract the redirect URL if it exists
    # if "HTTP_REFERER" in request.META:
    #     if request.META["HTTP_HOST"] not in request.META["HTTP_REFERER"]:
    #         redirect_url = request.META["HTTP_REFERER"]
    #
    #     if "service=http" in request.META["HTTP_REFERER"]:
    #         m = re.search("service=http.*", request.META["HTTP_REFERER"])
    #         redirect_url = m.group(0)
    #         redirect_url = redirect_url.replace("service=", "")
    #         print(redirect_url)

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
            UUID_SESSION_REMOTE_SESSION_INDEX[remote_session_key] = request.user
            return redirect(redirect_url)

    response = render_to_response("casapp/index.html", RequestContext(request))
    print("> uuid_session: %s" % (uuid_session))
    response.set_cookie("uuid_session", uuid_session)
    return response


@csrf_exempt
def authenticate(request):
    authenticated = False
    username = None
    if "session_key" in request.REQUEST:
        session_key = request.REQUEST["session_key"]
        if session_key in UUID_SESSION_REMOTE_SESSION_INDEX:
            user = UUID_SESSION_REMOTE_SESSION_INDEX[session_key]
            if user.is_authenticated():
                authenticated = True
                username = user.username
    token = None
    if not authenticated:
        token = str(uuid.uuid4())
    response = {
        "response": authenticated,
        "token": token,
        "username": username
    }
    return HttpResponse(json.dumps(response))
