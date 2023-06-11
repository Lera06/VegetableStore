from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm
from django.contrib.auth.models import User


#  Create your views here.


class LoginView(View):

    def get(self, request):
        return render(request, 'login/login.html')

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home:index')
        return render(request, 'login/login.html', {"error": form.errors.get("__all__")})


class LogoutView(View):
    def get(self, request):
        if request.user.is_authenticated:
           logout(request)
        return redirect('home:index')


class SignUpView(View):

    def get(self, request):
        return render(request, 'login/signup.html')

    def post(self, request):
        form = CustomUserCreationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home:index')
        return render(request, 'login/signup.html', {"errors": form.errors})




