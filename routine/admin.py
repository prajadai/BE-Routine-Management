from django.contrib import admin
from .models import Department, Semester, Subject, Teacher, Classroom, Routine
from import_export.admin import ImportExportModelAdmin

# Register your models here.

@admin.register(Routine)
class RoutineAdmin(ImportExportModelAdmin):
    pass

admin.site.register(Department)
admin.site.register(Semester)
admin.site.register(Subject)
admin.site.register(Teacher)
admin.site.register(Classroom)
# admin.site.register(Routine)