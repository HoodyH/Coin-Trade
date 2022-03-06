from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from TCWallet.models import Wallet

User = get_user_model()


class TradingMetadata(models.Model):
    timestamp = models.DateTimeField(auto_now=True)
    amount = models.FloatField(_('Invested mount'), default=0)
    change = models.FloatField(_('Change of the currency'), default=0)

    class Meta:
        abstract = True


class TradingAction(TradingMetadata):
    """Trading action list"""
    pass


class TradingBlock(models.Model):

    class AlgorithmsChoices(models.TextChoices):
        SOP = 'SOP', _('Sell on point')

    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    wallet = models.ForeignKey(Wallet, null=True, on_delete=models.SET_NULL)

    algorithm = models.CharField(
        max_length=3,
        default=AlgorithmsChoices.SOP,
        choices=AlgorithmsChoices.choices,
        null=False,
        blank=False
    )
