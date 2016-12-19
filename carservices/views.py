#!/usr/bin/env Python
# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from .models import *
from . import config
from django.shortcuts import render
from django.http import HttpResponse, QueryDict, HttpResponseRedirect, JsonResponse
from django.template import RequestContext, loader
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
import requests
import json
import time
import uuid
import exceptions
import os

# Create your views here.

@csrf_exempt
def sign_in(request):

    request_data = json.loads(request.body)
    CarMEID = request_data.get('id')
    PassWord = request_data.get('password')

    if len(CarMEID)!=0 and len(PassWord)!=0:
        try:
            carmeid = Account.objects.get(id=CarMEID)
            carmeid_password = carmeid.password

            if PassWord!=carmeid_password:
                carmeids = {'code': 1, 'result': {'errmsg': "Incorrect password."}}
                return JsonResponse(carmeids)

            else:
                carmeid_id = carmeid.id
                carmeid_token = carmeid.token
                carmeid_create_time = carmeid.create_time
                timestamp_carmeid_createtime = time.mktime(carmeid_create_time.timetuple())

                carmeids = {'code': 0, 'result': {'create_time': timestamp_carmeid_createtime, 'id': carmeid_id, 'token': carmeid_token}}
                return JsonResponse(carmeids)

        except ObjectDoesNotExist:
            carmeid = Account.objects.create(id=CarMEID, password=PassWord, token=str(uuid.uuid1()))

            carmeid_id = carmeid.id
            carmeid_token = carmeid.token
            carmeid_create_time = carmeid.create_time
            timestamp_carmeid_createtime = time.mktime(carmeid_create_time.timetuple())

            carmeids = {'code': 0, 'result': {'create_time': timestamp_carmeid_createtime, 'id': carmeid_id, 'token': carmeid_token}}
            return JsonResponse(carmeids)
    else:
        carmeids = {'code': 1, 'result': {'errmsg': "Incoming parameter id or password is null."}}
        return JsonResponse(carmeids)

   
# @api_view(['GET'])
# @permission_classes([AllowAny])
def page(request):
    import pdb
    pdb.set_trace()

    params = QueryDict(request.get_full_path()).values()
    for param in params:
        print param

    # return render(request, 'carservices/register.html')

    carmeids = {'errmsg': "empty id or password", 'url': "http://www.baidu.com"}
    #return Response(carmeids, status=status.HTTP_200_OK)


@csrf_exempt
def establish_relationship(request):
    import pdb
    pdb.set_trace()
    #return HttpResponseRedirect('page/')
    

    code = request.GET.get('code')
    state = request.GET.get('state')
    print code
    print state

    if code is None or state is None:
        return HttpResponse('Bad Request')
    
    appid = os.getenv('appid')
    secret = os.getenv('secret')

    fetch_access_token_url = config.FETCH_ACCESS_TOKEN_URL % (appid, secret, code)
    #fetch_access_token_url = 'http://www.baidu.com'
    access_token_response = requests.get(fetch_access_token_url)
    
    access_token_content = access_token_response.json()
    openID = access_token_content.get('openid')
    access_token = access_token_content.get('access_token')

    fetch_user_info_url = config.FETCH_USER_INFO_URL % (access_token, openID)
    userinfo_response = requests.get(fetch_user_info_url)

    userinfo_content = userinfo_response.json()
    nickname = userinfo_content.get('nickname')
    headimgurl = userinfo_content.get('headimgurl')


    # state = '3'
    # openID = '1'
    # nickname = 'awea'
    # headimgurl = 'www.baidu.com'
    try:       
        carmeid = Account.objects.get(id=state)

        # try:
        #     wxuser = WXUser.objects.get(openid=openID)

        #     if (wxuser.account is None) or (wxuser.account.id!=state) or (wxuser.name!=nickname) or (wxuser.head_portrait!=headimgurl):
        #         if wxuser.account is None or wxuser.account.id!=state:
        #             wxuser.account=carmeid
        #         if wxuser.name!=nickname:
        #             wxuser.name=nickname
        #         if wxuser.head_portrait!=headimgurl:
        #             wxuser.head_portrait=headimgurl
        #         wxuser.save()

        # except ObjectDoesNotExist:
        #     wxuser = WXUser.objects.create(openid=openID, name=nickname, head_portrait=headimgurl, account=carmeid)
        
        #pdb.set_trace()
        wxusers = WXUser.objects.filter(openid=openID).filter(bind=True)
        if wxusers is not None and len(wxusers)==1:
            for wxuser in wxusers:
                if wxuser.account.id==state:
                    if wxuser.name==nickname and wxuser.head_portrait==headimgurl:
                        account_wxuser_bind = {'code': 1, 'result': {'msg': "WXUser had already bind to CarMEID."}}
                        return JsonResponse(account_wxuser_bind)
                    else:
                        if wxuser.name!=nickname:
                            wxuser.name=nickname
                        if wxuser.head_portrait!=headimgurl:
                            wxuser.head_portrait=headimgurl
                        wxuser.save()    
                        account_wxuser_bind = {'code': 0, 'result': {'msg': "WXUser's information modified successfully."}}
                        return JsonResponse(account_wxuser_bind)
            account_wxuser_bind = {'code': 1, 'result': {'msg': "Please unbind the binding-CarMEID first."}}
            return JsonResponse(account_wxuser_bind)

        bundled_wxusers = WXUser.objects.filter(openid=openID).filter(bind=False)
        if len(wxusers)==0 and len(bundled_wxusers)>0:
            for bundled_wxuser in bundled_wxusers:
                if bundled_wxuser.account.id==state:
                    bundled_wxuser.bind=True
                    bundled_wxuser.name=nickname
                    bundled_wxuser.head_portrait=headimgurl
                    bundled_wxuser.save()
                    account_wxuser_bind = {'code': 0, 'result': {'msg': "WXUser binds to CarMEID successfully."}}
                    return JsonResponse(account_wxuser_bind)

                    # if wxuser.bind==False and wxuser.account.id!=state:
                    #     new_wxuser = WXUser.objects.create(openid=openID, name=nickname, head_portrait=headimgurl, account=carmeid, bind=True)
                    #     account_wxuser_bind = {'code': 0, 'result': {'msg': "WXUser binds to CarMEID successfully."}}
                    #     return JsonResponse(account_wxuser_bind)

                    # if wxuser.bind==True and wxuser.account.id!=state:
                    #     account_wxuser_bind = {'code': 1, 'result': {'msg': "Please unbinding the binding-CarMEID first."}}
                    #     return JsonResponse(account_wxuser_bind)

                    # if wxuser.bind==True and wxuser.account.id==state and (wxuser.name!=nickname or wxuser.head_portrait!=headimgurl):
                    #     if wxuser.name!=nickname:
                    #         wxuser.name=nickname
                    #     if wxuser.head_portrait!=headimgurl:
                    #         wxuser.head_portrait=headimgurl
                    #     wxuser.save()

                        # wxuser_id = wxuser.id
                        # wxuser_openid = wxuser.openid
                        # wxuser_name = wxuser.name
                        # wxuser_head_portrait = wxuser.head_portrait
                        # wxuser_bind = wxuser.bind

                        # wxuser_account_id = carmeid.id
                        # wxuser_account_create_time = carmeid.create_time
                        # timestamp_wxuser_account_createtime = time.mktime(wxuser_account_create_time.timetuple())

                        # account_wxuser_bind = {'id': wxuser_id, 'openid': wxuser_openid, 'name': wxuser_name, 'head_portrait': wxuser_head_portrait, 
                        #     'bind': wxuser_bind, 'account': {'CarMEID': wxuser_account_id, 'create_time': timestamp_wxuser_account_createtime}}
                        # return JsonResponse(account_wxuser_bind)

                        # account_wxuser_bind = {'code': 0, 'result': {'msg': "WXUser's information modified successfully."}}
                        # return JsonResponse(account_wxuser_bind)

                    # if wxuser.bind==True and wxuser.account.id==state and wxuser.name==nickname and wxuser.head_portrait==headimgurl:
                    #     account_wxuser_bind = {'code': 1, 'result': {'msg': "WXUser had already bind to CarMEID."}}
                    #     return JsonResponse(account_wxuser_bind)

                # else:
                #     continue

            new_wxuser = WXUser.objects.create(openid=openID, name=nickname, head_portrait=headimgurl, account=carmeid, bind=True)
            account_wxuser_bind = {'code': 0, 'result': {'msg': "WXUser binds to CarMEID successfully."}}
            return JsonResponse(account_wxuser_bind)
            
        if len(wxusers)==0 and len(bundled_wxusers)==0:
            new_wxuser = WXUser.objects.create(openid=openID, name=nickname, head_portrait=headimgurl, account=carmeid, bind=True)

            # wxuser_id = new_wxuser.id
            # wxuser_openid = new_wxuser.openid
            # wxuser_name = new_wxuser.name
            # wxuser_head_portrait = new_wxuser.head_portrait
            # wxuser_bind = new_wxuser.bind

            # wxuser_account_id = carmeid.id
            # wxuser_account_create_time = carmeid.create_time
            # timestamp_wxuser_account_createtime = time.mktime(wxuser_account_create_time.timetuple())

            # account_wxuser_bind = {'id': wxuser_id, 'openid': wxuser_openid, 'name': wxuser_name, 'head_portrait': wxuser_head_portrait,
            #     'bind': wxuser_bind, 'account': {'CarMEID': wxuser_account_id, 'create_time': timestamp_wxuser_account_createtime}}
            # return JsonResponse(account_wxuser_bind)

            account_wxuser_bind = {'code': 0, 'result': {'msg': "WXUser binds to CarMEID successfully."}}
            return JsonResponse(account_wxuser_bind)

    except ObjectDoesNotExist:
        account_wxuser_bind = {'code': 1, 'result': {'errmsg': "Invalid CarMEID."}}
        return JsonResponse(account_wxuser_bind)

    #response = requests.get('http://192.168.102.9:8000/api/v1/page/')
    # pdb.set_trace()
    # return HttpResponseRedirect('http://www.baidu.com')


@csrf_exempt
def bound_accounts(request):

    binding_wxusers = []
    request_data = json.loads(request.body)
    CarMEID = request_data.get('id')
    Token = request_data.get('token')

    if len(CarMEID)!=0 and len(Token)!=0:
        try:
            account = Account.objects.get(id=CarMEID)
            account_token = account.token

            if Token==account_token:
                account_id = account.id
                account_create_time = account.create_time
                timestamp_account_createtime = time.mktime(account_create_time.timetuple())

                wxusers = WXUser.objects.filter(account=CarMEID).filter(bind=True)
                for wxuser in wxusers:
                    wxuser_id = wxuser.id
                    wxuser_openid = wxuser.openid
                    wxuser_name = wxuser.name
                    wxuser_head_portrait = wxuser.head_portrait

                    binding_wxuser = {'id': wxuser_id, 'openid': wxuser_openid, 'name': wxuser_name, 'head_portrait': wxuser_head_portrait}
                    binding_wxusers.append(binding_wxuser)

                bundled_accounts = {'code': 0, 'result': {'CarMEID': account_id, 'create_time': timestamp_account_createtime, 'WXUsers': binding_wxusers}}
                return JsonResponse(bundled_accounts)

            else:
                bundled_accounts = {'code': 1, 'result': {'errmsg': "Expired or Invalid token."}}
                return JsonResponse(bundled_accounts)

        except ObjectDoesNotExist:
            bundled_accounts = {'code': 1, 'result': {'errmsg': "Empty or Invalid CarMEID."}}
            return JsonResponse(bundled_accounts)
    else:
        bundled_accounts = {'code': 1, 'result': {'errmsg': "Incoming parameter id or token is null."}}
        return JsonResponse(bundled_accounts)
 
@csrf_exempt
def remove_binding(request):

    request_data = json.loads(request.body)
    CarMEID = request_data.get('id')
    OpenID = request_data.get('openid')
    Token = request_data.get('token')

    if len(CarMEID)!=0 and len(OpenID)!=0 and len(Token)!=0:
        try:
            account = Account.objects.get(id=CarMEID)
            account_token = account.token

            if Token==account_token:
                try:
                    wxuser = WXUser.objects.get(openid=OpenID)
                    if wxuser.bind==True and wxuser.account.id==CarMEID:
                        wxuser.bind=False
                        wxuser.save()
                        unbinding_accounts = {'code': 0, 'result': {'msg': "Remove binding successfully."}}
                        return JsonResponse(unbinding_accounts)
                    else:
                        unbinding_accounts = {'code': 1, 'result': {'errmsg': "WXUser didn't bind to the CarMEID ever."}}
                        return JsonResponse(unbinding_accounts)
                except ObjectDoesNotExist:
                    unbinding_accounts = {'code': 1, 'result': {'errmsg': "WXUser does not exist."}}
                    return JsonResponse(unbinding_accounts)
            else:
                unbinding_accounts = {'code': 1, 'result': {'errmsg': "Expired or Invalid token."}}
                return JsonResponse(unbinding_accounts)

        except ObjectDoesNotExist:
            unbinding_accounts = {'code': 1, 'result': {'errmsg': "Empty or Invalid CarMEID."}}
            return JsonResponse(unbinding_accounts)
    else:
        unbinding_accounts = {'code': 1, 'result': {'errmsg': "Incoming parameter id or token or openid is null."}}
        return JsonResponse(unbinding_accounts)