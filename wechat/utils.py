#!/usr/bin/python
# -*- coding:utf-8 -*-

import xml.etree.ElementTree as ET
import uuid, hashlib
from datetime import datetime
import random
import time
import urlparse
import re
from urllib import urlencode


def now():
	return int(time.mktime(datetime.now().timetuple()))

def nonceStr():
	return str(uuid.uuid1()).replace('-', '')


def generateSHA1Sign(dd):
	l = dd.items()
	l = filter(lambda t: t[1] is not None and len(t[1].strip()) > 0, l)
	l = map(lambda t: '%s=%s' % t, l)
	l = sorted(l)
	stringSignTemp = reduce(lambda _1, _2: '%s&%s' % (_1, _2), l)
	stringSignTemp = stringSignTemp.encode('utf8')
	sha1Sign = hashlib.sha1(stringSignTemp).hexdigest()
	return sha1Sign
