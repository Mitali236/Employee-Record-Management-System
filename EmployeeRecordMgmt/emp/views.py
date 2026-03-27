from django.contrib import messages
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden
from .models import CustomUser, LeaveRequest, Employee, get_user_count
from django.http import HttpResponse
from django.contrib.auth import get_user_model 
from .forms import LeaveRequestForm, CustomUser, CustomForm, SignUpForm, SignInForm
from django.apps import apps
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm
import re
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

# Create your views here.

def index(request):
    return render(request,'index.html')

def validate_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, email):
        raise ValidationError("Invalid email format.")

def validate_password(password):
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long.")
    if not re.search(r'[A-Z]', password):
        raise ValidationError("Password must contain at least one uppercase letter.")
    if not re.search(r'[a-z]', password):
        raise ValidationError("Password must contain at least one lowercase letter.")
    if not re.search(r'\d', password):
        raise ValidationError("Password must contain at least one number.")
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise ValidationError("Password must contain at least one special character.")

def registration(request):
    error_message = ""
    if request.method == "POST":
        print(request.POST)

        # Check if all required fields are present
        missing_fields = [key for key in ['firstname', 'lastname', 'empcode', 'email', 'pwd', 'cpwd'] if key not in request.POST]
        if missing_fields:
            error_message = f"Missing fields: {', '.join(missing_fields)}"
            return render(request, 'registration.html', {'error': True, 'error_message': error_message})

        fn = request.POST['firstname']
        ln = request.POST['lastname']
        ec = request.POST['empcode']
        em = request.POST['email']
        pwd = request.POST['pwd']
        cpwd = request.POST['cpwd']

        # Validate email
        try:
            validate_email(em)
        except ValidationError as e:
            error_message = str(e)
            return render(request, 'registration.html', {'error': True, 'error_message': error_message})

        # Validate password
        try:
            validate_password(pwd)
        except ValidationError as e:
            error_message = str(e)
            return render(request, 'registration.html', {'error': True, 'error_message': error_message})

        # Check if passwords match
        if pwd != cpwd:
            error_message = "Passwords do not match."
            return render(request, 'registration.html', {'error': True, 'error_message': error_message})

        # Check if the user already exists
        if User.objects.filter(username=em).exists():
            error_message = "User already exists."
            return render(request, 'registration.html', {'error': True, 'error_message': error_message})

        try:
            user = User.objects.create_user(first_name=fn, last_name=ln, username=em, password=pwd)
            EmployeeDetail.objects.create(user=user, empcode=ec)
            EmployeeExperience.objects.create(user=user)
            EmployeeEducation.objects.create(user=user)

            # After successful registration
            return HttpResponseRedirect('/success/')  # Redirect to a success page

            # Or, if you want to go back to the registration page with a success message
            return HttpResponseRedirect('/registration?success=true')  # Redirect back to registration

        except Exception as e:
            error_message = f"Error: {e}"
            print(f"Error: {e}")

    return render(request, 'registration.html', {'error': False, 'error_message': error_message})

def emp_login(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['emailid']
        p = request.POST['password']
        user = authenticate(username=u,password=p)
        if user:
            login(request,user)
            error = "no"
        else:
            error = "yes"
    return render(request,'emp_login.html', locals())

def emp_home(request):
    if not request.user.is_authenticated:
        return redirect('emp_login')
    return render(request,'emp_home.html')

def Logout(request):
    logout(request)
    return redirect('index')


def profile(request):
    if not request.user.is_authenticated:
        return redirect('emp_login')
    error = ""
    user = request.user
    employee = EmployeeDetail.objects.get(user=user)
    if request.method == "POST":
        fn = request.POST['firstname']
        ln = request.POST['lastname']
        ec = request.POST['empcode']
        dept = request.POST['department']
        designation = request.POST['designation']
        contact = request.POST['contact']
        jdate = request.POST['jdate']
        gender = request.POST['gender']

        employee.user.first_name = fn
        employee.user.last_name = ln
        employee.empcode = ec
        employee.empdept = dept
        employee.designation = designation
        employee.contact = contact
        employee.gender = gender

        if jdate:
            employee.joiningdate = jdate

        try:
            employee.save()
            employee.user.save()
            error = "no"
        except:
            error = "yes"


    return render(request,'profile.html',locals())

def admin_login(request):
    return render(request,'admin_login.html')

def my_experience(request):
    if not request.user.is_authenticated:
        return redirect('emp_login')

    user = request.user
    experience = EmployeeExperience.objects.get(user=user)



    return render(request,'my_experience.html',locals())

def edit_myexperience(request):
    if not request.user.is_authenticated:
        return redirect('emp_login')
    error = ""
    user = request.user
    experience = EmployeeExperience.objects.get(user=user)
    if request.method == "POST":
        company1name = request.POST['company1name']
        company1desig = request.POST['company1desig']
        company1salary = request.POST['company1salary']
        company1duration = request.POST['company1duration']

        company2name = request.POST['company2name']
        company2desig = request.POST['company2desig']
        company2salary = request.POST['company2salary']
        company2duration = request.POST['company2duration']

        company3name = request.POST['company3name']
        company3desig = request.POST['company3desig']
        company3salary = request.POST['company3salary']
        company3duration = request.POST['company3duration']

        experience.company1name = company1name
        experience.company1desig = company1desig
        experience.company1salary = company1salary
        experience.company1duration = company1duration

        experience.company2name = company2name
        experience.company2desig = company2desig
        experience.company2salary = company2salary
        experience.company2duration = company2duration

        experience.company3name = company3name
        experience.company3desig = company3desig
        experience.company3salary = company3salary
        experience.company3duration = company3duration



        try:
            experience.save()
            error = "no"
        except:
            error = "yes"


    return render(request,'edit_myexperience.html',locals())

def my_education(request):
    if not request.user.is_authenticated:
        return redirect('emp_login')
        education = EmployeeEducation.objects.get(user=user)

    user = request.user

    return render(request,'my_education.html',locals())

def edit_myeducation(request):
    if not request.user.is_authenticated:
        return redirect('emp_login')
    error = ""
    user = request.user
    education = EmployeeEducation.objects.get(user=user)
    if request.method == "POST":
        coursepg = request.POST['coursepg']
        schoolclgpg = request.POST['schoolclgpg']
        yearofpassingpg = request.POST['yearofpassingpg']
        percentagepg = request.POST['percentagepg']

        coursegra = request.POST['coursegra']
        schoolclggra = request.POST['schoolclggra']
        yearofpassinggra = request.POST['yearofpassinggra']
        percentagegra = request.POST['percentagegra']

        coursessc = request.POST['coursessc']
        schoolclgssc = request.POST['schoolclgssc']
        yearofpassingssc = request.POST['yearofpassingssc']
        percentagessc = request.POST['percentagessc']

        coursehsc = request.POST['coursehsc']
        schoolclghsc = request.POST['schoolclghsc']
        yearofpassinghsc = request.POST['yearofpassinghsc']
        percentagehsc = request.POST['percentagehsc']

        education.coursepg = coursepg
        education.schoolclgpg = schoolclgpg
        education.yearofpassingpg = yearofpassingpg
        education.percentagepg = percentagepg

        education.coursegra = coursegra
        education.schoolclggra = schoolclggra
        education.yearofpassinggra = yearofpassinggra
        education.percentagegra = percentagegra

        education.coursessc = coursessc
        education.schoolclgssc = schoolclgssc
        education.yearofpassingssc = yearofpassingssc
        education.percentagessc = percentagessc

        education.coursehsc = coursehsc
        education.schoolclghsc = schoolclghsc
        education.yearofpassinghsc = yearofpassinghsc
        education.percentagehsc = percentagehsc

        try:
            education.save()
            error = "no"
        except:
            error = "yes"


    return render(request,'edit_myeducation.html',locals())

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            return render(request, 'change_password.html', {'error': 'no'})  # Success
        else:
            # Check if the old password is incorrect
            if form.errors.get('old_password'):
                return render(request, 'change_password.html', {'error': 'not'})  # Current password is wrong
            return render(request, 'change_password.html', {'error': 'yes'})  # General error
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})

def admin_login(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['username']
        p = request.POST['pwd']

        user = authenticate(request, username=u, password=p)
        try:
            if user.is_staff:
                login(request, user)
                error = "no"

            else:
                error = "yes"
        except:
            error = "yes"
    return render(request, 'admin_login.html', locals())

def admin_home(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    return render(request,'admin_home.html')

def change_passwordadmin(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error = ""
    user = request.user

    if request.method == "POST":
        c = request.POST['currentpassword']
        n = request.POST['newpassword']

        try:
            if user.check_password(c):
                user.set_password(n)
                user.save()
                error = "no"
            else:
                error = "not"
        except:
            error = "yes"


    return render(request,'change_passwordadmin.html',locals())

def all_employee(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    employee = EmployeeDetail.objects.all()
    return render(request, 'all_employee.html', locals())

def delete_employee(request, pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    user = User.objects.get(id=pid)
    user.delete()
    return redirect('all_employee')

def edit_profile(request, pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error = ""
    user = request.user
    employee = EmployeeDetail.objects.all()
    if request.method == "POST":
        fn = request.POST['firstname']
        ln = request.POST['lastname']
        ec = request.POST['empcode']
        dept = request.POST['department']
        designation = request.POST['designation']
        contact = request.POST['contact']
        jdate = request.POST['jdate']
        gender = request.POST['gender']

        employee.user.first_name = fn
        employee.user.last_name = ln
        employee.empcode = ec
        employee.empdept = dept
        employee.designation = designation
        employee.contact = contact
        employee.gender = gender

        if jdate:
            employee.joiningdate = jdate

        try:
            employee.save()
            employee.user.save()
            error = "no"
        except:
            error = "yes"


    return render(request,'edit_profile.html',locals())


def edit_education(request, pid):
    if not request.user.is_authenticated:
        return redirect('emp_login')
    error = ""
    user = User.objects.get(id=pid)
    education = EmployeeEducation.objects.get(user=user)
    if request.method == "POST":
        coursepg = request.POST['coursepg']
        schoolclgpg = request.POST['schoolclgpg']
        yearofpassingpg = request.POST['yearofpassingpg']
        percentagepg = request.POST['percentagepg']

        coursegra = request.POST['coursegra']
        schoolclggra = request.POST['schoolclggra']
        yearofpassinggra = request.POST['yearofpassinggra']
        percentagegra = request.POST['percentagegra']

        coursessc = request.POST['coursessc']
        schoolclgssc = request.POST['schoolclgssc']
        yearofpassingssc = request.POST['yearofpassingssc']
        percentagessc = request.POST['percentagessc']

        coursehsc = request.POST['coursehsc']
        schoolclghsc = request.POST['schoolclghsc']
        yearofpassinghsc = request.POST['yearofpassinghsc']
        percentagehsc = request.POST['percentagehsc']

        education.coursepg = coursepg
        education.schoolclgpg = schoolclgpg
        education.yearofpassingpg = yearofpassingpg
        education.percentagepg = percentagepg

        education.coursegra = coursegra
        education.schoolclggra = schoolclggra
        education.yearofpassinggra = yearofpassinggra
        education.percentagegra = percentagegra

        education.coursessc = coursessc
        education.schoolclgssc = schoolclgssc
        education.yearofpassingssc = yearofpassingssc
        education.percentagessc = percentagessc

        education.coursehsc = coursehsc
        education.schoolclghsc = schoolclghsc
        education.yearofpassinghsc = yearofpassinghsc
        education.percentagehsc = percentagehsc

        try:
            education.save()
            error = "no"
        except:
            error = "yes"


    return render(request,'edit_education.html',locals())

def edit_experience(request, pid):
    if not request.user.is_authenticated:
        return redirect('emp_login')
    error = ""
    user = User.objects.get(id=pid)
    experience = EmployeeExperience.objects.get(user=user)
    if request.method == "POST":
        company1name = request.POST['company1name']
        company1desig = request.POST['company1desig']
        company1salary = request.POST['company1salary']
        company1duration = request.POST['company1duration']

        company2name = request.POST['company2name']
        company2desig = request.POST['company2desig']
        company2salary = request.POST['company2salary']
        company2duration = request.POST['company2duration']

        company3name = request.POST['company3name']
        company3desig = request.POST['company3desig']
        company3salary = request.POST['company3salary']
        company3duration = request.POST['company3duration']

        experience.company1name = company1name
        experience.company1desig = company1desig
        experience.company1salary = company1salary
        experience.company1duration = company1duration

        experience.company2name = company2name
        experience.company2desig = company2desig
        experience.company2salary = company2salary
        experience.company2duration = company2duration

        experience.company3name = company3name
        experience.company3desig = company3desig
        experience.company3salary = company3salary
        experience.company3duration = company3duration



        try:
            experience.save()
            error = "no"
        except:
            error = "yes"


    return render(request,'edit_experience.html',locals())

def is_hr(user):
    return user.is_authenticated and user.role == 'HR'

@login_required
def hr_dashboard(request):
    if not is_hr(request.user):
        return HttpResponseForbidden("You are not authorized to access this page.")
    
    employees = CustomUser.objects.filter(role='Employee')
    return render(request, 'hr_dashboard.html', {'employees': employees})

@login_required
def manage_employee(request, employee_id=None):
    if not is_hr(request.user):
        return HttpResponseForbidden("You are not authorized to perform this action.")
    
    if request.method == 'POST':
        #Add or update employee logic
        name = request.POST['name']
        email = request.POST['email']
        role = request.POST['role']
        if employee_id:
            employee = CustomUser.objects.get(id=employee_id)
            employee.username = name
            employee.email = email
            employee.role = role
            employee.save()
        else:
            CustomUser.objects.create_user(username=name, email=email, password='password', role=role)
        return redirect('hr_dashboard')

    context = {}
    if employee_id:
        context['employee'] = CustomUser.objects.get(id=employee_id)

    return render(request, 'manage_employee.html', context)
        
def create_hr_user(username, email, password):
    user = CustomUser.objects.create_user(
        username=username,
        email=email,
        password=password,
        role='HR'
    )
    return user

def is_hr_user(user):
    return user.groups.filter(name = 'HR').exists() or user.is_superuser

pass

def employee_list(request):
    # Assuming you have a model 'Employee' in 'emp' app
    Employee = apps.get_model('emp', 'Employee')
    Department = apps.get_model('emp', 'Department')

    # Get all employees
    employees = Employee.objects.all()

    # Check if a specific department exists, and create it if it doesn't
    department_name = "Sales"
    department, created = Department.objects.get_or_create(name=department_name)

    if created:
        print(f"Created new department: {department_name}")

    # Render the employee list
    return render(request, 'employee_list.html', {'employees': employees, 'department': department})

class ExampleModel(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
User = get_user_model()

def user_list_view(request):
    users = User.objects.all()  # Query all users
    return render(request, 'user_list.html', {'users': users})

def request_leave(request):
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('leave_requests')
    else:
        form = LeaveRequestForm()
    return render(request, 'request_leave.html', {'form': form})

def leave_requests(request):
    leave_requests = LeaveRequest.objects.all()
    return render(request, 'leave_requests.html', {'leave_requests': leave_requests})

def user_list(request):
    users = CustomUser .objects.all()
    return render(request, 'user_list.html', {'users': users})

def leave_request_view(request):
    if request.method == 'POST':
        # Instantiate the CustomForm with POST data
        form = CustomForm(request.POST)
        pass
        # Check if the nested LeaveRequestForm is valid
        if form.is_valid() and form.leave_request.is_valid():
            # Save the LeaveRequest instance
            leave_request = form.leave_request.save(commit=False)
            # You can set additional fields on leave_request here if needed
            leave_request.save()  # Save the LeaveRequest instance
            
            # Redirect to a success page or another view
            return redirect('success_url')  # Replace with your success URL
            
    else:
        # If GET request, instantiate an empty form
        form = CustomForm()

    return render(request, 'your_template.html', {'form': form})

def my_view(request):
    from .models import LeaveRequest
    user_count = get_user_count()
    if request.method == 'POST':
        form = CustomForm(request.POST)
        if form.is_valid():
            leave_request = form.leave_request.save(commit=False)
            # Additional processing if needed
            leave_request.save()
            return redirect('success_url') # Redirect after successful submission
        else:
            form = CustomForm()
        return render(request, 'template.html', {'user_count': user_count})
    
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, 'Account created successfully!')
        return redirect('login')
    else:
        print(form.errors)  # Debugging line to see what errors are present
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, error)

def login_view(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)  # Log the user in
                return redirect('home')  # Redirect to home or dashboard
            else:
                form.add_error(None, "Invalid email or password.")  # Add a non-field error
    else:
        form = SignInForm()
    return render(request, 'login.html', {'form': form})

def employee_records(request):
    if request.method == 'POST':
        # Handle form submission
        name = request.POST.get('name')
        email = request.POST.get('email')
        position = request.POST.get('position')
        department = request.POST.get('department')
        Employee.objects.create(name=name, email=email, position=position, department=department)

    employees = Employee.objects.all()
    return render(request, 'employee_records.html', {'employees': employees})

def register_employee(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        empcode = request.POST.get('empcode')
        email = request.POST.get('email')
        password = request.POST.get('pwd')
        confirm_password = request.POST.get('cpwd')

        # Validation
        if password != confirm_password:
            messages.error(request, _("Passwords do not match."))
            return redirect('register_employee')

        try:
            user = User.objects.create_user(username=email, email=email, password=password)
            user.first_name = firstname
            user.last_name = lastname
            user.save()

            # Save additional employee details
            employee = Employee(user=user, empcode=empcode)
            employee.save()

            messages.success(request, _("Registration successful!"))
            return redirect('login')  # Redirect to login or any other page
        except ValidationError as e:
            messages.error(request, e.messages)
        except Exception as e:
            messages.error(request, _("An error occurred during registration."))

    return render(request, 'registration/register.html')