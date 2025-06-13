from django.core.management.base import BaseCommand
from routine.models import Department, Semester, Subject, Routine, Teacher, Classroom
import csv
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Imports routine data from CSV'

    def handle(self, *args, **options):
        csv_path = os.path.join(settings.BASE_DIR, 'data', 'routine.csv')

        with open(csv_path, 'r') as file:
            reader = csv.DictReader(file)
            reader.fieldnames = [field.strip() for field in reader.fieldnames]

            for row in reader:
                row = {k.strip(): v.strip() for k, v in row.items()}

                try:
                    # Department
                    dept, _ = Department.objects.get_or_create(
                        name=row['department_name']
                    )

                    # Semester
                    semester, _ = Semester.objects.get_or_create(
                        name=row['semester_name'],
                        department=dept
                    )

                    # Subject
                    subject, _ = Subject.objects.get_or_create(
                        name=row['subject'],
                        semester=semester
                    )

                    # Teacher
                    teacher, _ = Teacher.objects.get_or_create(
                        name=row['teacher'],
                        department=dept
                    )

                    # Classroom
                    classroom, _ = Classroom.objects.get_or_create(
                        room_number=row['classroom']
                    )

                    # Routine
                    Routine.objects.create(
                        day=row['day'],
                        period=row['period'],
                        semester=semester,
                        subject=subject,       # ✅ Now a Subject instance
                        teacher=teacher,
                        classroom=classroom
                    )

                    self.stdout.write(self.style.SUCCESS(f"Added: {row['day']} {row['period']}"))

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Line {reader.line_num}: {str(e)} | Data: {row}"))
