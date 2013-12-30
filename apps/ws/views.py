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
    
def home(request):
    
    response = """
Welcome to another instance of the Medical Licsense Verification System (MLVS).

This server is configured for the state of %s.

This is a reference implementation of a simple RESTFul web service that returns
license status information

Query MLVS with the provider's NPI or the state issued license number. Use HTTP
GET to query like so:

     https://[SERVER]/npi/[NPI]
     
             -or-
     
     https://[SERVER]/license/[LICENSE]     

If the HTTP response code is 200, then a JSON response containing the status
information will be returned.  Below is an example.

    {
    "first_name": "Fred",
    "last_name": "Flinstone",
    "state": "WV",
    "license_type": "MD",
    "number": "2342345345",
    "npi": "1223353456",
    "status": "ACTIVE",
    "created_at": "2013-12-30",
    "updated_at": "2013-12-30"
    }


If the HTTP response code is 404 or otherwise not 200, there is no answer on file
and the body of the response can be ignored because it is irrelevant.
    """ % (settings.DEFAULT_STATE)

    return HttpResponse(response, mimetype="text/plain")