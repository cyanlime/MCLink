from django.contrib import admin

from .models import *

# Register your models here.

class AccountAdmin(admin.ModelAdmin):
    #list_display = ('id', 'create_time')
    list_display = ('id', 'create_time', 'password', 'token')
    search_fields = ['id']

class WXUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'openid', 'name', 'head_portrait', 'account')
    search_fields = ['name']

admin.site.register(Account, AccountAdmin)
admin.site.register(WXUser, WXUserAdmin)