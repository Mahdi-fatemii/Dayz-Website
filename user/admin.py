from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(SteamUser)
class SteamUserAdmin(admin.ModelAdmin):
    pass


admin.site.register(VipLevel)
admin.site.register(Vip)
admin.site.register(Payment)
