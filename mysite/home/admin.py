from django.contrib import admin
from home.models import Contact, Orders
from .models import Certi, Registration, Project
from django.contrib.auth.models import Group

admin.site.site_header = 'DEPT AI'

# Register other models
admin.site.register(Contact)
admin.site.register(Orders)
admin.site.register(Project)

# Unregister default Group model if you want
# admin.site.unregister(Group)

# Only register Certi and Registration if they aren't already registered
if not admin.site.is_registered(Certi):
    class CertiAdmin(admin.ModelAdmin):
        list_display = ('event_name', 'event_start_date', 'event_end_date', 'is_approved', 'is_completed')
    admin.site.register(Certi, CertiAdmin)

if not admin.site.is_registered(Registration):
    class RegistrationAdmin(admin.ModelAdmin):
        list_display = ('user', 'event', 'registered_on')
    admin.site.register(Registration, RegistrationAdmin)
