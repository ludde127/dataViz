from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, logout, login

from dataViz.utils import context_render
from users.forms import UserForm, LoginForm
from users.models import NormalUser, User
# Create your views here.


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            clean = form.cleaned_data
            user = authenticate(username=clean.get("username"), password=clean.get("password"))
            if user is not None:
                # Authenticated
                login(request, user)
                messages.success(request, "You are logged in.")
                return HttpResponseRedirect(reverse("index"))
            else:
                messages.error(request, "Incorrect credentials.")
    return context_render(request, 'users/login.html', context={"form": LoginForm()})


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "You have been logged out.")
    else:
        messages.error(request, "You are not logged in")
    return HttpResponseRedirect(reverse("login"))


def create_account(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in.")
    else:
        if request.method == "POST":
            form = UserForm(request.POST)
            if form.is_valid():
                if User.objects.filter(username=form.cleaned_data.get("username")).exists():
                    messages.error(request, "User already exists.")
                else:
                    form = form.cleaned_data
                    std_user = User.objects.create_user(username=form.get("username"), email=form.get("email"), password=form.get("password"))
                    new_user = NormalUser.objects.create(user=std_user)
                    new_user.save()
                    std_user.save()
                    messages.success(request, f"Successfully created user with username {std_user.username}")
                    login(request, std_user)
                    return HttpResponseRedirect(reverse("index"))
            else:
                messages.error(request, "Could not create account")

    return context_render(request, "users/create_account.html", context={"form": UserForm()})


def reset_password(request):
    return context_render(request, "users/reset_password.html")


