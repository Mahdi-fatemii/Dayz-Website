"""
URL configuration for dayz_website project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls import include
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from user.views import *
from django.urls import path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('signin/', SigninView.as_view(), name='signin'),
    path('logout/', login_required(LogoutView.as_view(), login_url='/'), name='logout'),
    path(r'^', include(('social_django.urls', 'social'), namespace='social')),
    path('', IndexView.as_view(), name='index'),
    path('vipshop/', vip_shop, name='vipshop'),
    path('request', request_payment, name='request_payment'),
    path('verify', verify_payment, name='verify_payment'),
    path('seccess', secces_payment_redirect, name='secces_payment_redirect'),
    path('unseccess', unseccess_payment_redirect, name='unsecces_payment_redirect')

]
