from django.db.models.signals import post_save
from django.dispatch import receiver
from django.apps import apps

@receiver(post_save, sender='emp.Employee')
def employee_saved(sender, instance, created, **kwargs):
    # Use apps.get_model to reference another model if needed
    Department = apps.get_model('emp', 'Department')

    if created:
        department = instance.department
        department.employee_count += 1
        department.save()
        print(f"Updated employee count for {department.name}: {department.employee_count}")