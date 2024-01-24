from django.contrib.auth.views import auth_logout
from django.shortcuts import render, redirect
from django.views import View
from .models import *
import requests

import json
from django.conf import settings
import requests
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from datetime import datetime


# Create your views here.


if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'

ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"


phone = ''

CallbackURL = 'http://127.0.0.1:8000/verify'


class SigninView(View):
    def get(self, request):
        return render(request, 'signin.html')


class LogoutView(View):
    def get(self, request):
        auth_logout(request)
        return redirect('signin')


class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')


def payment_checker(user):
    try:
        cart = Payment.objects.get(user=user)
    except Payment.DoesNotExist:
        return False
    else:
        return True


def vip_shop(request):
    vip_all = Vip.objects.all()
    user = request.user
    if request.method == 'POST':
        pay_status = payment_checker(user=user)
        if pay_status is False:
            vip_level = request.POST.get('vipse')
            vip = Vip.objects.get(vip_name=vip_level)
            order_name = vip.vip_name
            amount = vip.vip_price
            description = vip.vip_description
            pay = Payment(price=amount, vip_name=order_name, description=description, user=user)
        else:
            vip_level = request.POST.get('vipse')
            vip = Vip.objects.get(vip_name=vip_level)
            pay = Payment.objects.get(user=user)
            pay.vip_name = vip.vip_name
            pay.price = vip.vip_price
            pay.description = vip.vip_description

        pay.save()
        return redirect(reverse('request_payment'))
    return render(request, 'shop.html', {'vip_all': vip_all})


def request_payment(request):
    user = request.user

    pay = Payment.objects.get(user=user)

    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": pay.price,
        "Description": pay.description,
        "Phone": phone,
        "CallbackURL": CallbackURL,
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    try:
        response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)

        if response.status_code == 200:
            response = response.json()
            if response['Status'] == 100:
                url = f"{ZP_API_STARTPAY}{response['Authority']}"
                return redirect(url)
            else:
                return {'status': False, 'code': str(response['Status'])}
        return HttpResponse(response)

    except requests.exceptions.Timeout:
        return {'status': False, 'code': 'timeout'}
    except requests.exceptions.ConnectionError:
        return {'status': False, 'code': 'connection error'}


def verify_payment(request):
    authority = request.GET['Authority']
    user = request.user

    pay = Payment.objects.get(user=user)

    total_price = pay.price

    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": total_price,
        'Authority': authority,

    }
    data = json.dumps(data)
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}

    res = requests.post(ZP_API_VERIFY, data=data, headers=headers)
    if res.status_code == 200:
        response = res.json()

        if response['Status'] == 100:
            pay.status = 'Purchased'
            vip_level = VipLevel(vip_level=pay.vip_name, user=user)
            vip_level.save()
            pay.save()
            return redirect(reverse('secces_payment_redirect'))

    return redirect(reverse('unsecces_payment_redirect'))


def secces_payment_redirect(request):
    return render(request, "seccess_payment.html", context={})


def unseccess_payment_redirect(request):
    return render(request, "unseccess_payment.html", context={})