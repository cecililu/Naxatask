from django.contrib import admin
from . models import *
# Register your models here.

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name','time_started')
    # list_filter = ('time_started',)

class OwnerAdmin(admin.ModelAdmin):
    list_display=('full_name','email',)
   
class DepartmentAdmin(admin.ModelAdmin):
    list_display=('name',)

class OwnerProfileAdmin(admin.ModelAdmin):
    list_display=('name','is_organization')
    list_filter = ('is_organization',)

admin.site.register(Project,ProjectAdmin)
admin.site.register(Owner,OwnerAdmin)
admin.site.register(Department,DepartmentAdmin)
admin.site.register(OwnerProfile,OwnerProfileAdmin)