from django.contrib import admin
from . models import *
# Register your models here.
from import_export.admin import ImportExportMixin
class ProjectAdmin(ImportExportMixin,admin.ModelAdmin):
    list_display = ('name','time_started')
    # list_filter = ('time_started',)
    
class OwnerAdmin(ImportExportMixin,admin.ModelAdmin):
    list_display=('full_name','email',)
   
class DepartmentAdmin(ImportExportMixin,admin.ModelAdmin):
    list_display=('name',)

class OwnerProfileAdmin(ImportExportMixin,admin.ModelAdmin):
    list_display=('name','is_organization')
    list_filter = ('is_organization',)

class DocumentAdmin(admin.ModelAdmin):
    readonly_fields = ('date_created','date_updated_on')


admin.site.register(Project,ProjectAdmin)
admin.site.register(Owner,OwnerAdmin)
admin.site.register(Department,DepartmentAdmin)
admin.site.register(OwnerProfile,OwnerProfileAdmin)
admin.site.register(Document,DocumentAdmin)