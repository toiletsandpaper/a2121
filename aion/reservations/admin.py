from django.contrib import admin

'''This creates a  look to register all models to admin
Disabled this feature in order to enable django-import-export
'''
# from django.apps import apps
# app = apps.get_app_config('reservations')

# for model_name, model in app.models.items():
#     admin.site.register(model) # Register all models
 
from import_export.admin import ImportExportModelAdmin
from .models import Resource, Announcement, Reservation, Profile, TimeBlock
from .models import School, Organization, EmailFilter

@admin.register(School)
class SchoolAdmin(ImportExportModelAdmin):
    pass

@admin.register(Organization)
class OrganizationAdmin(ImportExportModelAdmin):
    pass

@admin.register(EmailFilter)
class EmailFilterAdmin(ImportExportModelAdmin):
    pass

@admin.register(Resource)
class ResourceAdmin(ImportExportModelAdmin):
    pass

@admin.register(Announcement)
class AnnouncementAdmin(ImportExportModelAdmin):
    pass

@admin.register(Reservation)
class ReservationAdmin(ImportExportModelAdmin):
    pass

@admin.register(Profile)
class ProfileAdmin(ImportExportModelAdmin):
    pass

@admin.register(TimeBlock)
class TimeBlockAdmin(ImportExportModelAdmin):
    pass


'''Adding Import-Export to the User Model 
'''

from import_export import resources
from django.contrib.auth.models import User
class UserResource(resources.ModelResource):
    '''This class speficies the model and fields used in export 
    '''
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'last_login', 'date_joined')

admin.site.unregister(User)
@admin.register(User)
class UserAdmin(ImportExportModelAdmin):
    '''This class registers the UserAdmin area with the resource class 
    '''
    resource_class = UserResource
    pass

from analytics.models import LifetimeAionStat, LifetimeSchoolStat

@admin.register(LifetimeAionStat)
class LifetimeAionStatAdmin(admin.ModelAdmin):
    pass

@admin.register(LifetimeSchoolStat)
class LifetimeSchoolStatAdmin(admin.ModelAdmin):
    pass
