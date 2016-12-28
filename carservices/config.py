#!/usr/bin/python

AUTHORIZE_REDIRECT_URL = \
    ('https://open.weixin.qq.com/connect/oauth2/authorize'
    '?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_userinfo&state=%s#wechat_redirect')
FETCH_WEB_ACCESS_TOKEN_URL = \
    ('https://api.weixin.qq.com/sns/oauth2/access_token'
    '?appid=%s&secret=%s&code=%s&grant_type=authorization_code')
FETCH_USER_INFO_URL = \
    ('https://api.weixin.qq.com/sns/userinfo'
    '?access_token=%s&openid=%s&lang=zh_CN')


FETCH_ACCESS_TOKEN_URL = \
    ('https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential'
    '?appid=%s&secret=%s')
CREATE_QRCODE_TICKET_URL = \
    ('https://api.weixin.qq.com/cgi-bin/qrcode/create'
    '?access_token=%s')
FETCH_QRCODE_URL = \
    ('https://mp.weixin.qq.com/cgi-bin/showqrcode'
    '?ticket=%s')
FETCH_BASE_USER_INFO_URL = \
    ('https://api.weixin.qq.com/cgi-bin/user/info'
    '?access_token=%s&openid=%s&lang=zh_CN')