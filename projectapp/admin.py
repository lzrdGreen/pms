from django.contrib import admin
from .models import Project, Task
# Register your models here.

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    search_fields = ('title', 'description')

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'due_date', 'priority', 'status')
    search_fields = ('title', 'description')
    list_filter = ('priority', 'status')

admin.site.register(Project, ProjectAdmin)
admin.site.register(Task, TaskAdmin)
