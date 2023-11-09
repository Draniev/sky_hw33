from django.contrib import admin
from bot.models import TgUser


@admin.register(TgUser)
class TgUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'chat_id', 'state', 'verification_code')
