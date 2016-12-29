from django.conf.urls import  include, url
from .views import *
import wechat.views
from . import views
urlpatterns = (
   url(r'^$',weixin),
#   url(r'^create/$',createMenu),
   url(r'^weixinJsapi/$',views.weixinJsapi,name='weixinJsapi'),
   url(r'^weixin1Jsapi/$',views.weixin1Jsapi,name='weixin1Jsapi'),
   url(r'^UpdateMaterial/$',views.UpdateMaterial,name='UpdateMaterial'),
)

