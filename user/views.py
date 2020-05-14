import uuid

from django.conf import settings
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView

from blog.models import Post
from user.forms import LoginForm, RegisterForm, ForgotForm, PasswordForm, ChannelCreateForm
from user.models import User, Channel
from user.tasks import send_email


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"])
            if user is not None and user.is_confirmed != "NOT_CONFIRMED":
                login(request, user)
                return redirect(reverse('root'))
            else:
                return render(
                    request, "login.html",
                    {"form": form, "errors": ["Incorrect login or password or you need to confirm your account"]})
        else:
            return render(request, "login.html", {"form": form})
    else:
        if request.user.is_authenticated:
            return redirect(reverse('profile'))
        form = LoginForm()
        return render(request, "login.html", {"form": form})


@login_required(login_url=reverse_lazy('login'))
def logout_view(request):
    logout(request)
    return redirect(reverse("login"))


def confirm(request, code):
    success = False
    if request.method == "GET":
        try:
            user = User.objects.get(confirm_code=code)
            if user.is_confirmed == "NOT_CONFIRMED":
                user.is_confirmed = "CONFIRMED"
                user.save()
                success = True
        except User.DoesNotExist:
            success = False
        except ValidationError:
            success = False
        return render(request, "confirm-page.html", {"success": success})


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.create_user(
                form.cleaned_data["username"],
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"])
            user.profile_pic = form.cleaned_data["profile_pic"]
            user.save()
            send_email.delay("Confirm Email", settings.DEFAULT_FROM_EMAIL, user.email,
                             'mail.html', args=dict(code=user.confirm_code, name=user.first_name))
            return redirect(reverse("login"))
        else:
            return render(request, "register.html", {"form": form})
    else:
        return render(request, "register.html", {"form": RegisterForm()})


def forgot(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect(reverse('profile'))
        form = ForgotForm()
        return render(request, "forgot.html", {"form": form})
    elif request.method == "POST":
        form = ForgotForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(email=form.cleaned_data['email'])
                token = uuid.uuid4()
                user.confirm_code = token
                user.save()
                send_email.delay("Reset password", settings.DEFAULT_FROM_EMAIL, user.email,
                                 'mail-reset.html', args=dict(code=user.confirm_code, name=user.first_name))
            except User.DoesNotExist:
                return render(
                    request, "forgot.html",
                    {"form": form, "errors": ["This email is wrong"]})
            return render(request, "forgot_success.html", {})


def reset(request, code):
    success = False
    if request.method == "GET":
        try:
            user = User.objects.get(confirm_code=code)
            form = PasswordForm()
        except User.DoesNotExist:
            return redirect(reverse('root'))
        except ValidationError:
            return redirect(reverse('root'))
        return render(request, "reset.html", {"form": form, "code": code})
    elif request.method == "POST":
        form = PasswordForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(confirm_code=code)
                user.set_password(form.cleaned_data['password'])
                user.save()
                return redirect(reverse("login"))
            except User.DoesNotExist:
                pass
        else:
            render(request, "reset.html", {"form": form, "code": code})


@login_required(login_url=reverse_lazy('login'))
def profile_view(request):
    user = request.user
    return render(request, "profile.html", {"user": user,
                                            "followed_channels": user.channel_set.all()})


@login_required(login_url=reverse_lazy('login'))
def create(request):
    if request.method == "POST":
        form = ChannelCreateForm(request.POST)
        if form.is_valid():
            channel = Channel.objects.create(owner=request.user, name=form.cleaned_data['name'],
                                             description=form.cleaned_data['description'])
            return redirect(reverse("channel-detail", kwargs={"pk": channel.id}))
        else:
            return render(request, "channel_create.html", {"form": form, "errors": "Some data is wrong"})
    else:
        return render(request, "channel_create.html", {"form": ChannelCreateForm()})


class ChannelDetailView(DetailView):
    template_name = "channel.html"
    model = Channel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(author=super().get_object())
        return context



