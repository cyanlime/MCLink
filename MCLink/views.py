#!/usr/bin/env Python
# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from rest_framework import views
from rest_framework.decorators import(
    api_view,
)
from django.http import HttpResponse

@api_view(['GET'])
def mp_verify(request):
    return HttpResponse('mxqdYEZf8FuVDLUT', content_type="text/plain;charset=UTF-8")