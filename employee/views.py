from django.shortcuts import render, redirect

# Create your views here.
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.contrib import messages

User = get_user_model()


def set_password(request, uidb64, token):

    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is None or not default_token_generator.check_token(user, token):
        return render(request, "invalid_link.html")

    if request.method == "POST":

        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect(
                "set_password",
                uidb64=uidb64,
                token=token
            )

        user.set_password(password)
        user.save()

        messages.success(
            request,
            "Password created successfully. You can now login."
        )

        return redirect("login")

    return render(request, "set_password.html")

from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def employee_dashboard(request):

    employee = request.user.employee

    return render(
        request,
        "employee_dashboard.html",
        {
            "employee": employee
        }
    )