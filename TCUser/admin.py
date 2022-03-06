from django.contrib import admin
from .models import User

admin.site.register([])


@admin.register(User)
class CurrencyWalletAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_active')
