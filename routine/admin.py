from django.contrib import admin
from .models import Department, Semester, Subject, Teacher, Classroom, Routine

# Register your models here.

admin.site.register(Department)
admin.site.register(Semester)
admin.site.register(Subject)
admin.site.register(Teacher)
admin.site.register(Classroom)
admin.site.register(Routine)