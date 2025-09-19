from django.contrib import admin
from .models import Account, JournalEntry, JournalLine


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "balance")
    search_fields = ("code", "name")
    ordering = ("code",)


class JournalLineInline(admin.TabularInline):  # inline table inside JournalEntry
    model = JournalLine
    extra = 1  # show 1 empty row by default
    autocomplete_fields = ["account"]


@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ("id", "date", "narration")
    search_fields = ("narration",)
    date_hierarchy = "date"
    inlines = [JournalLineInline]


@admin.register(JournalLine)
class JournalLineAdmin(admin.ModelAdmin):
    list_display = ("entry", "account", "debit", "credit")
    list_filter = ("account",)
    search_fields = ("entry__narration", "account__name")
