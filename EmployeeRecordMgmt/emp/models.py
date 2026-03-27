from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.apps import apps
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


# Create your models here.
def get_user_count():
    return CustomUser.objects.count()

class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, validators=[validate_email])
    department = models.CharField(max_length=100)

    def clean(self):
        super().clean()
        if not self.first_name or not self.last_name:
            raise ValidationError('First name and last name cannot be empty.')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        db_table = 'employee'
        ordering = ['last_name']
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'

class CustomUser(AbstractUser):
    # Add custom fields if needed
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    pass 

    def clean(self):
        super().clean()
        if not self.phone_number:
            raise ValidationError('Phone number is required.')

    def __str__(self):
        return self.username
    
class EmployeeDetail(models.Model):
    user = models.ForeignKey('emp.CustomUser', on_delete=models.CASCADE)
    employee_code = models.CharField(max_length=50)
    designation = models.CharField(max_length=100, null=True)
    department = models.CharField(max_length=100, null=True)
    contact = models.CharField(max_length=15, null=True)
    gender = models.CharField(max_length=50, null=True)
    joining_date = models.DateField(null=True)

    def clean(self):
        super().clean()
        if not self.employee_code:
            raise ValidationError('Employee code is required.')
        if not self.designation:
            raise ValidationError('Designation is required.')
        if not self.department:
            raise ValidationError('Department is required.')
        if not self.contact:
            raise ValidationError('Employee code is required.')
        if not self.gender:
            raise ValidationError('Designation is required.')
        if not self.joining_date:
            raise ValidationError('Department is required.')

    def __str__(self):
        return self.user.username if self.user.username else 'User  without username'

class EmployeeEducation(models.Model):
    user = models.ForeignKey('emp.CustomUser', on_delete=models.CASCADE)
    postgraduate_course = models.CharField(max_length=100, null=True)
    postgraduate_institution = models.CharField(max_length=200, null=True)
    postgraduate_year_of_passing = models.CharField(max_length=20, null=True)
    postgraduate_percentage = models.CharField(max_length=30, null=True)
    undergraduate_course = models.CharField(max_length=100, null=True)
    undergraduate_institution = models.CharField(max_length=200, null=True)
    undergraduate_year_of_passing = models.CharField(max_length=20, null=True)
    undergraduate_percentage = models.CharField(max_length=30, null=True)
    ssc_course = models.CharField(max_length=100, null=True)
    ssc_institution = models.CharField(max_length=200, null=True)
    ssc_year_of_passing = models.CharField(max_length=20, null=True)
    ssc_percentage = models.CharField(max_length=30, null=True)
    hsc_course = models.CharField(max_length=100, null=True)
    hsc_institution = models.CharField(max_length=200, null=True)
    hsc_year_of_passing = models.CharField(max_length=20, null=True)
    hsc_percentage = models.CharField(max_length=30, null=True)

    def clean(self):
        super().clean()
        if not self.postgraduate_course and not self.undergraduate_course:
            raise ValidationError('At least one educational qualification is required.')
    
    def __str__(self):
        return self.user.username if self.user.username else 'User without username'

class EmployeeExperience(models.Model):
    user = models.ForeignKey('emp.CustomUser', on_delete=models.CASCADE,)
    company1_name = models.CharField(max_length=100, null=True)
    company1_designation = models.CharField(max_length=100, null=True)
    company1_salary = models.CharField(max_length=100, null=True)
    company1_duration = models.CharField(max_length=100, null=True)
    company2_name = models.CharField(max_length=100, null=True)
    company2_designation = models.CharField(max_length=100, null=True)
    company2_salary = models.CharField(max_length=100, null=True)
    company2_duration = models.CharField(max_length=100, null=True)
    company3_name = models.CharField(max_length=100, null=True)
    company3_designation = models.CharField(max_length=100, null=True)
    company3_salary = models.CharField(max_length=100, null=True)
    company3_duration = models.CharField(max_length=100, null=True)
    def __str__(self):
        return self.user.username if self.user.username else 'User without username'
    
class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    
class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class LeaveRequest(models.Model):
        employee = models.ForeignKey('emp.CustomUser', on_delete=models.CASCADE)
        start_date = models.DateField()
        end_date = models.DateField()
        reason = models.TextField()
        status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending')

        def clean(self):
            # Call the parent class's clean method
            super().clean()

            # Custom validation
            if self.end_date < self.start_date:
                raise ValidationError('End date must be after start date.')
        
        def __str__(self):
            return f"{self.employee.username} - {self.status}"

class SomeOtherModel(models.Model):
    employee = models.ForeignKey('emp.Employee', on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"SomeOtherModel for {self.employee.name}"

class YourModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    email = models.EmailField()

    def __str__(self):
        return self.name
    
class Employee_records(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    position = models.CharField(max_length=100)
    department = models.CharField(max_length=100)

    def __str__(self):
        return self.name