from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from .models import Company, User
from django.contrib.auth.decorators import login_required
from .forms import SalaryInfoForm
from .models import SalaryInfo
from .models import WorkShift
from .forms import WorkShiftForm
from .models import Leave
from .forms import LeaveApplicationForm, LeaveApprovalForm
from .models import Attendance
from .models import Project
from .forms import ProjectForm, UpdateProjectStatusForm
from django.contrib import messages
from .models import BankDetails, BankEditRequest
from .forms import BankDetailsForm, BankEditRequestForm
from datetime import timedelta
from django.utils import timezone
from .forms import CompanyRegistrationForm, UserRegistrationForm, UserLoginForm, CompanyLoginForm
from django.contrib.auth import logout as auth_logout

#landing page
def landing_page(request):
    return render(request, 'landing_page.html')

def logout_view(request):
    """Handles user logout and redirects to the landing page."""
    auth_logout(request)  # Log out the user
    return redirect('landing_page') 

def company_register(request):
    if request.method == 'POST':
        form = CompanyRegistrationForm(request.POST)
        if form.is_valid():
            company = form.save(commit=False)
            company.password = form.cleaned_data['password']
            company.save()
            return redirect('company_login')
    else:
        form = CompanyRegistrationForm()
    return render(request, 'company_app/company_register.html', {'form': form})


def company_login(request):
    if request.method == 'POST':
        form = CompanyLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                company = Company.objects.get(username=username, password=password)
                request.session['company_id'] = company.id  # Store company in session
                return redirect('user_list')
            except Company.DoesNotExist:
                form.add_error(None, "Invalid login credentials")
    else:
        form = CompanyLoginForm()
    return render(request, 'company_app/company_login.html', {'form': form})

def user_register(request):
    if 'company_id' not in request.session:
        return redirect('company_login')  # Redirect to login if no company is logged in

    company = Company.objects.get(id=request.session['company_id'])

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.company = company
            user.save()
            return redirect('user_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'company_app/user_register.html', {'form': form})

def user_list(request):
    if 'company_id' not in request.session:
        return redirect('company_login')
        
    company = Company.objects.get(id=request.session['company_id'])
    users = User.objects.filter(company=company)
    return render(request, 'company_app/user_list.html', {'users': users})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                auth_login(request, user)
                return redirect('user_dashboard')
    else:
        form = UserLoginForm()
    return render(request, 'company_app/login.html', {'form': form})


#salary - user
@login_required
def user_dashboard(request):
    return render(request, 'user_dashboard.html')

@login_required
def user_work_shift(request):
    user = request.user
    work_shifts = WorkShift.objects.filter(user=user)

    context = {
        'work_shifts': work_shifts
    }
    return render(request, 'user_work_shift.html', context)

#salary - company

def salary_list(request):
    salaries = SalaryInfo.objects.all()
    return render(request, 'salary_list.html', {'salaries': salaries})

def salary_create(request):
    if request.method == 'POST':
        form = SalaryInfoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('salary_list')
    else:
        form = SalaryInfoForm()
    return render(request, 'salary_form.html', {'form': form})

def salary_update(request, pk):
    salary = get_object_or_404(SalaryInfo, pk=pk)
    if request.method == 'POST':
        form = SalaryInfoForm(request.POST, instance=salary)
        if form.is_valid():
            form.save()
            return redirect('salary_list')
    else:
        form = SalaryInfoForm(instance=salary)
    return render(request, 'salary_form.html', {'form': form})

def salary_delete(request, pk):
    salary = get_object_or_404(SalaryInfo, pk=pk)
    if request.method == 'POST':
        salary.delete()
        return redirect('salary_list')
    return render(request, 'salary_confirm_delete.html', {'salary': salary})


# work shift 

def work_shift_list(request):
    shifts = WorkShift.objects.all()
    return render(request, 'work_shift_list.html', {'shifts': shifts})

def add_work_shift(request):
    if request.method == 'POST':
        form = WorkShiftForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('work_shift_list')
    else:
        form = WorkShiftForm()
    return render(request, 'work_shift_form.html', {'form': form})

def edit_work_shift(request, shift_id):
    shift = get_object_or_404(WorkShift, id=shift_id)
    if request.method == 'POST':
        form = WorkShiftForm(request.POST, instance=shift)
        if form.is_valid():
            form.save()
            return redirect('work_shift_list')
    else:
        form = WorkShiftForm(instance=shift)
    return render(request, 'work_shift_form.html', {'form': form})


def delete_work_shift(request, shift_id):
    shift = get_object_or_404(WorkShift, id=shift_id)
    if request.method == 'POST':
        shift.delete()
        return redirect('work_shift_list')
    return render(request, 'work_shift_confirm_delete.html', {'shift': shift})


#leaves
def apply_leave(request):
    if request.method == 'POST':
        form = LeaveApplicationForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.user = request.user
            leave.save()
            return redirect('user_leave_status')
    else:
        form = LeaveApplicationForm()
    return render(request, 'apply_leave.html', {'form': form})


def user_leave_status(request):
    leaves = Leave.objects.filter(user=request.user)
    return render(request, 'user_leave_status.html', {'leaves': leaves})


def manage_leaves(request):
    leaves = Leave.objects.all()
    return render(request, 'manage_leaves.html', {'leaves': leaves})


def approve_or_deny_leave(request, leave_id):
    leave = get_object_or_404(Leave, id=leave_id)
    if request.method == 'POST':
        form = LeaveApprovalForm(request.POST, instance=leave)
        if form.is_valid():
            form.save()
            return redirect('manage_leaves')
    else:
        form = LeaveApprovalForm(instance=leave)
    return render(request, 'approve_or_deny_leave.html', {'form': form, 'leave': leave})

#attendance


def check_in(request):
    user = request.user
    today = timezone.now().date()

    # Check if user has already checked in today
    attendance, created = Attendance.objects.get_or_create(user=user, date=today)
    if created or attendance.check_in_time is None:
        attendance.check_in_time = timezone.now().time()
        attendance.save()
    return redirect('user_attendance')


def check_out(request):
    user = request.user
    today = timezone.now().date()

    # Check if user has already checked in today and has not checked out yet
    try:
        attendance = Attendance.objects.get(user=user, date=today, check_in_time__isnull=False, check_out_time__isnull=True)
        attendance.check_out_time = timezone.now().time()

        # Calculate total hours
        check_in_datetime = timezone.make_aware(timezone.datetime.combine(today, attendance.check_in_time))
        check_out_datetime = timezone.make_aware(timezone.datetime.combine(today, attendance.check_out_time))
        attendance.total_hours = check_out_datetime - check_in_datetime
        attendance.save()
    except Attendance.DoesNotExist:
        pass

    return redirect('user_attendance')

def user_attendance(request):
    attendances = Attendance.objects.filter(user=request.user)
    return render(request, 'user_attendance.html', {'attendances': attendances})


def manage_attendance(request):
    attendances = Attendance.objects.all()
    return render(request, 'manage_attendance.html', {'attendances': attendances})


#project master

def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_projects')
    else:
        form = ProjectForm()
    return render(request, 'create_project.html', {'form': form})


def update_project_status(request, project_id):
    project = get_object_or_404(Project, id=project_id, assigned_user=request.user)
    if request.method == 'POST':
        form = UpdateProjectStatusForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('user_projects')
    else:
        form = UpdateProjectStatusForm(instance=project)
    return render(request, 'update_project_status.html', {'form': form, 'project': project})


def manage_projects(request):
    projects = Project.objects.all()
    return render(request, 'manage_projects.html', {'projects': projects})


def user_projects(request):
    projects = Project.objects.filter(assigned_user=request.user)
    return render(request, 'user_projects.html', {'projects': projects})


#bank master


@login_required
def add_or_edit_bank_details(request):
    bank_details, created = BankDetails.objects.get_or_create(user=request.user)

    if not created and not bank_details.is_editable:
        if request.method == 'POST':
            form = BankEditRequestForm(request.POST)
            if form.is_valid():
                BankEditRequest.objects.create(user=request.user)
                messages.success(request, "Edit request submitted.")
                return redirect('bank_details')
        else:
            form = BankEditRequestForm()
        return render(request, 'bank_details/request_edit.html', {'form': form})

    if request.method == 'POST':
        form = BankDetailsForm(request.POST, instance=bank_details)
        if form.is_valid():
            bank_details.is_editable = False
            form.save()
            messages.success(request, "Bank details saved.")
            return redirect('bank_details')
    else:
        form = BankDetailsForm(instance=bank_details)

    return render(request, 'bank_details/add_or_edit.html', {'form': form})

@login_required
def view_bank_details(request):
    bank_details = BankDetails.objects.filter(user=request.user)
    return render(request, 'bank_details/view.html', {'bank_details': bank_details})

@login_required
def approve_edit_request(request, request_id):
    if request.user.is_staff:
        edit_request = get_object_or_404(BankEditRequest, id=request_id, is_approved=False)
        bank_details = edit_request.user.bank_details
        bank_details.is_editable = True
        bank_details.save()
        edit_request.is_approved = True
        edit_request.save()
        messages.success(request, f"Edit request approved for {edit_request.user.name}.")
    return redirect('company_view_bank_requests')

@login_required
def company_view_bank_requests(request):
    edit_requests = BankEditRequest.objects.filter(is_approved=False)
    return render(request, 'bank_details/company_view_requests.html', {'edit_requests': edit_requests})

@login_required
def company_view_bank_details(request):
    bank_details = BankDetails.objects.all()
    return render(request, 'bank_details/company_view.html', {'bank_details': bank_details})