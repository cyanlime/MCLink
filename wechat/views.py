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
from django.core.exceptions import ObjectDoesNotExist


def ceshi(request):

   return render(request,'ceshi.html')

def location(request):

   return render(request,'location.html')


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
	Content = xml.find('Content').text
		
 	if Content == '1':
       	    msg = '悬崖边上放了一个 WARNING 的牌子，结果只有程序猿掉了下去...'
        elif Content == '2':
            msg = datetime.datetime.now()
        else:
            msg = '欢迎访问车友同行微信公众号，本公众号正在建设中，目前提供的服务有限，输入1听一个笑话，输入2查看当前时间,任意输入将重新收到本消息。'

    if MsgType == 'image':
	msg = '您发的图片我们已经收到。'
    if MsgType == 'voice':
	msg = '感谢您的留言，我们会尽快处理。'
    if MsgType == 'video':
	msg = '感谢您的留言，我们会尽快处理。'
    if MsgType == 'shortvideo':
	msg = '感谢您的留言，我们会尽快处理。'
    if MsgType == 'location':
	msg = msg = '您当前尚未绑定设备哦，如需绑定，点击<a href="http://car.yijiayinong.com/ceshi/">扫一扫</a>，对准设备上的二维码即可！'
    if MsgType == 'link':
	msg = '感谢您的留言，我们会尽快处理。'
    
    if MsgType == 'event':
	msgContent = xml.find('Event').text
	if msgContent == 'subscribe':
	    msg = '感谢您的关注！'

	if msgContent == 'unsubscribe':
	    msg = '取消关注？'
	    
        if msgContent == 'CLICK':
	    key = xml.find('EventKey').text
	    if key == 'ceshi':
		OppenId = FromUserName
		 
		wxusers = WXUser.objects.filter(openid = OppenId).filter(bind=True)
		if wxusers is not None and len(wxusers)==1:
		    for _ in wxusers:
			account = _.account 
		    msg = account
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
                    "url": "http://www.baidu.com"
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
            "url": "http://www.baidu.com"
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

    
