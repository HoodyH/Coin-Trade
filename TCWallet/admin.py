from django.contrib import admin
from .models import (
    Wallet,
    CurrencyWallet,
    Transaction,
)

admin.site.register([Wallet])


@admin.register(CurrencyWallet)
class CurrencyWalletAdmin(admin.ModelAdmin):
    list_display = ('wallet', 'currency', 'value')
    list_filter = ('wallet', 'currency')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('currency_wallet', 'value')
    list_filter = ('currency_wallet',)
