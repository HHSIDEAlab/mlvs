from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from models import License


def lookup_via_npi(request, npi):
    l = get_object_or_404(License, npi=npi)
    return HttpResponse(l.as_json(), mimetype="application/json")
    

def lookup_via_license(request, number):
    l = get_object_or_404(License, number=number)
    return HttpResponse(l.as_json(), mimetype="application/json")