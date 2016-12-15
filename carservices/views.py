#!/usr/bin/env Python
# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from .models import *
from . import config
from rest_framework import views
from rest_framework.views import APIView
from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import(
    AllowAny,
    IsAuthenticated,
)
from rest_framework.decorators import(
    api_view,
    permission_classes,
    parser_classes,
)

from django.http import HttpResponse, QueryDict, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.exceptions import ObjectDoesNotExist
import requests
import json
import time
import uuid
import exceptions

# Create your views here.

@api_view(['POST'])
@permission_classes([AllowAny])
def sign_in(request):
    # import pdb
    # pdb.set_trace()
    CarMEID = request.data.get('id')
    PassWord = request.data.get('password')
    
    if CarMEID is not None and PassWord is not None:
        try:
            carmeid = Account.objects.get(id=CarMEID)
        except ObjectDoesNotExist:
            carmeid = Account.objects.create(id=CarMEID, password=PassWord, token=str(uuid.uuid1()))

        carmeid_id = carmeid.id
        carmeid_token = carmeid.token
        carmeid_create_time = carmeid.create_time
        timestamp_carmeid_createtime = time.mktime(carmeid_create_time.timetuple())

        carmeids = {'create_time': timestamp_carmeid_createtime, 'id': carmeid_id, 'token': carmeid_token}
        return Response(carmeids, status=status.HTTP_200_OK)
    
    else:
        carmeids = {'errmsg': "empty id or password"}
        return Response(carmeids, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def page(request):
    import pdb
    pdb.set_trace()

    params = QueryDict(request.get_full_path()).values()
    for param in params:
        print param

    # return render(request, 'carservices/register.html')

    carmeids = {'errmsg': "empty id or password", 'url': "http://www.baidu.com"}
    return Response(carmeids, status=status.HTTP_200_OK)


@api_view(['GET'])
#@api_view(['POST'])
@permission_classes([AllowAny])
def establish_relationship(request):
    import pdb
    #pdb.set_trace()
    #return HttpResponseRedirect('page/')
    
    # # # code = request.GET.get('code')
    # # # state = request.GET.get('state')

    # # # if code is None or state is None:
    # # #     return HttpResponse('Bad Request')
    
    # # # fetch_access_token_url = '%s%s%s' % (config.FETCH_ACCESS_TOKEN_URL) 
    # # # access_token_response = requests.get(fetch_access_token_url)
    
    # # # access_token_content = access_token_response.json()
    # # # openID = access_token_content.get('openid')
    # # # access_token = access_token_content.get('access_token')

    # # # fetch_user_info_url = '%s%s' % (config.FETCH_USER_INFO_URL)
    # # # userinfo_response = requests.get(fetch_user_info_url)

    # # # userinfo_content = userinfo_response.json()
    # # # nickname = userinfo_content.get('nickname')
    # # # headimgurl = userinfo_content.get('headimgurl')

    
    state = '2'
    openID = '1'
    nickname = 'aasxa'
    headimgurl = 'www.baidu.com'
    try:       
        carmeid = Account.objects.get(id=state)

        try:
            wxuser = WXUser.objects.get(openid=openID)

            if wxuser.account.id!=state:
                wxuser.account=carmeid
                wxuser.save()

            else:
                # if wxuser.name!=nickname:
                #     wxuser.name=nickname
                #     wxuser.save()
                # if wxuser.head_portrait!=headimgurl:
                #     wxuser.head_portrait=headimgurl
                #     wxuser.save()
                #pdb.set_trace()
                if (wxuser.name!=nickname) or (wxuser.head_portrait!=headimgurl):
                    wxuser.name=nickname
                    wxuser.head_portrait=headimgurl
                    wxuser.save()

        except ObjectDoesNotExist:
            wxuser = WXUser.objects.create(openid=openID, name=nickname, head_portrait=headimgurl, account=carmeid)

        wxuser_id = wxuser.id
        wxuser_openid = wxuser.openid
        wxuser_name = wxuser.name
        wxuser_head_portrait = wxuser.head_portrait

        wxuser_account_id = carmeid.id
        wxuser_account_create_time = carmeid.create_time
        timestamp_wxuser_account_createtime = time.mktime(wxuser_account_create_time.timetuple())

        account_wxuser_bind = {'id': wxuser_id, 'openid': wxuser_openid, 'name': wxuser_name, 'head_portrait': wxuser_head_portrait, 
            'account': {'CarMEID': wxuser_account_id, 'create_time': timestamp_wxuser_account_createtime}}             
        return Response(account_wxuser_bind, status=status.HTTP_200_OK)

    except ObjectDoesNotExist:
        account_wxuser_bind = {'errmsg': "Empty CarMEID"}
        return Response(account_wxuser_bind, status=status.HTTP_200_OK)


    #response = requests.get('http://192.168.102.9:8000/api/v1/page/')

    # pdb.set_trace()
    # return HttpResponseRedirect('http://www.baidu.com')

@api_view(['POST'])
@permission_classes([AllowAny])
def bound_accounts(request):
    # import pdb
    # pdb.set_trace()

    binding_wxusers = []
    CarMEID = request.data.get('id')

    try:
        account = Account.objects.get(id=CarMEID)
        account_id = account.id
        account_create_time = account.create_time
        timestamp_account_createtime = time.mktime(account_create_time.timetuple())

        wxusers = WXUser.objects.filter(account=CarMEID)
        for wxuser in wxusers:
            wxuser_id = wxuser.id
            wxuser_openid = wxuser.openid
            wxuser_name = wxuser.name
            wxuser_head_portrait = wxuser.head_portrait

            binding_wxuser = {'id': wxuser_id, 'openid': wxuser_openid, 'name': wxuser_name, 'head_portrait': wxuser_head_portrait}
            binding_wxusers.append(binding_wxuser)

        bundled_accounts = {'CarMEID': account_id, 'create_time': timestamp_account_createtime, 'WXUsers': binding_wxusers}
        return Response(bundled_accounts, status=status.HTTP_200_OK)

    except ObjectDoesNotExist:
        bundled_accounts = {'errmsg': "Empty or Invalid CarMEID"}
        return Response(bundled_accounts, status=status.HTTP_200_OK)