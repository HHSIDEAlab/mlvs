from django.contrib import admin
from models import License, LicenseType



class LicenseTypeAdmin(admin.ModelAdmin):

    list_display = ('code', 'state', 'license_type', 'credential',  'provider_type', 'mac')      
    search_fields = ('state', 'license_type', 'provider_type', 'mac', 'credential')

admin.site.register(LicenseType, LicenseTypeAdmin)



class LicenseAdmin(admin.ModelAdmin):

    list_display = ('__unicode__', 'name', 'status', 'updated_at')      
    search_fields = ('number', 'npi', 'license_type', 'first_name', 'last_name')

admin.site.register(License, LicenseAdmin)
