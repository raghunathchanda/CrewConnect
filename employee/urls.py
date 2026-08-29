from django.urls import path


from employee import views

urlpatterns = [
    path(
        "set-password/<uidb64>/<token>/",
        views.set_password,
        name="set_password"
    ),
    path(
        "dashboard/",
        views.employee_dashboard,
        name="employee_dashboard"
    ),
]