#!/usr/bin/python
#-*- coding: UTF-8 -*- 
#coding=utf-8
"""
WSGI config for MCLink project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os
import hashlib
import json
import urllib2
import urllib
from wechat import config

url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (
config.AppID, config.AppSecret)
result = urllib2.urlopen(url).read()
access_token = json.loads(result).get('access_token')
url = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s" % access_token
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
        "url": "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxf1cad953c13fccfc&redirect_uri=http://car.yijiayinong.com/flow_card/&response_type=code&scope=snsapi_base&state=123#wechat_redirect"
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


from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MCLink.settings")

application = get_wsgi_application()


