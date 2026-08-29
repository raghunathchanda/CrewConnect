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
    path(
    "profile/",
    views.employee_profile,
    name="employee_profile"
),
path(
    "leave/apply/",
    views.apply_leave,
    name="apply_leave"
),
path(
    "leave/my/",
    views.my_leaves,
    name="my_leaves"
),

]