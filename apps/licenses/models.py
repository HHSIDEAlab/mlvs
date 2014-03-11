from django.db import models
from django.conf import settings
from localflavor.us.us_states import US_STATES
import json
from collections import OrderedDict

LICENSE_STATUS_CHOICES =( ("", "Unknown"),
                          ("ACTIVE","Active"),
                          ("ACTIVE_WITH_RESTRICTIONS","Active with Restrictions"),
                          ("EXPIRED","Expired"),
                          ("REVOKED","Revoked"),
                          ("DECEASED","Deceased"), )


class LicenseType(models.Model):
    state          = models.CharField(max_length=2,
                                    choices = US_STATES)
    license_type   = models.CharField(max_length=3)
    
    mac            =  models.IntegerField(max_length=2,
                        verbose_name = "Medicare Administrative Contractor")
    
    provider_type  = models.IntegerField(max_length=2)
    
    credential     = models.CharField(max_length=150)
    
    class Meta:
        
        unique_together =  (('state', 'license_type'), )

    def __unicode__(self):
        lt ="%s (%s-%s)" % (self.credential, self.state, self.license_type)
        return lt
    
    def code(self):
        lt ="%s-%s" % (self.state, self.license_type)
        return lt


class License(models.Model):
    

    license_type   = models.ForeignKey(LicenseType)
    
    
    number         = models.CharField(max_length=20)
    
    first_name     = models.CharField(max_length=100)
    last_name      = models.CharField(max_length=100)
    
    npi            = models.CharField(max_length=10, blank=True, default="")

    status         = models.CharField(max_length=10, choices=LICENSE_STATUS_CHOICES,
                                         default ="", blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True, auto_now_add=True)
        
    
    class Meta:
        
        unique_together =  (('license_type', 'number'), )
    
    def __unicode__(self):
        l ="%s-%s" % (self.license_type.code(), self.number)
        return l
    
    
    def name(self):
        n ="%s %s" % (self.first_name, self.last_name)
        return n
    
    def as_json(self):
        d = OrderedDict()
        d['first_name'] = self.first_name
        d['last_name'] = self.last_name
        d['state'] = self.license_type.state
        d['credential'] = self.license_type.credential
        d['code'] = str(self)
        d['license_type'] = self.license_type.license_type
        d['number'] = self.number
        d['npi'] = self.npi
        d['status'] = self.status
        d['created_at'] = str(self.created_at)
        d['updated_at'] = str(self.updated_at)
        j = json.dumps(d, indent=4)
        return j
