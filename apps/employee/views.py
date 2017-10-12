# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import json
import logging

from employee.account import Account
from common.http_response_customer import HttpResponseCustomer
from common.errcode import *

# Create your views here.
@csrf_exempt
def signin(request):
    if request.method == "POST":
        try:
            json_data = json.loads(request.body) #if not json data ,it will raise a except.
            phone = json_data["phone"]
            password = json_data["password"]
            storeid = json_data["storeid"]
            logging.debug("phone:%s password:%s storeid:%s " % (phone, password, storeid))
        except :
            return HttpResponseCustomer(errCode = FORMAT_ILLEGAL_CODE, reason = [FORMAT_ILLEGAL], data = {})

        if phone == "" or password == "" or storeid == "":
            return HttpResponseCustomer(errCode = FORMAT_ILLEGAL_CODE, reason = [FORMAT_ILLEGAL], data = {})

        try:
            account = Account.objects.get(phone = phone)
        except:
            return HttpResponseCustomer(errCode = ACCOUNT_INVALID_CODE, reason = [ACCOUNT_INVALID], data = {"token":""})
        else:
            if account.password != password:
                return HttpResponseCustomer(errCode = PASSWORD_INVALID_CODE, reason = [PASSWORD_INVALID], data = {"token":""})

            if account.storeid != storeid:
                return HttpResponseCustomer(errCode = STOREID_INVALID_CODE, reason = [STOREID_INVALID], data = {"token":""})

            if account.status != Account.ACCOUNT_ACTIVE:
                return HttpResponseCustomer(errCode = ACCOUNT_FORBIDDEN_CODE, reason = [ACCOUNT_FORBIDDEN], data = {"token":""})

        token = account.signin()
        response = HttpResponseCustomer(errCode = 0, reason = [], data = {"token":token})
        return response
    else:
        return HttpResponseCustomer(errCode = FORMAT_ILLEGAL_CODE, reason = [FORMAT_ILLEGAL], data = {"token":""})

@csrf_exempt
def exit(request):
    return HttpResponseCustomer(errCode = FORMAT_ILLEGAL_CODE, reason = [FORMAT_ILLEGAL], data = {"token":""})        
