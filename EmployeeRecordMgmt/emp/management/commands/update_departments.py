from django.core.management.base import BaseCommand
from django.apps import apps

class Command(BaseCommand):
    help = 'Update Department Information'

    def handle(self, *args, **options):
        Department = apps.get_model('emp', 'Department')

        departments = Department.objects.all()
        for department in departments:
            department.employee_count = 0
            department.save()
            self.stdout.write(self.style.SUCCESS(f'Updated department: {department.name}')) 
        return super().handle(*args, **options)