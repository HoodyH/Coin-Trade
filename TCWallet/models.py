from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user}'


class CurrencyWallet(models.Model):

    class CurrenciesChoices(models.TextChoices):
        BITCOIN = 'BTC', _('Bitcoin')
        CRO = 'CRO', _('Cro')
        ETHEREUM = 'ETH', _('Ethereum')

    currency = models.CharField(
        max_length=3,
        choices=CurrenciesChoices.choices,
        null=False,
        blank=False
    )
    wallet = models.ForeignKey(Wallet, null=True, on_delete=models.SET_NULL)
    value = models.FloatField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['currency', 'wallet'], name="unique-currency-in-wallet")
        ]


class Transaction(models.Model):
    """Represent a currency transaction inside a wallet"""
    currency_wallet = models.ForeignKey(CurrencyWallet, on_delete=models.CASCADE)
    value = models.FloatField(default=0)
