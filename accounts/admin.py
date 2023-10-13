from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from django.utils.html import format_html

# Register your models here.
class userAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="30" style="border-radius:50%;">'.format(object.profile_picture.url))
    thumbnail.short_description = 'profile picture'
    list_display = ('email', 'first_name', 'last_name', 'username','is_active','is_staff', 'is_admin', 'is_superuser','date_joined')
    readonly_fields = ('date_joined',)
    list_display_links = ('email','username')

class countryAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(Profile, userAdmin)
admin.site.register(Country, countryAdmin)