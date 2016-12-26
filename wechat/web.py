#!/usr/bin/python
#-*- coding: UTF-8 -*- 
#coding=utf-8
import sys, os
import tornado.ioloop
import tornado.web
import logging
import logging.handlers
import re
from urllib import unquote

import xml.etree.ElementTree as ET
import config
import pdb
import hashlib
import time
import urllib2
import json
import web
reload(sys)
sys.setdefaultencoding('utf8')

def deamon(chdir = False):
        try:
                if os.fork() > 0:
                        os._exit(0)
        except OSError, e:
                print 'fork #1 failed: %d (%s)' % (e.errno, e.strerror)
                os._exit(1)

def init():
        pass

class DefaultHandler(tornado.web.RequestHandler):
        def get(self):
                self.write('WeChatAPI Say Hello!')

class TestHandler(tornado.web.RequestHandler):
        def get(self):
                self.write('WeChatAPI Test!')

class LogHandler(tornado.web.RequestHandler):
        def get(self):
                log_filename = 'logs/logging'
                if not os.path.exists(log_filename):
                        self.write('The log file is empty.')
                        return
                log_file = None
                log_file_lines = None
                try:
                        log_file = open(log_filename, 'r')
                        if log_file is None:
                                raise Exception('log_file is None')
                        log_file_lines = log_file.readlines()
                        if log_file_lines is None:
                                raise Exception('log_file_lines is None')
                except Exception, e:
                        logger = logging.getLogger('web')
                        logger.error('Failed to read the log file (logs/logging), error: %s' % e)
                finally:
                        if log_file is not None:
                                log_file.close()
                if log_file_lines is None:
                        self.write('Failed to read the log file.')
                line_limit = 500
                for _ in log_file_lines[::-1]:
                        line_limit -= 1
                        if line_limit > 0:
                                self.write(unquote(_) + '<BR/>')



class weixin(tornado.web.RequestHandler):

        def get(self):
                signature = self.get_argument('signature','')
                timestamp = self.get_argument('timestamp','')
                nonce = self.get_argument('nonce','')
                echostr = self.get_argument('echostr','')
                token= config.TOKEN
                list=[token,timestamp,nonce]
                list.sort()
                sha1=hashlib.sha1()
                map(sha1.update,list)
                hashcode=sha1.hexdigest()
                if hashcode == signature:
                        self.write(echostr)
                else:

                        self.write('shibai 4055555')

        def parse_request_xml(self,rootElem):
                msg = {}
                if rootElem.tag == 'xml':
                        for child in rootElem:
                                msg[child.tag] = child.text
                return msg

        def post(self):
                body = self.request.body
                msg = self.parse_request_xml(ET.fromstring(body))
                MsgType = tornado.escape.utf8(msg.get("MsgType"))
                Content= tornado.escape.utf8(msg.get("Content"))
                FromUserName = tornado.escape.utf8(msg.get("FromUserName"))
                CreateTime = tornado.escape.utf8(msg.get("CreateTime"))
                ToUserName = tornado.escape.utf8(msg.get("ToUserName"))
                #关注 click事件
                if MsgType == 'event':
                        eventKey = tornado.escape.utf8(msg.get("EventKey"))
                        sub = tornado.escape.utf8(msg.get("Event"))
                        #扫码事件，返回文本消息 感谢您的关注，谢谢！
                        if sub == 'subscribe':

                                Content="感谢您的关注，谢谢！"
                        #click事件

                        if eventKey == 'Text_1':

                                dom = xml.dom.minidom.parse('weixin/Text_1.xml')
                                print dom
                                Content = "click事件正在处理"
                if MsgType == 'text':
                        Content= tornado.escape.utf8(msg.get("Content"))

                        if Content == '1':

                                Content = "数字啊"
                        else:

                                Content ="000"

                        Content ="您发送的文本消息已收到，谢谢！"

                #图片信息
                if MsgType == 'image':

                        Content = "您发送的图片信息我们已收到，谢谢！"

                #语音消息
                if MsgType == 'voice':
                        Content = "您发送的语音信息我们已收到，谢谢！"

                #视频消息
                if MsgType == 'video':
                        Content = "您发送的视频信息我们已收到，谢谢！"

                #小视频信息
                if MsgType == 'shortvideo':
                        Content = "您发送的小视频信息我们已经收到，谢谢！"

                #地理位置信息
                if MsgType == 'location':
                        Content = "您发的地理位置我们已经收到，谢谢！"

                # url 信息
                if MsgType == 'link':
                        Content = "您发送的url链接我们已收到，谢谢！"
		print MsgType
                data = """<xml>
                        <ToUserName><![CDATA[%s]]></ToUserName>
                        <FromUserName><![CDATA[%s]]></FromUserName>
                        <CreateTime>%s</CreateTime>
                        <MsgType><![CDATA[%s]]></MsgType>
                        <Content><![CDATA[%s]]></Content>
                </xml>""" % (FromUserName,ToUserName,int(time.time()),'text',Content)
                self.write(data)



        #验证密钥
        def token(requset):
		import pdb
                pdb.set_trace()
                url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (
                Config.AppID, Config.AppSecret)
                result = urllib2.urlopen(url).read()
                Config.access_token = json.loads(result).get('access_token')
                print 'access_token===%s' % Config.access_token
                return HttpResponse(result)
        #创建菜单
        def createMenu(request):
                url = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s"% Config.access_token
                data = {
			"button": [
        		{
            			"name": "远程控制",
            			"sub_button": [
                		{
                    			"type": "click",
                    			"name": "查询位置",
                    			"key": "FANGBEI"
                		},
                 		{
            				"name": "快速导航",
            				"type": "location_select",
            				"key": "rselfmenu_2_0"
        			},
                		{
                    			"type": "view",
                    			"name": "行使轨迹",
                    			"url": "http://"
                		},
                		{
                    			"type": "view",
                    			"name": "我的设备",
                    			"url": "http://"
                		}
            			]
        		},
        		{
            		"type": "view",
                    	"name": "流量卡",
                    	"url": "http://"           
        		},
        		{
           		"type": "view",
                    	"name": "更多服务",
                    	"url": "http://m.weizhang8.cn/"
        		}
    			]
		} 
		
                req = urllib2.Request(url)
                req.add_header('Content-Type', 'application/json')
                req.add_header('encoding', 'utf-8')
                response = urllib2.urlopen(req, json.dumps(data,ensure_ascii=False))
                result = response.read()
                return HttpResponse(result)


settings = {
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
}

routes = [
        (r"/", DefaultHandler),
        (r"/wx/test", TestHandler),
        (r"/wx/weixin", weixin),
]
if config.Mode == 'DEBUG':
        routes.append((r"/log", LogHandler))

application = tornado.web.Application(routes, **settings)

if __name__ == "__main__":
        if '-d' in sys.argv:
                deamon()
        logdir = 'logs'
        if not os.path.exists(logdir):
                os.makedirs(logdir)
        fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
        formatter = logging.Formatter(fmt)
        handler = logging.handlers.TimedRotatingFileHandler(
                '%s/logging' % logdir, 'M', 20, 360)
        handler.suffix = '%Y%m%d%H%M%S.log'
        handler.extMatch = re.compile(r'^\d{4}\d{2}\d{2}\d{2}\d{2}\d{2}')
        handler.setFormatter(formatter)
        logger = logging.getLogger('web')
        logger.addHandler(handler)
        if config.Mode == 'DEBUG':
                logger.setLevel(logging.DEBUG)
        else:
                logger.setLevel(logging.ERROR)

        init()

        application.listen(80)
        print 'Server is running, listening on port 80....'
        tornado.ioloop.IOLoop.instance().start()
