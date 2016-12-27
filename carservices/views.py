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
import datetime
import time
import uuid
import logging
import exceptions
import os
import urllib
import qrcode
from cStringIO import StringIO


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

   
@csrf_exempt
def binding(request):
   
    #logger = logging.getLogger('django')
    code = request.GET.get('code')
    state = request.GET.get('state')
    if code is None or state is None:
        redirect_status = {'code': 1, 'result': {'errmsg': "Code or State missing."}}
        return JsonResponse(redirect_status)
    
    appid = os.getenv('AppID')
    secret = os.getenv('AppSecret')
    if appid is None or secret is None:
        public_number_status = {'code': 1, 'result': {'errmsg': "AppID or AppSecret missing."}}
        return JsonResponse(public_number_status)
    fetch_access_token_url = config.FETCH_ACCESS_TOKEN_URL % (appid, secret, code)
    
    try:
        access_token_response = requests.get(fetch_access_token_url)
        access_token_content = access_token_response.json()
    except:
        access_token_request = {'code': 1, 'result': {'errmsg': "Access token Request Error."}}
        return JsonResponse(access_token_request)
    fetch_access_token_errcode = access_token_content.get('errcode')
    if fetch_access_token_errcode is not None:
        fetch_access_token_errmsg = access_token_content.get('errmsg')
        fetch_access_token = {'code': 1, 'result': {'errcode': fetch_access_token_errcode, 'errmsg': fetch_access_token_errmsg}}
        return JsonResponse(fetch_access_token)
    openID = access_token_content.get('openid')
    access_token = access_token_content.get('access_token')
    fetch_user_info_url = config.FETCH_USER_INFO_URL % (access_token, openID)

    try:
        userinfo_response = requests.get(fetch_user_info_url)
        userinfo_content = userinfo_response.json()
    except:
        userinfo_request = {'code': 1, 'result': {'errmsg': "UserInfo Request Error."}}
        return JsonResponse(userinfo_request)
    fetch_userinfo_errcode = userinfo_content.get('errcode')
    if fetch_userinfo_errcode is not None:
        fetch_userinfo_errmsg = userinfo_content.get('errmsg')
        fetch_userinfo = {'code': 1, 'result': {'errcode': fetch_userinfo_errcode, 'errmsg': fetch_userinfo_errmsg}}
        return JsonResponse(fetch_userinfo)
    nickname = userinfo_content.get('nickname').encode('raw_unicode_escape')
    headimgurl = userinfo_content.get('headimgurl')
 
    try:       
        carmeid = Account.objects.get(id=state)
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
       
        if len(wxusers)>1:
            account_wxuser_bind = {'code': 1, 'result': {'msg': "More than one CarMEID that WXUser binding to ."}}
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
            new_wxuser = WXUser.objects.create(openid=openID, name=nickname, head_portrait=headimgurl, account=carmeid, bind=True)
            account_wxuser_bind = {'code': 0, 'result': {'msg': "WXUser binds to CarMEID successfully."}}
            return JsonResponse(account_wxuser_bind)
            
        if len(wxusers)==0 and len(bundled_wxusers)==0:
            new_wxuser = WXUser.objects.create(openid=openID, name=nickname, head_portrait=headimgurl, account=carmeid, bind=True)
            account_wxuser_bind = {'code': 0, 'result': {'msg': "WXUser binds to CarMEID successfully."}}
            return JsonResponse(account_wxuser_bind)
    except ObjectDoesNotExist:
        account_wxuser_bind = {'code': 1, 'result': {'errmsg': "Invalid CarMEID."}}
        return JsonResponse(account_wxuser_bind)


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
            bundled_accounts = {'code': 1, 'result': {'errmsg': "Invalid CarMEID."}}
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
                wxusers = WXUser.objects.filter(openid=OpenID).filter(bind=True)
                if wxusers is not None and len(wxusers)==1:
                    for wxuser in wxusers:
                        if wxuser.account.id==CarMEID:
                            wxuser.bind=False
                            wxuser.save()
                            unbinding_accounts = {'code': 0, 'result': {'msg': "Remove binding successfully."}}
                            return JsonResponse(unbinding_accounts)
                        else:
                            unbinding_accounts = {'code': 1, 'result': {'errmsg': "WXUser doesn't bind to the CarMEID."}}
                            return JsonResponse(unbinding_accounts)                       
                else:
                    unbinding_accounts = {'code': 1, 'result': {'errmsg': "WXUser doesn't exist or bind to one CarMEID."}}
                    return JsonResponse(unbinding_accounts)
            else:
                unbinding_accounts = {'code': 1, 'result': {'errmsg': "Expired or Invalid token."}}
                return JsonResponse(unbinding_accounts)

        except ObjectDoesNotExist:
            unbinding_accounts = {'code': 1, 'result': {'errmsg': "Invalid CarMEID."}}
            return JsonResponse(unbinding_accounts)
    else:
        unbinding_accounts = {'code': 1, 'result': {'errmsg': "Incoming parameter id or token or openid is null."}}
        return JsonResponse(unbinding_accounts)


@csrf_exempt
def generate_qrcode(request):

    CarMEID = request.GET.get('id')
    Token = request.GET.get('token')
    if CarMEID is None or Token is None:
        sign_in_status = {'code': 1, 'result': {'errmsg': "CarMEID or Token missing."}}
        return JsonResponse(sign_in_status)

    appid = os.getenv('AppID')
    if appid is None:
        appid_status = {'code': 1, 'result': {'errmsg': "AppID missing."}}
        return JsonResponse(appid_status)

    if len(CarMEID)!=0 and len(Token)!=0:
        try:
            account = Account.objects.get(id=CarMEID)
            account_token = account.token

            if Token==account_token:
                Redirect_URI = 'http://car.yijiayinong.com/api/v1/bind/'
                redirect_uri = urllib.quote_plus(Redirect_URI)
                authorize_redirect_url = config.AUTHORIZE_REDIRECT_URL % (appid, redirect_uri, CarMEID)

                image = qrcode.make(authorize_redirect_url)
                buf = StringIO()
                image.save(buf)
                image_stream = buf.getvalue()
                return HttpResponse(image_stream, content_type="image/png")
            else:
                qrcode_response = {'code': 1, 'result': {'errmsg': "Expired or Invalid token."}}
                return JsonResponse(qrcode_response)

        except ObjectDoesNotExist:
            qrcode_response = {'code': 1, 'result': {'errmsg': "Invalid CarMEID."}}
            return JsonResponse(qrcode_response)
    else:
        qrcode_response = {'code': 1, 'result': {'errmsg': "Incoming parameter id or token is null."}}
        return JsonResponse(qrcode_response)


@csrf_exempt
def upload_position(request):

    request_data = json.loads(request.body)
    CarMEID = request_data.get('id')
    Token = request_data.get('token')
    LineArrs = request_data.get('lineArr')

    if len(CarMEID)!=0 and len(Token)!=0 and len(LineArrs)!=0:
        try:
            account = Account.objects.get(id=CarMEID)
            account_token = account.token

            if Token==account_token:
                for linearr in LineArrs:
                    if len(linearr)==5:
                        position_account = account
                        position_longitude = linearr[0]
                        position_latitude = linearr[1]
                        position_bearing = linearr[2]
                        position_speed = linearr[3]
                        timestamp_position_time = linearr[4]
                        position_time = datetime.datetime.fromtimestamp(timestamp_position_time)

                        position = Position.objects.create(account=position_account, longitude=position_longitude,
                            latitude=position_latitude, bearing=position_bearing, speed=position_speed, time=position_time)

                        accounts_position = {'code': 0, 'result': {'msg': "Location information upload successfully."}}
                        return JsonResponse(accounts_position)
                    else:
                        accounts_position = {'code': 1, 'result': {'msg': "Incoming parameter lineArr ValueError."}}
                        return JsonResponse(accounts_position)
            else:
                accounts_position = {'code': 1, 'result': {'errmsg': "Expired or Invalid token."}}
                return JsonResponse(accounts_position)

        except ObjectDoesNotExist:
            accounts_position = {'code': 1, 'result': {'errmsg': "Invalid CarMEID."}}
            return JsonResponse(accounts_position)
    else:
        accounts_position = {'code': 1, 'result': {'errmsg': "Incoming parameter id or token or lineArr is null."}}
        return JsonResponse(accounts_position)


@csrf_exempt
def search_position(request):

    request_data = json.loads(request.body)
    CarMEID = request_data.get('id')
    OpenID = request_data.get('openid')
    Token = request_data.get('token')

    if len(CarMEID)!=0 and len(OpenID)!=0 and len(Token)!=0:
        try:
            account = Account.objects.get(id=CarMEID)
            account_token = account.token

            if Token==account_token:
                wxusers = WXUser.objects.filter(openid=OpenID).filter(bind=True)
                if wxusers is not None and len(wxusers)==1:
                    for wxuser in wxusers:
                        if wxuser.account.id==CarMEID:
                            position_account_id = account.id
                            position_account_createtime = account.create_time
                            timestamp_carmeid_createtime = time.mktime(position_account_createtime.timetuple())

                            position = Position.objects.filter(account=CarMEID).order_by('-time').first()
                            position_longitude = position.longitude
                            position_latitude = position.latitude
                            position_bearing = position.bearing
                            position_speed = position.speed
                            position_time = position.time
                            timestamp_position_time = time.mktime(position_time.timetuple())

                            account_position = {'code': 0, 'result': {
                                'account': {'carmeid': position_account_id, 'create_time': timestamp_carmeid_createtime},
                                'longitude': position_longitude, 'latitude': position_latitude, 'bearing': position_bearing,
                                'speed': position_speed, 'time': timestamp_position_time}}
                            return JsonResponse(account_position)
                        else:
                            account_position = {'code': 1, 'result': {'errmsg': "WXUser doesn't bind to the CarMEID."}}
                            return JsonResponse(account_position)
                else:
                    account_position = {'code': 1, 'result': {'errmsg': "WXUser doesn't exist or bind to one CarMEID."}}
                    return JsonResponse(account_position)
            else:
                account_position = {'code': 1, 'result': {'errmsg': "Expired or Invalid token."}}
                return JsonResponse(account_position)

        except ObjectDoesNotExist:
            account_position = {'code': 1, 'result': {'errmsg': "Invalid CarMEID."}}
            return JsonResponse(account_position)
    else:
        account_position = {'code': 1, 'result': {'errmsg': "Incoming parameter id or token or openid is null."}}
        return JsonResponse(account_position)


@csrf_exempt
def search_trace(request):
    # import pdb
    # pdb.set_trace()

    request_data = json.loads(request.body)
    CarMEID = request_data.get('id')
    OpenID = request_data.get('openid')
    Token = request_data.get('token')
    timestamp_StartTime = request_data.get('start_time')
    timestamp_EndTime = request_data.get('end_time')

    points = []
    if len(CarMEID)!=0 and len(OpenID)!=0 and len(Token)!=0 and (timestamp_StartTime and timestamp_EndTime) is not None:
        try:
            account = Account.objects.get(id=CarMEID)
            account_token = account.token

            if Token==account_token:
                wxusers = WXUser.objects.filter(openid=OpenID).filter(bind=True)
                if wxusers is not None and len(wxusers)==1:
                    for wxuser in wxusers:
                        if wxuser.account.id==CarMEID:
                            if timestamp_EndTime>timestamp_StartTime:
                                start_date = datetime.datetime.fromtimestamp(timestamp_StartTime)
                                end_date = datetime.datetime.fromtimestamp(timestamp_EndTime)

                                position_account_id = account.id
                                position_account_createtime = account.create_time
                                timestamp_carmeid_createtime = time.mktime(position_account_createtime.timetuple())

                                positions = Position.objects.filter(account=CarMEID).filter(time__range=(start_date, end_date))
                                for position in positions:
                                    position_longitude = position.longitude
                                    position_latitude = position.latitude
                                    position_bearing = position.bearing
                                    position_speed = position.speed
                                    position_time = position.time
                                    timestamp_position_time = time.mktime(position_time.timetuple())

                                    point = {'longitude': position_longitude, 'latitude': position_latitude, 'bearing': position_bearing,
                                        'speed': position_speed, 'time': timestamp_position_time}
                                    points.append(point)

                                account_traces = {'code': 0, 'result': {'points': points,
                                    'account': {'carmeid': position_account_id, 'create_time': timestamp_carmeid_createtime}}}
                                return JsonResponse(account_traces)
                            else:
                                account_traces = {'code': 1, 'result': {'errmsg': "Incoming parameter values end_time no more than start_time."}}
                                return JsonResponse(account_traces)

                        else:
                            account_traces = {'code': 1, 'result': {'errmsg': "WXUser doesn't bind to the CarMEID."}}
                            return JsonResponse(account_traces)
                else:
                    account_traces = {'code': 1, 'result': {'errmsg': "WXUser doesn't exist or bind to one CarMEID."}}
                    return JsonResponse(account_traces)
            else:
                account_traces = {'code': 1, 'result': {'errmsg': "Expired or Invalid token."}}
                return JsonResponse(account_traces)

        except ObjectDoesNotExist:
            account_traces = {'code': 1, 'result': {'errmsg': "Invalid CarMEID."}}
            return JsonResponse(account_traces)
    else:
        account_traces = {'code': 1, 'result': {'errmsg': "Incoming parameter id or token or openid or start_time or end_time is null."}}
        return JsonResponse(account_traces)