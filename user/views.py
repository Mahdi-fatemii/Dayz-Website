from django.contrib.auth.views import auth_logout
from django.shortcuts import render, redirect
from django.views import View
# Create your views here.


class SigninView(View):
    def get(self, request):
        return render(request, 'signin.html')


class LogoutView(View):
    def get(self, request):
        auth_logout(request)
        return redirect('signin')