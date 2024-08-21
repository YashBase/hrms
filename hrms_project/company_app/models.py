from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError("Users must have a username")
        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None):
        user = self.create_user(username=username, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class Company(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class User(AbstractBaseUser):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="users")
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)

    objects = UserManager()

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.name


#salary
class JobType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class SalaryInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_type = models.ForeignKey(JobType, on_delete=models.SET_NULL, null=True)
    salary_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user.username} - {self.job_type.name} - ${self.salary_amount}"
    
# work shift    

class WorkShift(models.Model):
    DAY_SHIFT = 'Day Shift'
    NIGHT_SHIFT = 'Night Shift'
    EVENING_SHIFT = 'Evening Shift'

    SHIFT_CHOICES = [
        (DAY_SHIFT, 'Day Shift'),
        (NIGHT_SHIFT, 'Night Shift'),
        (EVENING_SHIFT, 'Evening Shift'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shift_type = models.CharField(max_length=20, choices=SHIFT_CHOICES)
    total_work_time = models.DecimalField(max_digits=5, decimal_places=2)  # E.g., 8.5 for 8 hours 30 minutes

    def __str__(self):
        return f'{self.user.username} - {self.shift_type}'
    

#leave 
from django.contrib.auth import get_user_model

User = get_user_model()

class Leave(models.Model):
    PENDING = 'Pending'
    APPROVED = 'Approved'
    DENIED = 'Denied'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (DENIED, 'Denied'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)

    def __str__(self):
        return f'{self.user.name} - {self.date} - {self.status}'
    

#attendance

class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    check_in_time = models.TimeField(null=True, blank=True)
    check_out_time = models.TimeField(null=True, blank=True)
    total_hours = models.DurationField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.name} - {self.date}"
    
#project master
class Project(models.Model):
    STATUS_CHOICES = [
        ('none', 'None'),
        ('started', 'Started'),
        ('in-progress', 'In-Progress'),
        ('done', 'Done'),
    ]

    project_name = models.CharField(max_length=255)
    assigned_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projects")
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='none')

    def __str__(self):
        return self.project_name
    

#bank master

class BankDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='bank_details')
    bank_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=20)
    ifsc_code = models.CharField(max_length=11)
    micr_code = models.CharField(max_length=9)
    account_holder_name = models.CharField(max_length=255)
    branch_address = models.TextField()
    is_editable = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.name}'s Bank Details"

class BankEditRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='edit_requests')
    requested_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Edit Request by {self.user.name} on {self.requested_at}"