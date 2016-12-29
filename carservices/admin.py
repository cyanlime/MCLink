from django.contrib import admin

from .models import *

# Register your models here.

class AccountAdmin(admin.ModelAdmin):
    #list_display = ('id', 'create_time')
    list_display = ('id', 'create_time', 'carmeid', 'password', 'token')
    search_fields = ['carmeid']

class WXUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'openid', 'name', 'head_portrait', 'account', 'bind')
    search_fields = ['name']

class PositionAdmin(admin.ModelAdmin):
    list_display = ('id', 'longitude', 'latitude', 'bearing', 'speed', 'time', 'account')
    search_fields = ['id']

admin.site.register(Account, AccountAdmin)
admin.site.register(WXUser, WXUserAdmin)
admin.site.register(Position, PositionAdmin)