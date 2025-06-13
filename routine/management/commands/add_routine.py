from django.core.management.base import BaseCommand
from routine.models import Department, Semester, Subject, Teacher, Classroom, Routine

class Command(BaseCommand):
    help = 'Add routine manually from command line'

    def handle(self, *args, **kwargs):
        day = input("Enter day: ")
        period = input("Enter period (e.g., 10:15-11:55): ")
        dept_name = input("Enter department name: ")
        semester_name = input("Enter semester name: ")
        subject_name = input("Enter subject name: ")
        teacher_name = input("Enter teacher name: ")
        classroom_number = input("Enter classroom number: ")

        dept, _ = Department.objects.get_or_create(name=dept_name)
        semester, _ = Semester.objects.get_or_create(name=semester_name, department=dept)
        subject, _ = Subject.objects.get_or_create(name=subject_name, semester=semester)
        teacher, _ = Teacher.objects.get_or_create(name=teacher_name, department=dept)
        classroom, _ = Classroom.objects.get_or_create(room_number=classroom_number)

        Routine.objects.create(
            day=day,
            period=period,
            semester=semester,
            subject=subject,
            teacher=teacher,
            classroom=classroom
        )

        self.stdout.write(self.style.SUCCESS("✅ Routine entry added successfully!"))
