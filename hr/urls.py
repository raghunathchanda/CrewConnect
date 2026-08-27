from django.urls import path
from .views import (login_view, dashboard, logout_view,
                    employee_list,employee_create,employee_update,employee_delete)


urlpatterns = [
    path("", login_view, name="login"),
    path("dashboard/", dashboard, name="dashboard"),
    path("logout/", logout_view, name="logout"),
    # path("viewemployees/", viewemployees, name="viewemployees"),
    path("employees/", employee_list, name="employee_list"),
    # path("employees/add/", employee_create, name="employee_create"),
    # path("employees/<int:id>/edit/", employee_update, name="employee_update"),
    # path("employees/<int:id>/delete/", employee_delete, name="employee_delete"),
]