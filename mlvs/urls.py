from django.conf.urls import patterns, include, url

from django.contrib import admin
from apps.licenses.views import lookup_via_npi, lookup_via_license, home
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mlvs.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^$', home, name="home"),
    
    url(r'^npi/(?P<npi>\S+).json', lookup_via_npi,
            name="lookup_via_npi"),
    
    url(r'^license/(?P<state>\S+)/(?P<license_type>\S+)/(?P<number>\S+).json', lookup_via_license,
            name="lookup_via_license"),

)
