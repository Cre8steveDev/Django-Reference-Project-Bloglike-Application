from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .email import send_welcome_email
from .forms import LoginForm, ProfileForm, RegistrationForm


def login_user(request):
    if request.user.is_authenticated:
        return redirect("profile")

    form = LoginForm(request.POST or None)
    next_page = request.POST.get("next") or request.GET.get("next") or "profile"

    if request.method == "POST" and form.is_valid():
        user = authenticate(
            request,
            username=form.cleaned_data["email"],
            password=form.cleaned_data["password"],
        )
        if user is not None:
            auth_login(request, user)
            messages.success(request, "Welcome back.")
            return redirect(next_page)

        form.add_error(None, "Please check your email and password and try again.")

    return render(request, "auth/login.html", {"form": form, "next_page": next_page})


def register_user(request):
    if request.user.is_authenticated:
        return redirect("profile")

    form = RegistrationForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid():
        user = form.save()
        send_welcome_email(user)
        auth_login(request, user)
        messages.success(request, "Your account has been created.")
        return redirect("profile")

    return render(request, "auth/register.html", {"form": form})


def logout_user(request):
    auth_logout(request)
    messages.info(request, "You have been signed out.")
    return redirect("home")


@login_required(login_url="login")
def user_profile(request):
    posts = request.user.posts.select_related("author")
    form = ProfileForm(request.POST or None, request.FILES or None, instance=request.user)
    profile_fields = [
        request.user.username,
        request.user.email,
        request.user.name,
        request.user.birthday,
        request.user.location,
        request.user.bio,
        request.user.avatar,
        request.user.gender,
        request.user.portfolio_url,
    ]
    filled_fields = sum(1 for value in profile_fields if value)
    profile_completion = round((filled_fields / len(profile_fields)) * 100) if profile_fields else 0

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Your profile has been updated.")
        return redirect("profile")

    return render(
        request,
        "auth/profile.html",
        {
            "form": form,
            "posts": posts,
            "profile_completion": profile_completion,
        },
    )
