from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from import_export.admin import ImportExportModelAdmin

from .models import *

class ObservationAdmin(admin.ModelAdmin):
    list_display = ('owner', 'users_organization', 'users_department', 'character', 'category', 'photo1', 'photo2',
                    'photo3', 'photo4', 'photo5', 'risk', 'site', 'place', 'description', 'correction',
                    'control', 'manager', 'date_closed_target')

    search_fields = ('user', 'character', 'category', 'view', 'site', 'place', 'manager')

    list_filter = ('owner', 'users_organization', 'users_department', 'character', 'dialog', 'category',
                   'risk', 'view', 'site', 'place', 'manager')

class SiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'sites_organisation', 'sites_manager')

    search_fields = ('name', 'sites_organisation', 'sites_manager')

    list_filter = ('name', 'sites_organisation', 'sites_manager')

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'users_organization', 'users_department', 'responsible_manager', 'is_manager')

    search_fields = ('user', 'users_organization', 'users_department', 'responsible_manager', 'is_manager')

    list_filter = ('user', 'users_organization', 'users_department', 'responsible_manager', 'is_manager')

class PlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'place_organisation', 'site_place')

    search_fields = ('name', 'place_organisation', 'site_place')

    list_filter = ('name', 'place_organisation', 'site_place')


# Define a new User admin
# class UserAdmin(ImportExportModelAdmin, BaseUserAdmin):
#     list_display = ('email', 'first_name', 'last_name')
#     list_filter = ('is_staff', 'is_superuser')

# Re-register UserAdmin
# admin.site.unregister(User)
# admin.site.register(User,UserAdmin)

admin.site.register(Observation, ObservationAdmin)
admin.site.register(Category)
admin.site.register(View)
admin.site.register(Place, PlaceAdmin)
admin.site.register(Control)
admin.site.register(Organization)
admin.site.register(Department)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Site, SiteAdmin)


