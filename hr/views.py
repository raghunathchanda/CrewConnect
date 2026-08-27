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
    ).all()

    return render(request,"employee_list.html",
        {"employees": employees})


def employee_create():
    return None


def employee_update():
    return None


def employee_delete():
    return None