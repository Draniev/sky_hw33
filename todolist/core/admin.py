from core.models import User
from django.contrib import admin


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email',
                    'first_name', 'last_name', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email', 'last_name', 'first_name')
    readonly_fields = ('date_joined', 'last_login')
    exclude = ('password',)


# Register your models here.
admin.site.register(User, UserAdmin)
