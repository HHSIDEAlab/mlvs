from django.db import models
from django.conf import settings
from localflavor.us.us_states import US_STATES
import json
from collections import OrderedDict

LICENSE_STATUS_CHOICES =( ("UNK", "Unknown"),
                          ("ACTIVE","Active"),
                          ("ACTIVE_WITH_RESTRICTIONS","Active with Restrictions"),
                          ("EXPIRED","Expired"),
                          ("REVOKED","Revoked"),
                          ("DECEASED","Deceased"), )

LICENSE_TYPE_CHOICES =(   ("MD", "Medical Doctor (MD)"),
                          ("DO","Doctor of Osteopathy (DO)"),
                          ("RN","Registered Nurse (RN)"),
                          ("OTHER","Other"), )

class License(models.Model):
    
    first_name     = models.CharField(max_length=100)
    last_name      = models.CharField(max_length=100)
    number         = models.CharField(max_length=20, unique=True)
    npi            = models.CharField(max_length=20)
    state          = models.CharField(max_length=2,  blank=True,
                                      default=settings.DEFAULT_STATE,
                                    choices = US_STATES)
    license_type   = models.CharField(max_length=5,  blank=True, default="",
                                    choices = LICENSE_TYPE_CHOICES)

    status         = models.CharField(max_length=10, choices=LICENSE_STATUS_CHOICES,
                                         default ="")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True, auto_now_add=True)
        
    def __unicode__(self):
        l ="%s-%s" % (self.state, self.number)
        return l
    
    def as_json(self):
        d = OrderedDict()
        d['first_name'] = self.first_name
        d['last_name'] = self.last_name
        d['state'] = self.state
        d['number'] = self.number
        d['npi'] = self.npi
        d['status'] = self.status
        d['created_at'] = str(self.created_at)
        d['updated_at'] = str(self.updated_at)
        j = json.dumps(d, indent=4)
        return j
