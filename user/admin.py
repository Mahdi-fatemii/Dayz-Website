from django.contrib import admin
from .models import SteamUser
# Register your models here.


@admin.register(SteamUser)
class SteamUserAdmin(admin.ModelAdmin):
    pass