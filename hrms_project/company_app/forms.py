from django import forms
from .models import Company, User
from .models import SalaryInfo, JobType
from .models import WorkShift
from .models import Project
from .models import BankDetails

class CompanyRegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Company
        fields = ['name', 'username', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

class UserRegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['name', 'username', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class CompanyLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

#salary

class SalaryInfoForm(forms.ModelForm):
    class Meta:
        model = SalaryInfo
        fields = ['user', 'job_type', 'salary_amount']

    user = forms.ModelChoiceField(queryset=User.objects.all(), label="Select User")
    job_type = forms.ModelChoiceField(queryset=JobType.objects.all(), label="Select Job Type")
    salary_amount = forms.DecimalField(max_digits=10, decimal_places=2, label="Salary Amount")
    

 # work shift
class WorkShiftForm(forms.ModelForm):
    class Meta:
        model = WorkShift
        fields = ['user', 'shift_type', 'total_work_time']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'shift_type': forms.Select(attrs={'class': 'form-control'}),
            'total_work_time': forms.NumberInput(attrs={'class': 'form-control'}),
        }
   
#leave

from .models import Leave

class LeaveApplicationForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = ['date', 'reason']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class LeaveApprovalForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = ['status']
        widgets = {
            'status': forms.Select(),
        }

#project master
class ProjectForm(forms.ModelForm):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d']
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d']
    )

    class Meta:
        model = Project
        fields = ['project_name', 'assigned_user', 'start_date', 'end_date', 'status']

class UpdateProjectStatusForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['status']

#bank master

class BankDetailsForm(forms.ModelForm):
    class Meta:
        model = BankDetails
        fields = ['bank_name', 'account_number', 'ifsc_code', 'micr_code', 'account_holder_name', 'branch_address']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and not self.instance.is_editable:
            for field in self.fields:
                self.fields[field].widget.attrs['readonly'] = True

class BankEditRequestForm(forms.Form):
    reason = forms.CharField(widget=forms.Textarea, required=True)