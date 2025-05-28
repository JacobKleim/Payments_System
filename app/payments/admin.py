from django.contrib import admin

from .models import BalanceLog, Organization, Payment


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    pass


@admin.register(BalanceLog)
class BalanceLogAdmin(admin.ModelAdmin):
    pass


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    pass
