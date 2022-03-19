from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, default='main', null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name="unique-wallet-per-user")
        ]

    def __str__(self):
        return f'{self.user}-{self.name}'

    @property
    def value(self):
        v = 0
        for cw in CurrencyWallet.objects.filter(wallet=self):
            v += cw.value
        return v if v else 0


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

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['currency', 'wallet'], name="unique-currency-in-wallet")
        ]

    def __str__(self):
        return f'{self.wallet}-{self.currency}'

    @property
    def value(self):
        _val = int(Transaction.objects.filter(
            currency_wallet=self,
            direction=Transaction.TransactionDirectionChoices.IN
        ).aggregate(models.Sum('value')).get('value__sum') or 0)

        _val -= int(Transaction.objects.filter(
            currency_wallet=self,
            direction=Transaction.TransactionDirectionChoices.OUT
        ).aggregate(models.Sum('value')).get('value__sum') or 0)

        return _val


class Transaction(models.Model):
    """Represent a currency transaction inside a wallet"""

    class TransactionDirectionChoices(models.TextChoices):
        OUT = 0, _('Outgoing transaction')
        IN = 1, _('Ingoing transaction')

    currency_wallet = models.ForeignKey(CurrencyWallet, on_delete=models.CASCADE)
    direction = models.CharField(
        max_length=3,
        choices=TransactionDirectionChoices.choices,
        default=TransactionDirectionChoices.OUT,
        null=False,
        blank=False
    )
    value = models.FloatField(default=0)
    change = models.FloatField(default=0)
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f'{self.currency_wallet}-{self.value}'
