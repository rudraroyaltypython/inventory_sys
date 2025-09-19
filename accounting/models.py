from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


class Account(models.Model):
    name = models.CharField(max_length=120)
    code = models.CharField(max_length=32, unique=True)
    balance = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.code} - {self.name}"


class JournalEntry(models.Model):
    date = models.DateField()
    narration = models.TextField(blank=True)

    def __str__(self):
        return f"Entry {self.id} ({self.date})"


class JournalLine(models.Model):
    entry = models.ForeignKey(JournalEntry, related_name="lines", on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.PROTECT)
    debit = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    credit = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.account.name}: Dr {self.debit} / Cr {self.credit}"


# -----------------------
# Signals for auto-balance
# -----------------------

@receiver(post_save, sender=JournalLine)
def update_account_balance_on_save(sender, instance, created, **kwargs):
    """
    When a JournalLine is added or updated, recalc the account balance.
    """
    recalc_account_balance(instance.account)


@receiver(post_delete, sender=JournalLine)
def update_account_balance_on_delete(sender, instance, **kwargs):
    """
    When a JournalLine is deleted, recalc the account balance.
    """
    recalc_account_balance(instance.account)


def recalc_account_balance(account):
    """
    Recalculate balance = sum(debits) - sum(credits).
    """
    lines = JournalLine.objects.filter(account=account)
    debit_total = sum(line.debit for line in lines)
    credit_total = sum(line.credit for line in lines)
    account.balance = debit_total - credit_total
    account.save(update_fields=["balance"])
