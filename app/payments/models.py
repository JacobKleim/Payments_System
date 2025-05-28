from django.db import models


class Organization(models.Model):
    inn = models.CharField(max_length=12, unique=True)
    balance = models.BigIntegerField(default=0)

    def __str__(self):
        return f"Organization {self.inn} Balance: {self.balance}"


class Payment(models.Model):
    operation_id = models.UUIDField(unique=True)
    amount = models.BigIntegerField()
    payer_inn = models.CharField(max_length=12)
    document_number = models.CharField(max_length=100)
    document_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.operation_id} Amount: {self.amount}"


class BalanceLog(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="balance_logs")
    old_balance = models.BigIntegerField()
    new_balance = models.BigIntegerField()
    changed_at = models.DateTimeField(auto_now_add=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"BalanceLog for {self.organization.inn} at {self.changed_at}"
