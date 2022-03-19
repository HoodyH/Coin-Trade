from django.contrib import admin
from .models import (
    TradingAction
)

admin.site.register([])


@admin.register(TradingAction)
class TradingActionAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    list_filter = ()
