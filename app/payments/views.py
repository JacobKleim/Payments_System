import json

from django.db import transaction
from django.http import Http404, JsonResponse
from django.utils.dateparse import parse_datetime
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .models import BalanceLog, Organization, Payment


@method_decorator(csrf_exempt, name="dispatch")
class BankWebhookView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            operation_id = data["operation_id"]
            amount = data["amount"]
            payer_inn = data["payer_inn"]
            document_number = data["document_number"]
            document_date = parse_datetime(data["document_date"])
            if document_date is None:
                return JsonResponse({"error": "Invalid document_date"}, status=400)
        except (KeyError, json.JSONDecodeError):
            return JsonResponse({"error": "Invalid input"}, status=400)

        if Payment.objects.filter(operation_id=operation_id).exists():
            return JsonResponse({"status": "already_processed"}, status=200)

        with transaction.atomic():
            payment = Payment.objects.create(
                operation_id=operation_id,
                amount=amount,
                payer_inn=payer_inn,
                document_number=document_number,
                document_date=document_date,
            )
            org, created = Organization.objects.get_or_create(inn=payer_inn)
            old_balance = org.balance
            org.balance += amount
            org.save(update_fields=["balance"])

            BalanceLog.objects.create(
                organization=org,
                old_balance=old_balance,
                new_balance=org.balance,
                payment=payment,
            )
            print(f"Balance updated for {payer_inn}: {old_balance} -> {org.balance}")

        return JsonResponse({"status": "success"}, status=200)


class OrganizationBalanceView(View):
    def get(self, request, inn):
        try:
            org = Organization.objects.get(inn=inn)
        except Organization.DoesNotExist:
            raise Http404("Organization not found")

        return JsonResponse({"inn": org.inn, "balance": org.balance})
