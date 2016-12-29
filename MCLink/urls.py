"""MCLink URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from . import views

from django.conf import settings
import wechat.views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include('carservices.urls', namespace="carservices")),
    url(r'^MP_verify_mxqdYEZf8FuVDLUT.txt', views.mp_verify, name='mp_verify'),


    url(r'^ceshi/$',wechat.views.ceshi,name='ceshi'),
    url(r'^location/$',wechat.views.location,name='location'),
    url(r'^running_track/$',wechat.views.running_track,name='running_track'),
    url(r'^flow_card/$',wechat.views.flow_card,name='flow_card'),
    url(r'^map/$',wechat.views.map,name='map'),
    url(r'^bill/$',wechat.views.bill,name='bill'),
    url(r'^flow/$',wechat.views.flow,name='flow'),
    url(r'^wechat/', include('wechat.urls')),

]
urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)

