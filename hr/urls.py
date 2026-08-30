from django.urls import path

from . import views
from .views import (login_view, dashboard, logout_view,
                    employee_list,employee_create,employee_update,employee_delete)


urlpatterns = [
    path("", login_view, name="login"),
    path("dashboard/", dashboard, name="dashboard"),
    path("logout/", logout_view, name="logout"),
    # path("viewemployees/", viewemployees, name="viewemployees"),
    path("employees/", employee_list, name="employee_list"),
    path("employees/add/", employee_create, name="employee_create"),
    path("employees/<int:id>/edit/", employee_update, name="employee_update"),
    path("employees/<int:id>/delete/", employee_delete, name="employee_delete"),
    path("leave-approval/",views.leave_approval,name="leave_approval"),
    path("leave/<int:id>/action/",views.leave_action,name="leave_action"),
    path("payroll/",views.payroll,name="payroll"),
    path("payroll/generate/",views.generate_payslip,name="generate_payslip"),
path("reports/",views.reports,name="reports"),

path(
    "departments/",
    views.department_list,
    name="department_list"
),

path(
    "departments/add/",
    views.department_create,
    name="department_create"
),

path(
    "departments/<int:id>/edit/",
    views.department_update,
    name="department_update"
),

path(
    "departments/<int:id>/delete/",
    views.department_delete,
    name="department_delete"
),
path(
    "designations/",
    views.designation_list,
    name="designation_list"
),

path(
    "designations/add/",
    views.designation_create,
    name="designation_create"
),

path(
    "designations/<int:id>/edit/",
    views.designation_update,
    name="designation_update"
),

path(
    "designations/<int:id>/delete/",
    views.designation_delete,
    name="designation_delete"
),
]