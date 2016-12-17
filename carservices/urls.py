from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^v1/sign_in/$', views.sign_in, name='sign_in'),
    url(r'^v1/page/$', views.page, name='page'),
    #url(r'^v1/$', views.establishfriends, name='establishfriends')
    url(r'^v1/bind/$', views.establish_relationship, name='establish_relationship'),
    url(r'^v1/bound_accounts/$', views.bound_accounts, name='bound_accounts'),
    url(r'^v1/unbind/$', views.remove_binding, name='remove_binding'),
]
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)