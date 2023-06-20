from django.contrib import admin
from wallets.models import Wallet

from blockchain.models import Transaction


class SentTransactionInline(admin.TabularInline):
    model = Transaction
    fk_name = "sender"
    verbose_name_plural = "Sent Transactions"
    readonly_fields = ("recipient", "amount", "block")
    can_delete = False
    extra = 0


class ReceivedTransactionInline(admin.TabularInline):
    model = Transaction
    fk_name = "recipient"
    verbose_name_plural = "Received Transactions"
    readonly_fields = ("sender", "amount", "block")
    can_delete = False
    extra = 0


class WalletAdmin(admin.ModelAdmin):
    inlines = [SentTransactionInline, ReceivedTransactionInline]


admin.site.register(Wallet, WalletAdmin)
