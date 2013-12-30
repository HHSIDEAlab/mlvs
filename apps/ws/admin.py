from django.contrib import admin
from models import License



class LicenseAdmin(admin.ModelAdmin):

    list_display = ('first_name', 'last_name', 'number', 'npi', 'license_type', 'status', 'updated_at')      
    search_fields = ('number', 'npi', 'license_type', 'first_name', 'last_name')

admin.site.register(License, LicenseAdmin)
