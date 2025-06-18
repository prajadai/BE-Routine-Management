from django.core.management.base import BaseCommand
from routine.models import Department, Semester, Subject, Routine, Teacher, Classroom, Section
import csv
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Imports routine data from CSV'

    def add_arguments(self, parser):
        parser.add_argument(
            '--section',
            type=str,
            default='AB',
            help='Default section name to use if not provided in data'
        )

    def handle(self, *args, **options):
        default_section = options['section']  # This defines default_section
        csv_path = os.path.join(settings.BASE_DIR, 'data', 'routine.csv')

        with open(csv_path, 'r') as file:
            reader = csv.DictReader(file)
            reader.fieldnames = [field.strip() for field in reader.fieldnames]

            for row in reader:
                row = {k.strip(): v.strip() for k, v in row.items()}

                try:
                    # Department
                    dept, _ = Department.objects.get_or_create(
                        name=row['department']
                    )

                    # Semester
                    semester, _ = Semester.objects.get_or_create(
                        name=row['semester'],
                        department=dept
                    )

                    print("DEBUG:", row['subject'], semester)

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

                    # Section
                    section_name = row.get('section', default_section)
                    section, _ = Section.objects.get_or_create(
                        name=section_name,
                        semester=semester
                    )

                    # Routine
                    Routine.objects.create(
                        day=row['day'],
                        period=row['period'],
                        semester=semester,
                        subject=subject,       # ✅ Now a Subject instance
                        teacher=teacher,
                        classroom=classroom,
                        section=section,
                        class_type=row.get('class_type','THEORY')
                    )

                    self.stdout.write(self.style.SUCCESS(f"Added: {row['day']} {row['period']}"))

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Line {reader.line_num}: {str(e)} | Data: {row}"))
