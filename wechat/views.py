#!/usr/bin/python
#-*- coding: UTF-8 -*- 
#coding=utf-8

import hashlib
import json
from xml.etree import ElementTree
from django.utils.encoding import smart_str
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import datetime
import urllib2
import urllib

from wechat import config

from rest_framework.response import Response
from rest_framework import status

from rest_framework.decorators import(
        api_view,
        permission_classes,
        parser_classes,
)
from . import utils
from django.shortcuts import render

from carservices.models import *
from django.shortcuts import render_to_response

def ceshi(request):

    return render(request,'ceshi.html')

def location(request):
    return render(request,'location.html')

def flow_card(request):

    return render(request,'flow_card.html')

def running_track(request):

    return render(request,'index.html')

def map(request):

    return render(request,'map_track.html')

def bill(request):
   
    return render(request,'bill.html')

def flow(request):
    
    return render(request,'flow.html')


def checkSignature(request):

    TOKEN = config.TOKEN
    signature = request.GET.get("signature", None)
    timestamp = request.GET.get("timestamp", None)
    nonce = request.GET.get("nonce", None)
    echoStr = request.GET.get("echostr",None)
    token = TOKEN
    tmpList = [token,timestamp,nonce]
    tmpList.sort()
    tmpstr = "%s%s%s" % tuple(tmpList)
    tmpstr = hashlib.sha1(tmpstr).hexdigest()
    if tmpstr == signature:
        return HttpResponse(echoStr)
    else:
        return HttpResponse("Hello World")

def parseTxtMsg(request):

    xmlstr = smart_str(request.body)
    xml =ElementTree.fromstring(xmlstr)
    ToUserName = xml.find('ToUserName').text
    FromUserName = xml.find('FromUserName').text
    CreateTime =xml.find('CreateTime').text
    MsgType = xml.find('MsgType').text

    if MsgType == 'text':
	msg = ''
    if MsgType == 'image':
	msg = ''
    if MsgType == 'voice':
	msg = ''
    if MsgType == 'video':
	msg = ''
    if MsgType == 'shortvideo':
	msg = ''
    if MsgType == 'location':
	msg = ''
    if MsgType == 'link':
	msg = ''
    
    if MsgType == 'event':
	msgContent = xml.find('Event').text
	if msgContent == 'subscribe':
	    OppenId = FromUserName
            wxusers = WXUser.objects.filter(openid = OppenId).filter(bind=True)
            if wxusers is not None and len(wxusers)==1:
                for _ in wxusers:
                    account = _.account
                msg = '感谢您关注车友同行! 这里可以帮您把手机和车机绑定的一起哦。点击远程控制可查看车机相关信息，查看车的位置、轨迹，发送目的地给车机。流量卡可助您快速充值，实时了解流量使用情况。'
            else:
                msg = '您当前尚未绑定设备哦，如需绑定，点击<a href="http://car.yijiayinong.com/ceshi/">扫一扫</a>，对准设备上的二维码即可！'

	if msgContent == 'unsubscribe':
	    msg = ''
	    
        if msgContent == 'CLICK':
	    key = xml.find('EventKey').text
	    if key == 'ceshi':
		OppenId = FromUserName
		 
		wxusers = WXUser.objects.filter(openid = OppenId).filter(bind=True)
		if wxusers is not None and len(wxusers)==1:
		    for _ in wxusers:
		   	account = _.account
		    msg = '您的车机ID是:'+str(account)
		else:  
		    msg = '您当前尚未绑定设备哦，如需绑定，点击<a href="http://car.yijiayinong.com/ceshi/">扫一扫</a>，对准设备上的二维码即可！'

	    if key == 'news':
		title = '查看违章'
                description = '查看违章'
                picurl = 'http://mmbiz.qpic.cn/mmbiz_png/Y3Yj4z3oKX4jI4SytSgULO6mzq4ECAgJUC3urV40CgIxRaJQQ1QFCSZcKxt8m3YMucHvv0K59zYJicKZzyia1jibg/0?wx_fmt=png'
                url = 'http://m.weizhang8.cn'
		
		return getResponseImageTextXml(FromUserName,ToUserName,title,description,picurl,url)

	if msgContent == 'VIEW':
		msg = '' 

    return sendTxtMsg(FromUserName,ToUserName,msg)


def sendTxtMsg(FromUserName,ToUserName,Content):
    reply_xml = """<xml>
        <ToUserName><![CDATA[%s]]></ToUserName>
        <FromUserName><![CDATA[%s]]></FromUserName>
        <CreateTime>%s</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[%s]]></Content>
        </xml>""" %(FromUserName,ToUserName,datetime.datetime.now(),Content)
    
    return HttpResponse(reply_xml)


def jump(FromUserName,ToUserName,url):

#    reply_xml = """<xml>
#    <ToUserName><![CDATA[%s]]></ToUserName>
#    <FromUserName><![CDATA[%s]]></FromUserName>
#    <CreateTime>%s</CreateTime>
#    <MsgType><![CDATA[%s]]></MsgType>
#    <Content><![CDATA[%s]]></Content>
#    </xml>""" %(FromUserName,ToUserName,datetime.datetime.now(),'text','Content')
#
#    return HttpResponse(reply_xml)
	
    reply_xml = """<xml>
        <ToUserName><![CDATA[%s]]></ToUserName>
        <FromUserName><![CDATA[%s]]></FromUserName>
        <CreateTime>%s</CreateTime>
        <MsgType><![CDATA[%s]]></MsgType>
        <Event><![CDATA[%s]]></Event>
        <EventKey><![CDATA[%s]]></EventKey>
    
        </xml>""" %(FromUserName,ToUserName,datetime.datetime.now(),'event','VIEW',url)
    print reply_xml
    return HttpResponse(reply_xml)


def getResponseImageTextXml(FromUserName, ToUserName,title,description,picurl,url):  
    
    reply_xml = """<xml>
	<ToUserName><![CDATA[%s]]></ToUserName>
	<FromUserName><![CDATA[%s]]></FromUserName>
	<CreateTime>%s</CreateTime>
	<MsgType><![CDATA[news]]></MsgType>
	<ArticleCount>1</ArticleCount>
	<Articles>
	<item>
	    <Title><![CDATA[%s]]></Title>
	    <Description><![CDATA[%s]]></Description>
	    <PicUrl><![CDATA[%s]]></PicUrl>
	    <Url><![CDATA[%s]]></Url>
	</item>
	</Articles>
	</xml>"""%(FromUserName,ToUserName,datetime.datetime.now(),title,description,picurl,url)
    return HttpResponse(reply_xml)


@csrf_exempt
def weixin(request):
    if request.method == 'GET':
        return checkSignature(request)
    else:
        return parseTxtMsg(request)

##获取access_token
def get_token():

    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (
    config.AppID, config.AppSecret)
    result = urllib2.urlopen(url).read()
    access_token = json.loads(result).get('access_token')
    print access_token
    return access_token

def fetchJsApiTicket():
	access_token = get_token()
	if access_token is None:
		return None
	url = 'https://api.weixin.qq.com/cgi-bin/ticket/getticket?type=jsapi&access_token='+access_token
	result1 = urllib2.urlopen(url).read()
        ticket = json.loads(result1).get('ticket')
	return ticket

def createWXConfig(jsApiList):
	nonceStr = utils.nonceStr()
	jsapi_ticket = fetchJsApiTicket()
	timestamp = str(utils.now())
	url = config.url
	d = {
		'noncestr': nonceStr,
		'jsapi_ticket': jsapi_ticket,
		'timestamp': timestamp,
		'url': url
	}
	signature = utils.generateSHA1Sign(d)
	dd = {
		'debug': False,
		'appId': config.AppID,
		'timestamp': timestamp,
		'nonceStr': nonceStr,
		'signature': signature,
		'jsApiList': jsApiList
	}
	return dd

@api_view(['GET'])
@csrf_exempt
def weixinJsapi(request):

    jsApiList = request.GET.get('jsApiList', None)
    data = createWXConfig(jsApiList)
    return Response(data)
    
    

def create1WXConfig(jsApiList):
        nonceStr = utils.nonceStr()
        jsapi_ticket = fetchJsApiTicket()
        timestamp = str(utils.now())
        url = config.url1
        d = {
                'noncestr': nonceStr,
                'jsapi_ticket': jsapi_ticket,
                'timestamp': timestamp,
                'url': url
        }
        signature = utils.generateSHA1Sign(d)
        dd = {
                'debug': False,
                'appId': config.AppID,
                'timestamp': timestamp,
                'nonceStr': nonceStr,
                'signature': signature,
                'jsApiList': jsApiList
        }
        return dd

@api_view(['GET'])
@csrf_exempt
def weixin1Jsapi(request):

    jsApiList = request.GET.get('jsApiList', None)
    data = create1WXConfig(jsApiList)
    return Response(data)


##创建自定义菜单	
@csrf_exempt
def createMenu(request):
    url = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s" % get_token()
    data = {
        "button": [
        {
            "name": "远程控制",
            "sub_button": [
                {
                    "type": "view",
                    "name": "查询位置",
                    "url": "http://car.yijiayinong.com/location/"
                },
                {
                    "name": "快速导航",
                    "type": "location_select",
                    "key": "rselfmenu_2_0"
                },
                {
                    "type": "view",
                    "name": "行驶轨迹",
                    "url": "http://car.yijiayinong.com/running_track/"
                },
                {
                    "type": "click",
                    "name": "我的设备",
                    "key": "ceshi"
                }]
        },
        {
            "type": "view",
            "name": "流量卡",
            "url": "http://car.yijiayinong.com/flow_card/"
        },
        {
           "type": "click",
           "name": "更多服务",
           "key": "news"
        }]
    }

    req = urllib2.Request(url)
    req.add_header('Content-Type', 'application/json')
    req.add_header('encoding', 'utf-8')
    response = urllib2.urlopen(req, json.dumps(data,ensure_ascii=False).encode('utf8'))
    result = response.read()
    return HttpResponse(result)


#获取图文列表
def Material():
   
    url = "https://api.weixin.qq.com/cgi-bin/material/batchget_material?access_token=%s" % get_token()
    data = {
    	"type":"news",
    	"offset":"0",
    	"count":"1"
    }
    req = urllib2.Request(url)
    req.add_header('Content-Type', 'application/json')
    req.add_header('encoding', 'utf-8')
    response = urllib2.urlopen(req, json.dumps(data,ensure_ascii=False).encode('utf8'))
    result = response.read()
    media = json.loads(result)
    media_id = (media['item'][0])['media_id']
    print media_id
    return media_id

#根据media_id,获取图文。
@api_view(['GET'])
@csrf_exempt
def UpdateMaterial(request):
    
    media_id = Material()
    url = 'https://api.weixin.qq.com/cgi-bin/material/get_material?access_token=%s' % get_token()
    data = {
	"media_id":media_id
    }
    req = urllib2.Request(url)
    req.add_header('Content-Type', 'application/json')
    req.add_header('encoding', 'utf-8')
    response = urllib2.urlopen(req, json.dumps(data,ensure_ascii=False).encode('utf8'))
    res = response.read()
    result = json.loads(res)
    return Response(result)

    
