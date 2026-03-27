from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import authenticate
from .models import CustomUser , YourModel, LeaveRequest

# Custom User Creation Form
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser  
        fields = ('username', 'email', 'phone_number')  # Ensure 'phone_number' is a field in CustomUser 

# Custom User Change Form
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser  
        fields = ('username', 'email', 'phone_number', 'is_active')  # Ensure 'phone_number' is a field in CustomUser 


class YourModelForm(forms.ModelForm):
    class Meta:
        model = YourModel
        fields = ['name', 'email', 'description']  # Replace with actual fields

class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['employee', 'start_date', 'end_date', 'reason']

# Custom Form that includes LeaveRequestForm
class CustomForm(forms.Form):
    leave_request = LeaveRequestForm()

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

class SignInForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if email and password:
            user = authenticate(username=email, password=password)
            if user is None:
                raise forms.ValidationError("Invalid email or password.")