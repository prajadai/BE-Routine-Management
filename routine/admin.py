from django.contrib import admin
from .models import Department, Semester, Subject, Teacher, Classroom, Routine
from import_export.admin import ImportExportModelAdmin
from django.http import HttpResponse
import csv
# Register your models here.

@admin.register(Routine)
class RoutineAdmin(ImportExportModelAdmin):
    list_display = ['day','semester','section','subject','teacher','classroom','class_type']
    actions = ['export_as_timetable']
    ordering=['day','period__start_time']
    # list_filter = ('day','semester')

    def export_as_timetable(self, request, queryset):

        # Periods sorted by time order
        periods = sorted(set(r.period for r in queryset))
        days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

        # Initialize timetable
        timetable = {day: {period: "-" for period in periods} for day in days}

        for r in queryset:
            cell = f"{r.subject}\n({r.teacher})\n{r.classroom}"
            if timetable[r.day][r.period] != "-":
                timetable[r.day][r.period] += f"\n---\n{cell}"
            else:
                timetable[r.day][r.period] = cell

        # Create response
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="timetable.csv"'
        writer = csv.writer(response)

        # Header
        writer.writerow(['Period/Day'] + days)

        # Rows
        for period in periods:
            row = [period]
            for day in days:
                row.append(timetable[day][period])
            writer.writerow(row)

        return response

admin.site.register(Department)
admin.site.register(Semester)
admin.site.register(Subject)
admin.site.register(Teacher)
admin.site.register(Classroom)
# admin.site.register(Routine)