from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from models import License, LicenseType


def lookup_via_npi(request, state, npi):
    l = get_object_or_404(License, state=state, npi=npi)
    return HttpResponse(l.as_json(), content_type="application/json")
    

def lookup_via_license(request, state, license_type, number):
    
   #lt = LicenseType
    print state, license_type, number
    l = get_object_or_404(License, license_type__state=state, license_type__license_type=license_type, number=number)
    
    return HttpResponse(l.as_json(), content_type="application/json")
    
def home(request):
    
    response = """
Welcome to the a server reference implemntation of Medical Licsense Verification
System (MLVS).

This is a reference implementation of a simple RESTFul web service that returns
license status information. Data is stored in a relational database of your choice.

See https://github.com/HHSIDEAlab/mlvs for more information.

Query MLVS with the provider's NPI or the state issued license number. Use HTTP
GET to query like so:
     
     http(s)://[SERVER]/license/[STATE_CODE]/[LICENSE_TYPE_CODE]/[LICENSE_NUMBER].json     

If the HTTP response code is 200, then a JSON response containing the status
information will be returned.  Below is an example.

    {
    "first_name": "Fred",
    "last_name": "Flinstone",
    "state": "WV",
    "credential": "Medical Doctor"
    "license_type": "MDR",
    "code": "WV-MDR-234234534",
    "number": "2342345345",
    "npi": "1223353456",
    "status": "ACTIVE",
    "created_at": "2012-04-20",
    "updated_at": "2014-08-14"
    }


If the HTTP response code is 404 or otherwise not 200, there is no answer on file
and the body of the response can be ignored because it is irrelevant.
    """ % (settings.DEFAULT_STATE)

    return HttpResponse(response, content_type="text/plain")