from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^v1/sign_in/$', views.sign_in, name='sign_in'),
    url(r'^v1/qrcode/$', views.generate_qrcode, name='qrcode'),
    url(r'^v1/bind/$', views.binding, name='binding'),
    url(r'^v1/bound_accounts/$', views.bound_accounts, name='bound_accounts'),
    url(r'^v1/unbind/$', views.remove_binding, name='remove_binding'),

    url(r'^v1/upload_position/$', views.upload_position, name='upload_position'),
    url(r'^v1/location/$', views.search_position, name='search_position'),
    url(r'^v1/path/$', views.search_trace, name='search_trace'),
]
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)