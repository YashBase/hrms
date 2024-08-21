from django.urls import path
from . import views
from .views import apply_leave, user_leave_status, manage_leaves, approve_or_deny_leave
from .views import check_in, check_out, user_attendance, manage_attendance
from .views import create_project, update_project_status, manage_projects, user_projects
from .views import landing_page
from .views import logout_view

urlpatterns = [
    path('', landing_page, name='landing_page'),
    path('register/', views.company_register, name='company_register'),
    path('login/', views.company_login, name='company_login'),
    path('user/register/', views.user_register, name='user_register'),
    path('user/list/', views.user_list, name='user_list'),
    path('user/login/', views.user_login, name='user_login'),
    #salary
    path('salary/', views.salary_list, name='salary_list'),
    path('salary/create/', views.salary_create, name='salary_create'),
    path('salary/update/<int:pk>/', views.salary_update, name='salary_update'),
    path('salary/delete/<int:pk>/', views.salary_delete, name='salary_delete'),
    path('user/dashboard/', views.user_dashboard, name='user_dashboard'),
    #work shift
    path('work_shifts/', views.work_shift_list, name='work_shift_list'),
    path('work_shifts/add/', views.add_work_shift, name='add_work_shift'),
    path('work_shifts/edit/<int:shift_id>/', views.edit_work_shift, name='edit_work_shift'),
    path('work_shifts/delete/<int:shift_id>/', views.delete_work_shift, name='delete_work_shift'),
    path('user/work_shift/', views.user_work_shift, name='user_work_shift'),
    #leaves
    path('apply_leave/', apply_leave, name='apply_leave'),
    path('user/leave_status/', user_leave_status, name='user_leave_status'),
    path('manage_leaves/', manage_leaves, name='manage_leaves'),
    path('manage_leaves/<int:leave_id>/', approve_or_deny_leave, name='approve_or_deny_leave'),
    #attendance
    path('check_in/', check_in, name='check_in'),
    path('check_out/', check_out, name='check_out'),
    path('user/attendance/', user_attendance, name='user_attendance'),
    path('manage_attendance/', manage_attendance, name='manage_attendance'),
    #project master
    path('create_project/', create_project, name='create_project'),
    path('update_project_status/<int:project_id>/', update_project_status, name='update_project_status'),
    path('manage_projects/', manage_projects, name='manage_projects'),
    path('user_projects/', user_projects, name='user_projects'),
    #bank master
    path('bank-details/', views.add_or_edit_bank_details, name='bank_details'),
    path('view-bank-details/', views.view_bank_details, name='view_bank_details'),
    path('company-view-bank-details/', views.company_view_bank_details, name='company_view_bank_details'),
    path('company-view-requests/', views.company_view_bank_requests, name='company_view_bank_requests'),
    path('approve-request/<int:request_id>/', views.approve_edit_request, name='approve_edit_request'),
    path('logout/', logout_view, name='logout'),

]
