from django.contrib.auth.views import auth_logout
from django.shortcuts import render, redirect
from django.views import View
from .models import *
import requests
from django.contrib.auth.decorators import login_required
import json
from django.conf import settings
import requests
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
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
        x = Payment.objects.get(user=user)
    except Payment.DoesNotExist:
        return False
    else:
        return True


def vip_level_checker(user):
    try:
        x = VipLevel.objects.get(user=user)
    except VipLevel.DoesNotExist:
        return False
    else:
        return True


@login_required
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
            pay.save()
        else:
            vip_level = request.POST.get('vipse')
            vip = Vip.objects.get(vip_name=vip_level)
            pay = Payment.objects.get(user=user)
            if pay.vip_name != 'Normal':
                pay.price = vip.vip_price - pay.price
                pay.vip_name = vip.vip_name
                pay.description = vip.vip_description
                if pay.price <= 0:
                    return render(request, 'shop.html', {'vip_all': vip_all})
                else:
                    pass
            elif pay.vip_name == 'Normal':
                pay.price = vip.price
                pay.vip_name = vip.vip_name
                pay.description = vip.vip_description
            else:
                return render(request, 'shop.html', {'vip_all': vip_all})
            pay.save()
        return redirect(reverse('request_payment'))
    return render(request, 'shop.html', {'vip_all': vip_all})


@login_required
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
        return HttpResponse(str(response))

    except requests.exceptions.Timeout:
        return {'status': False, 'code': 'timeout'}
    except requests.exceptions.ConnectionError:
        return {'status': False, 'code': 'connection error'}


@login_required
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
        check = vip_level_checker(user)
        if check is False:
            vip_level = VipLevel(vip_level='Normal', user=user)
            vip_level.save()
        pay.status = 'Failed'
        pay.save()

        if response['Status'] == 100:
            pay.status = 'Purchased'
            if pay.vip_name == 'Lieutenant':
                pay.price = 36000
            elif pay.vip_name == 'Sergeant':
                pay.price = 24000
            pay.save()
            check = vip_level_checker(user)
            if check is False:
                vip_level = VipLevel(vip_level=pay.vip_name, user=user)
                vip_level.save()
            else:
                vip_level_final = VipLevel.objects.get(user=user)
                vip_level_final.vip_level = pay.vip_name
                vip_level_final.save()
            return redirect(reverse('secces_payment_redirect'))

    return redirect(reverse('unsecces_payment_redirect'))


@login_required
def secces_payment_redirect(request):
    return render(request, "seccess_payment.html", context={})


@login_required
def unseccess_payment_redirect(request):
    return render(request, "unseccess_payment.html", context={})
