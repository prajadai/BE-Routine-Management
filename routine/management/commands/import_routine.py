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
            default='A',
            help='Default section name to use if not provided in data'
        )

    def handle(self, *args, **options):
        csv_path = os.path.join(settings.BASE_DIR, 'data', 'routine.csv')
        default_section = options['section']

        with open(csv_path, 'r') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                # Clean the data by stripping whitespace
                row = {k.strip(): v.strip() for k, v in row.items()}
                
                try:
                    # Department
                    department, _ = Department.objects.get_or_create(
                        name=row['Department']
                    )

                    # Semester
                    semester, _ = Semester.objects.get_or_create(
                        name=row['Semester'],
                        department=department
                    )

                    # Subject
                    subject, _ = Subject.objects.get_or_create(
                        name=row['Subject'],
                        semester=semester
                    )

                    # Teacher
                    teacher, _ = Teacher.objects.get_or_create(
                        name=row['Teacher'],
                        department=department
                    )

                    # Classroom
                    classroom, _ = Classroom.objects.get_or_create(
                        room_number=row['Classroom']
                    )

                    # Section - now using department instead of semester
                    section_name = row.get('Section', default_section)
                    section, _ = Section.objects.get_or_create(
                        name=section_name,
                        department=department  # Changed from semester to department
                    )

                    # Routine
                    Routine.objects.create(
                        day=row['Day'],
                        period=row['Period'],
                        semester=semester,
                        subject=subject,
                        teacher=teacher,
                        classroom=classroom,
                        section=section,
                        class_type=row.get('Class_Type', 'THEORY')
                    )

                    self.stdout.write(
                        self.style.SUCCESS(f"Imported: {row['Day']} {row['Period']} - {row['Subject']}")
                    )

                except KeyError as e:
                    self.stdout.write(
                        self.style.ERROR(f"Missing column in CSV: {str(e)} | Line {reader.line_num}")
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f"Error on line {reader.line_num}: {str(e)} | Data: {row}")
                    )