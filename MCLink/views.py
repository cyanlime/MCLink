#!/usr/bin/env Python
# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from django.http import HttpResponse, JsonResponse

def mp_verify(request):
    return HttpResponse('mxqdYEZf8FuVDLUT', content_type="text/plain;charset=UTF-8")
    # v = {'a': 123}
    # # import json
    # # return HttpResponse(json.dumps(v))
    # response = JsonResponse(v)
    # return response