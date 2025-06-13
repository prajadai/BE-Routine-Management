# from import_export import resources
# from .models import Routine

# class RoutineResource(resources.ModelResource):
#     class Meta:
#         model = Routine
#         skip_unchanged = True  # Avoid duplicates
#         import_id_fields = ['day', 'period']  # Unique identifiers

# resources.py
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import Routine, Semester, Subject, Teacher, Classroom

class RoutineResource(resources.ModelResource):
    semester = fields.Field(
        column_name='semester',
        attribute='semester',
        widget=ForeignKeyWidget(Semester, 'name')
    )
    
    subject = fields.Field(
        column_name='subject',
        attribute='subject',
        widget=ForeignKeyWidget(Subject, 'name')
    )
    
    teacher = fields.Field(
        column_name='teacher',
        attribute='teacher',
        widget=ForeignKeyWidget(Teacher, 'name')
    )
    
    classroom = fields.Field(
        column_name='classroom',
        attribute='classroom',
        widget=ForeignKeyWidget(Classroom, 'name')
    )

    class Meta:
        model = Routine
        skip_unchanged = True
        import_id_fields = []
        fields = ('day', 'period', 'semester', 'subject', 'teacher', 'classroom')