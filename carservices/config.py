#!/usr/bin/python

AUTHORIZE_BASE_REDIRECT_URL = \
    ('https://open.weixin.qq.com/connect/oauth2/authorize'
    '?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_base&state=%s#wechat_redirect')
AUTHORIZE_REDIRECT_URL = \
    ('https://open.weixin.qq.com/connect/oauth2/authorize'
    '?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_userinfo&state=%s#wechat_redirect')
FETCH_ACCESS_TOKEN_URL = \
    ('https://api.weixin.qq.com/sns/oauth2/access_token'
    '?appid=%s&secrect=%s&code=%s&grant_type=authorization_code')

FETCH_USER_INFO_URL = \
    ('https://api.weixin.qq.com/sns/userinfo'
    '?access_token=%s&openid=%s&lang=zh_CN')
