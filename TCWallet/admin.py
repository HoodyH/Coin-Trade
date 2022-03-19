from django.contrib import admin
from .models import (
    Wallet,
    CurrencyWallet,
    Transaction,
)


@admin.register(Wallet)
class CurrencyWalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'get_value')
    list_filter = ('user',)

    def get_value(self, obj: CurrencyWallet) -> str:
        return f"{obj.value:.2f}€"


@admin.register(CurrencyWallet)
class CurrencyWalletAdmin(admin.ModelAdmin):
    list_display = ('wallet', 'currency', 'get_value')
    list_filter = ('wallet', 'currency')

    def get_value(self, obj: CurrencyWallet) -> str:
        return f"{obj.value:.2f}€"


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'currency_wallet', 'direction', 'value', 'change')
    list_filter = ('currency_wallet', 'direction')
