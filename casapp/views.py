from rest_framework.response import Response
from rest_framework.decorators import api_view


# @api_view(['GET', 'POST', ])
# def index(request):
#     return Response({"user": "%s" % (request.user)}, status=200)

from django.template import RequestContext
from django.shortcuts import render_to_response


def index(request):

    return render_to_response("casapp/index.html",
                              RequestContext(request))


def authenticate(request):
    return Response({"response": True})
