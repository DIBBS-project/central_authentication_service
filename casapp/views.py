import json
import logging
import uuid

from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, HttpResponse

SESSIONS = {
    "current": [],
    "tmp_uuid_to_redirect_link": []
}

logging.basicConfig(level=logging.DEBUG)


# @csrf_exempt
def index(request, auth_token=None):

    def _detect_potential_cookie_uuid_for_request(request):
        session_key = None
        if "session_key" in request.REQUEST and request.REQUEST["session_key"] != "None":
            session_key = request.REQUEST["session_key"]
        if "sessionid" in request.COOKIES:
            session_key = request.COOKIES["sessionid"]
        if session_key is not None:
            matching_sessions = filter(lambda s: s["session_key"] == session_key, SESSIONS["current"])
            sessions_with_token_uuid = filter(lambda s: s["token_uuid"] != None, matching_sessions)
            if len(sessions_with_token_uuid) > 0:
                return sessions_with_token_uuid[0]["token_uuid"]
        return None

    def _add_session(request, session_key=None):
        # check if there is a 'redirect_url' parameter and process it
        new_session = {
            "session_key": session_key if session_key else request.REQUEST["session_key"] if "session_key" in request.REQUEST else None,
            "token_uuid": request.COOKIES["uuid_session"],
            "redirect_url": request.REQUEST["redirect_url"] if "redirect_url" in request.REQUEST else None,
            "user": request.user,
            "request": request
        }
        if "redirect_url" in request.REQUEST:
            request.COOKIES["redirect_url"] = request.REQUEST["redirect_url"]

        SESSIONS["current"] += [new_session]

    def non_authenticated_visitor_index(request, auth_token=None):
        session_key = None
        if "session_key" in request.REQUEST and request.REQUEST["session_key"] != "None":
            session_key = request.REQUEST["session_key"]
        if session_key:
            _add_session(request)
        else:
            uuid_to_redirect_link = {
                "token_uuid": "",
                "redirect_link": ""
            }
            SESSIONS["tmp_uuid_to_redirect_link"] += [uuid_to_redirect_link]
        redirect_response = HttpResponseRedirect('/accounts/login/')
        redirect_response.set_cookie("uuid_session", request.COOKIES["uuid_session"])
        return redirect_response

    def authenticated_visitor_index(request, auth_token=None):
        session_key = request.COOKIES["sessionid"] if request.COOKIES["sessionid"] != "None" else None
        if session_key:
            _add_session(request, session_key=session_key)
        matching_sessions = filter(lambda s: s["token_uuid"] == request.COOKIES["uuid_session"], SESSIONS["current"])
        sessions_with_redirect_urls = filter(lambda s: s["redirect_url"] != None, matching_sessions)
        redirect_urls = map(lambda s: s["redirect_url"], sessions_with_redirect_urls)
        if len(redirect_urls):
            redirect_url = redirect_urls[0]
            response = redirect(redirect_url)
        else:
            response = render_to_response("casapp/index.html", RequestContext(request))
        return response

    # The following block will force the "request.session.sessionkey" to be set with a value
    if not request.session.exists(request.session.session_key):
        request.session.create()

    logging.debug(" index: (a) request.COOKIES: %s" % (request.COOKIES))
    if not "uuid_session" in request.COOKIES:
        potential_cookie_uuid = _detect_potential_cookie_uuid_for_request(request)
        if potential_cookie_uuid is not None:
            request.COOKIES["uuid_session"] = potential_cookie_uuid
        else:
            request.COOKIES["uuid_session"] = str(uuid.uuid4())
    uuid_session = request.COOKIES["uuid_session"]

    logging.debug(" index: (b) uuid_session: %s" % (uuid_session))
    if not request.user.is_authenticated():
        response = non_authenticated_visitor_index(request, auth_token)
    else:
        response = authenticated_visitor_index(request, auth_token)
    return response


# @csrf_exempt
def authenticate(request):
    authenticated = False
    username = None
    if "session_key" in request.REQUEST:
        session_key = request.REQUEST["session_key"]
        logging.debug(" authenticate: session_key=%s" % (session_key))
        matching_sessions = filter(lambda s: s["session_key"] == session_key, SESSIONS["current"])
        if len(matching_sessions) > 0:
            for session in matching_sessions:
                if session["user"].is_authenticated():
                    authenticated = True
                    username = session["user"].username
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
    logging.debug(" authenticate: response=%s" % (response))
    return HttpResponse(json.dumps(response))


# @csrf_exempt
def session_logout(request):
    if "session_key" in request.REQUEST:
        session_key = request.REQUEST["session_key"]
        logging.debug(" authenticate: session_key=%s" % (session_key))
        matching_sessions = filter(lambda s: s["session_key"] == session_key, SESSIONS["current"])
        if len(matching_sessions) > 0:
            for session in matching_sessions:
                logout(session["request"])
        token_uuids = map(lambda s: s["token_uuid"], matching_sessions)
        if len(token_uuids) > 0:
            for token_uuid in token_uuids:
                SESSIONS["current"] = filter(lambda s: s["token_uuid"] != token_uuid, SESSIONS["current"])
    response = {
        "response": True,
    }
    return HttpResponse(json.dumps(response))
