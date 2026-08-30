from decimal import Decimal

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Sum, Count, ProtectedError
from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.decorators.cache import never_cache


from hr.models import Employee, Leave, Payslip


def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request, user)
            if Employee.objects.filter(user=user).exists():
                print("enter----------1")
                return redirect("employee_dashboard")
            print("enter----------2")
            return redirect("dashboard")
        return render(request,"login.html",{"error": "Invalid username or password"})
    return render(request, "login.html")





@login_required
@never_cache
def dashboard(request):
    return render(request, "dashboard.html")


def logout_view(request):
    logout(request)
    return redirect("login")


# def viewemployees(request):
#     return render(request, "view_employees.html")

def employee_list(request):

    employees = Employee.objects.select_related(
        "department",
        "designation"
    ).filter(
        status=True
    )

    return render(
        request,
        "employee_list.html",
        {
            "employees": employees
        }
    )


from django.shortcuts import render, redirect, get_object_or_404

from .models import Employee, Department, Designation


# def employee_create(request):
#
#     departments = Department.objects.all()
#     designations = Designation.objects.all()
#
#     if request.method == "POST":
#
#         employee_id = request.POST.get("employee_id")
#         name = request.POST.get("name")
#         email = request.POST.get("email")
#         phone = request.POST.get("phone")
#
#         department_id = request.POST.get("department")
#         designation_id = request.POST.get("designation")
#
#         joining_date = request.POST.get("joining_date")
#         employment_type = request.POST.get("employment_type")
#         salary = request.POST.get("salary")
#         address = request.POST.get("address")
#
#         status = request.POST.get("status") == "on"
#
#         Employee.objects.create(
#             employee_id=employee_id,
#             name=name,
#             email=email,
#             phone=phone,
#             department_id=department_id,
#             designation_id=designation_id,
#             joining_date=joining_date,
#             employment_type=employment_type,
#             salary=salary,
#             address=address,
#             status=status
#         )
#
#         return redirect("employee_list")
#
#     return render(
#         request,
#         "employee_add_update.html",
#         {
#             "departments": departments,
#             "designations": designations,
#             "employment_types": Employee.EMPLOYMENT_TYPES,
#             "is_update": False,
#         }
#     )

def employee_create(request):

    departments = Department.objects.all()
    designations = Designation.objects.all()

    if request.method == "POST":

        employee_id = request.POST.get("employee_id")
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")

        department_id = request.POST.get("department")
        designation_id = request.POST.get("designation")

        joining_date = request.POST.get("joining_date")
        employment_type = request.POST.get("employment_type")
        salary = request.POST.get("salary")
        address = request.POST.get("address")

        status = request.POST.get("status") == "on"
        if Employee.objects.filter(email=email).exists():
            messages.error(
                request,
                "Employee with this email already exists."
            )
            return redirect("employee_create")

        # Create Django User
        user = User.objects.create_user(
            username=email,
            email=email,
            first_name=name
        )

        # Disable password until employee creates one
        user.set_unusable_password()
        user.save()

        # Create Employee
        employee = Employee.objects.create(
            user=user,
            employee_id=employee_id,
            name=name,
            email=email,
            phone=phone,
            department_id=department_id,
            designation_id=designation_id,
            joining_date=joining_date,
            employment_type=employment_type,
            salary=salary,
            address=address,
            status=status
        )

        # Generate password setup token
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        # Password setup URL
        setup_link = request.build_absolute_uri(
            reverse(
                "set_password",
                kwargs={
                    "uidb64": uid,
                    "token": token
                }
            )
        )

        # Send email
        send_mail(
            subject="CrewConnect - Set Your Password",
            message=f"""
Hello {name},

Your CrewConnect employee account has been created.

Please click the link below to create your password:

{setup_link}

After setting your password, you can log in to CrewConnect.

Regards,
CrewConnect HR
""",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
        )

        return redirect("employee_list")

    return render(
        request,
        "employee_add_update.html",
        {
            "departments": departments,
            "designations": designations,
            "employment_types": Employee.EMPLOYMENT_TYPES,
            "is_update": False,
        }
    )

def employee_update(request, id):

    employee = get_object_or_404(
        Employee,
        id=id
    )

    departments = Department.objects.all()
    designations = Designation.objects.all()

    if request.method == "POST":

        employee.employee_id = request.POST.get("employee_id")
        employee.name = request.POST.get("name")
        employee.email = request.POST.get("email")
        employee.phone = request.POST.get("phone")

        employee.department_id = request.POST.get("department")
        employee.designation_id = request.POST.get("designation")

        employee.joining_date = request.POST.get("joining_date")
        employee.employment_type = request.POST.get("employment_type")
        employee.salary = request.POST.get("salary")
        employee.address = request.POST.get("address")

        employee.status = request.POST.get("status") == "on"

        employee.save()

        return redirect(
            "employee_list"
        )

    return render(
        request,
        "employee_add_update.html",
        {
            "employee": employee,
            "departments": departments,
            "designations": designations,
            "employment_types": Employee.EMPLOYMENT_TYPES,
            "is_update": True,
        }
    )


def employee_delete(request, id):
    employee = get_object_or_404(
        Employee,
        id=id
    )
    employee.status = not employee.status
    employee.save()
    return redirect("employee_list")


@login_required
def leave_approval(request):

    # Check whether logged-in user is an employee
    if Employee.objects.filter(user=request.user).exists():
        return redirect("employee_dashboard")

    leaves = Leave.objects.select_related(
        "employee",
        "employee__department",
        "employee__designation"
    ).order_by("-applied_date")

    return render(
        request,
        "leave_approval.html",
        {
            "leaves": leaves,
            "is_employee": False,
        }
    )


@login_required
def leave_action(request, id):

    # Employee cannot approve/reject
    if Employee.objects.filter(user=request.user).exists():
        return redirect("employee_dashboard")

    if request.method == "POST":

        leave = Leave.objects.get(id=id)

        action = request.POST.get("action")

        if action == "approve":

            leave.status = "Approved"
            leave.save()

        elif action == "reject":

            leave.status = "Rejected"
            leave.save()

    return redirect("leave_approval")

@login_required
def payroll(request):

    # Employee should not access HR payroll
    if Employee.objects.filter(user=request.user).exists():
        return redirect("employee_dashboard")

    employees = Employee.objects.filter(status=True)

    payslips = Payslip.objects.select_related(
        "employee"
    ).order_by("-year", "-month")

    return render(
        request,
        "payroll.html",
        {
            "employees": employees,
            "payslips": payslips,
        }
    )

@login_required
def generate_payslip(request):

    # Employee should not access HR payroll
    if Employee.objects.filter(user=request.user).exists():
        return redirect("employee_dashboard")

    if request.method == "POST":

        employee_id = request.POST.get("employee")
        month = request.POST.get("month")
        year = request.POST.get("year")
        allowances = request.POST.get("allowances") or 0
        deductions = request.POST.get("deductions") or 0

        employee = Employee.objects.get(
            id=employee_id
        )

        basic_salary = employee.salary

        allowances = Decimal(allowances)
        deductions = Decimal(deductions)

        net_salary = (
            basic_salary
            + allowances
            - deductions
        )

        Payslip.objects.create(
            employee=employee,
            month=month,
            year=year,
            basic_salary=basic_salary,
            allowances=allowances,
            deductions=deductions,
            net_salary=net_salary,
        )

        return redirect("payroll")

    return redirect("payroll")


# @login_required
# def reports(request):
#
#     # Employee should not access HR reports
#     if Employee.objects.filter(user=request.user).exists():
#         return redirect("employee_dashboard")
#
#     # Employee counts
#     total_employees = Employee.objects.count()
#
#     active_employees = Employee.objects.filter(
#         status=True
#     ).count()
#
#     inactive_employees = Employee.objects.filter(
#         status=False
#     ).count()
#
#
#     # Leave counts
#     total_leaves = Leave.objects.count()
#
#     pending_leaves = Leave.objects.filter(
#         status="Pending"
#     ).count()
#
#     approved_leaves = Leave.objects.filter(
#         status="Approved"
#     ).count()
#
#     rejected_leaves = Leave.objects.filter(
#         status="Rejected"
#     ).count()
#
#
#     # Payroll
#     total_payslips = Payslip.objects.count()
#
#     total_salary = Payslip.objects.aggregate(
#         total=Sum("net_salary")
#     )["total"] or 0
#
#
#     context = {
#         "total_employees": total_employees,
#         "active_employees": active_employees,
#         "inactive_employees": inactive_employees,
#
#         "total_leaves": total_leaves,
#         "pending_leaves": pending_leaves,
#         "approved_leaves": approved_leaves,
#         "rejected_leaves": rejected_leaves,
#
#         "total_payslips": total_payslips,
#         "total_salary": total_salary,
#     }
#
#     return render(
#         request,
#         "reports.html",
#         context
#     )

@login_required
def reports(request):

    # Employee should not access HR reports
    if Employee.objects.filter(user=request.user).exists():
        return redirect("employee_dashboard")

    # Default month/year
    month = request.GET.get("month", "8")
    year = request.GET.get("year", "2026")

    month = int(month)
    year = int(year)

    # -----------------------------
    # Employee Summary
    # -----------------------------

    total_employees = Employee.objects.count()

    active_employees = Employee.objects.filter(
        status=True
    ).count()

    inactive_employees = Employee.objects.filter(
        status=False
    ).count()


    # -----------------------------
    # Leave Summary
    # -----------------------------

    # Leaves applied during selected month/year
    leaves = Leave.objects.filter(
        start_date__year=year,
        start_date__month=month
    )

    total_leaves = leaves.count()

    pending_leaves = leaves.filter(
        status="Pending"
    ).count()

    approved_leaves = leaves.filter(
        status="Approved"
    ).count()

    rejected_leaves = leaves.filter(
        status="Rejected"
    ).count()


    # -----------------------------
    # Payroll Summary
    # -----------------------------

    payslips = Payslip.objects.filter(
        month=month,
        year=year
    )

    total_payslips = payslips.count()

    payroll_summary = payslips.aggregate(
        total_basic_salary=Sum("basic_salary"),
        total_allowances=Sum("allowances"),
        total_deductions=Sum("deductions"),
        total_net_salary=Sum("net_salary"),
    )

    total_basic_salary = (
        payroll_summary["total_basic_salary"] or 0
    )

    total_allowances = (
        payroll_summary["total_allowances"] or 0
    )

    total_deductions = (
        payroll_summary["total_deductions"] or 0
    )

    total_net_salary = (
        payroll_summary["total_net_salary"] or 0
    )


    # -----------------------------
    # Employee-wise Leave Details
    # -----------------------------

    leave_details = leaves.select_related(
        "employee"
    ).order_by("-start_date")


    # -----------------------------
    # Employee-wise Payroll Details
    # -----------------------------

    payroll_details = payslips.select_related(
        "employee"
    ).order_by("employee__name")


    context = {

        # Selected period
        "selected_month": month,
        "selected_year": year,

        # Employees
        "total_employees": total_employees,
        "active_employees": active_employees,
        "inactive_employees": inactive_employees,

        # Leaves
        "total_leaves": total_leaves,
        "pending_leaves": pending_leaves,
        "approved_leaves": approved_leaves,
        "rejected_leaves": rejected_leaves,
        "leave_details": leave_details,

        # Payroll
        "total_payslips": total_payslips,
        "total_basic_salary": total_basic_salary,
        "total_allowances": total_allowances,
        "total_deductions": total_deductions,
        "total_net_salary": total_net_salary,
        "payroll_details": payroll_details,
    }

    return render(
        request,
        "reports.html",
        context
    )


@login_required
def department_list(request):

    if Employee.objects.filter(user=request.user).exists():
        return redirect("employee_dashboard")

    departments = Department.objects.all().order_by("name")

    return render(
        request,
        "department_list.html",
        {
            "departments": departments
        }
    )

@login_required
def department_create(request):

    if Employee.objects.filter(user=request.user).exists():
        return redirect("employee_dashboard")

    if request.method == "POST":

        name = request.POST.get("name")

        if name:

            Department.objects.create(
                name=name
            )

            return redirect("department_list")

    return render(
        request,
        "department_form.html"
    )

@login_required
def department_update(request, id):

    if Employee.objects.filter(user=request.user).exists():
        return redirect("employee_dashboard")

    department = Department.objects.get(id=id)

    if request.method == "POST":

        name = request.POST.get("name")

        if name:

            department.name = name
            department.save()

            return redirect("department_list")

    return render(
        request,
        "department_form.html",
        {
            "department": department
        }
    )

@login_required
def department_delete(request, id):

    if Employee.objects.filter(user=request.user).exists():
        return redirect("employee_dashboard")

    department = Department.objects.get(id=id)

    if request.method == "POST":

        try:

            department.delete()

        except ProtectedError:

            return render(
                request,
                "department_list.html",
                {
                    "departments": Department.objects.all(),
                    "error": "This department cannot be deleted because employees are assigned to it."
                }
            )

        return redirect("department_list")

    return render(
        request,
        "department_confirm_delete.html",
        {
            "department": department
        }
    )

@login_required
def designation_list(request):

    if Employee.objects.filter(user=request.user).exists():
        return redirect("employee_dashboard")

    designations = Designation.objects.all().order_by("name")

    return render(
        request,
        "designation_list.html",
        {
            "designations": designations
        }
    )

@login_required
def designation_create(request):

    if Employee.objects.filter(user=request.user).exists():
        return redirect("employee_dashboard")

    if request.method == "POST":

        name = request.POST.get("name")

        if name:

            Designation.objects.create(
                name=name
            )

            return redirect("designation_list")

    return render(
        request,
        "designation_form.html"
    )

@login_required
def designation_update(request, id):

    if Employee.objects.filter(user=request.user).exists():
        return redirect("employee_dashboard")

    designation = Designation.objects.get(id=id)

    if request.method == "POST":

        name = request.POST.get("name")

        if name:

            designation.name = name
            designation.save()

            return redirect("designation_list")

    return render(
        request,
        "designation_form.html",
        {
            "designation": designation
        }
    )

@login_required
def designation_delete(request, id):

    if Employee.objects.filter(user=request.user).exists():
        return redirect("employee_dashboard")

    designation = Designation.objects.get(id=id)

    if request.method == "POST":

        try:

            designation.delete()

        except ProtectedError:

            return render(
                request,
                "designation_list.html",
                {
                    "designations": Designation.objects.all(),
                    "error": "This designation cannot be deleted because employees are assigned to it."
                }
            )

        return redirect("designation_list")

    return render(
        request,
        "designation_confirm_delete.html",
        {
            "designation": designation
        }
    )