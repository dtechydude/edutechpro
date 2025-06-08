from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from testapp.models import Project, Task

# Register your models here.
class ProjectAdmin(admin.ModelAdmin):
    list_display=('name', 'description', 'owner')

class TaskAdmin(admin.ModelAdmin):
    list_display=('title', 'description', 'project')


admin.site.register(Project, ProjectAdmin)
admin.site.register(Task, TaskAdmin)
