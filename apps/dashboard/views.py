from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.transferts.models import Transfert
from apps.package.models import Package
from apps.customer.models import Customer
from apps.passengers.models import Ticket
from django.db.models import Count, Sum
from django.utils.timezone import localdate


@login_required()
def dashboard_view(request):
    today = localdate()
    year = today.year
    month = today.month
    agency_id = request.session.get("agency_id")
    currency = request.session.get("currency")
    agency_name = request.session.get("name")
    nb_cus = Customer.objects.filter(agency=agency_id).count()
    nb_ticket = Ticket.objects.filter(
        agency=agency_id, created_at__year=year, created_at__month=month
    ).count()
    sum_ticket_price = Ticket.objects.filter(
        agency=agency_id,
        created_at__year=year,
        created_at__month=month,
    ).aggregate(total_amount=Sum("ticket_price", default=0))["total_amount"]

    monthly_commission = Transfert.objects.filter(
        agency=agency_id,
        created_at__year=year,
        created_at__month=month,
    ).aggregate(total_comm=Sum("commission_amount", default=0))["total_comm"]

    monthly_packages_number = Package.objects.filter(
        agency=agency_id,
        created_at__year=year,
        created_at__month=month,
    ).count()

    sum_package_price = Package.objects.filter(
        agency=agency_id,
        created_at__year=year,
        created_at__month=month,
    ).aggregate(total_amount=Sum("price", default=0))["total_amount"]
    return render(
        request,
        "dashboard/dashboard.html",
        {
            "nb_cus": nb_cus,
            "nb_ticket": nb_ticket,
            "sum_ticket_price": sum_ticket_price,
            "currency": currency,
            "agency_name": agency_name,
            "monthly_commission": monthly_commission,
            "monthly_packages_number": monthly_packages_number,
            "sum_package_price": sum_package_price,
        },
    )
