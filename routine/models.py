from django.db import models

# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Semester(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.department}"
    
class Subject(models.Model):
    name = models.CharField(max_length=100)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Teacher(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.department})"
    
class Classroom(models.Model):
    room_number = models.CharField(max_length=20, unique=True)
    capacity = models.PositiveIntegerField(blank=True, null=True)
    Department = models.ForeignKey(Department, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"Room {self.room_number} (Capacity:{self.capacity})"

#CHOICES for days of the week
DAY_CHOICES = [
    ('Sunday', 'Sunday'),
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday','Thursday'),
    ('Friday','Friday')
]

class Routine(models.Model):
    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    period = models.CharField(max_length=50) #eg 10:15-11:05
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)

    class Meta:
        #ensure no teahcer/classroom is double-booked
        unique_together = [
            ('day', 'period', 'teacher'),
            ('day', 'period', 'classroom'),
        ]

    def __str__(self):
        return f"{self.day} | {self.period} | {self.subject} | (Room:{self.classroom.room_number})"
    
