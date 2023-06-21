from django.contrib import admin

from blockchain.models import Block, Chain, Transaction


class TransactionInline(admin.TabularInline):
    model = Transaction
    readonly_fields = ("sender", "recipient", "amount", "block")
    can_delete = False
    extra = 0


class BlockAdmin(admin.ModelAdmin):
    model = Block
    inlines = [
        TransactionInline,
    ]
    readonly_fields = ("previous_hash", "timestamp", "proof", "security_hashes")


class ChainAdmin(admin.ModelAdmin):
    model = Chain
    readonly_fields = ("blocks", "difficulty")


admin.site.register(Block, BlockAdmin)
admin.site.register(Chain, ChainAdmin)
