from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^v1/sign_in/$', views.sign_in, name='sign_in'),
    url(r'^v1/page/$', views.page, name='page'),
    #url(r'^v1/$', views.establishfriends, name='establishfriends')
    url(r'^v1/bind/$', views.establish_relationship, name='establish_relationship'),
    url(r'^v1/bound_accounts/$', views.bound_accounts, name='bound_accounts')
]