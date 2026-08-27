from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

from hr.models import Employee


def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request, user)
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

        Employee.objects.create(
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