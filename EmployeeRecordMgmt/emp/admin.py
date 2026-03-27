from django.contrib import admin
from .models import CustomUser, Employee, YourModel, LeaveRequest, EmployeeDetail, EmployeeEducation, EmployeeExperience
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm, LeaveRequestForm, YourModelForm
from django.contrib.admin.sites import AlreadyRegistered

# Admin Model Classes
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser 
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone_number',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('phone_number',)}),
    )

class EmployeeExperienceAdmin(admin.ModelAdmin):
    list_display = ('user', 'company1_name', 'company1_designation', 'company1_salary', 'company1_duration', 'company2_name', 'company2_designation', 'company2_salary', 'company2_duration', 'company3_name', 'company3_designation', 'company3_salary', 'company3_duration')

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'department')
    search_fields = ('first_name', 'last_name', 'email', 'department')
    list_filter = ('department',)
    list_per_page = 20

@admin.register(YourModel)
class YourModelAdmin(admin.ModelAdmin):
    form = YourModelForm

@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    form = LeaveRequestForm

# Register remaining models
try:
    admin.site.register(Employee, EmployeeAdmin)
except AlreadyRegistered:
    pass

try:
    admin.site.register(EmployeeDetail)
except AlreadyRegistered:
    pass

try:
    admin.site.register(EmployeeEducation)
except AlreadyRegistered:
    pass

try:
    admin.site.register(EmployeeExperience, EmployeeExperienceAdmin)
except AlreadyRegistered:
    pass