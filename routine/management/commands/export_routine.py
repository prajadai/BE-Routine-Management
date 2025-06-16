import csv
from django.core.management.base import BaseCommand
from routine.models import Routine

DAY_ORDER= { 'Sunday':1, 'Monday':2, 'Tuesday':3, 'Wednesday':4, 'Thursday':5, 'Friday':6}

class Command(BaseCommand):
    help = 'Export routine in order of days and periods in a csv file format'

    def handle(self, *args, **options):
        days = options.get('days')  # This is a list like ['Sunday', 'Wednesday']

        routines = Routine.objects.select_related(
            'semester', 'subject', 'teacher', 'classroom'
        )
        if days:
            routines = routines.filter(day__in=days)

        filename = 'routine_export.csv'

        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Day','Period','Semester','Department','Subject','Teacher','Classroom'])

            # routines = Routine.objects.select_related(
            #     'semester','subject','teacher', 'classroom'
            # )
            # routines = Routine.objects.select_related(
            #     'semester','subject','teacher', 'classroom'
            # ).filter(day__in=['Sunday', 'Tuesday','Friday'])

        # Sorting manually by day and period
            sorted_routines = sorted(routines, key=lambda r: (DAY_ORDER.get(r.day, 99), r.period))

            for r in sorted_routines:
                writer.writerow([
                    r.day,
                    r.period,
                    r.semester.name,
                    r.semester.department.name,
                    r.subject.name,
                    r.teacher.name,
                    r.classroom.room_number
                ])

        # self.stdout.write(self.style.SUCCESS(f'Routine exported successfully to {filename}'))
        self.stdout.write(self.style.SUCCESS(
            f'Routine exported to {filename}' + (f' for days: {", ".join(days)}' if days else '')
        ))
        

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            nargs='+',
            type=str,
            help='Days to export routines for (e.g. --days Sunday Wednesday)'
    )
