from django.db.models import Sum
from django.views.generic.base import TemplateView
from django.utils import timezone
from decimal import Decimal

from djqscsv import render_to_csv_response

from recoup import models

class HomePageView(TemplateView):
    template_name = "home.html"
    title = "Scrooge Cost DB"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context["site_header"], context["site_title"] = self.title, self.title
        context["year"] = models.FinancialYear.objects.first()
        return context

class BillView(TemplateView):
    template_name = "bill.html"

    def get_context_data(self, **kwargs):
        context = super(BillView, self).get_context_data(**kwargs)
        division = models.Division.objects.get(pk=int(self.request.GET["division"]))
        services = division.enduserservice_set.all()
        for service in services:
            service.cost_estimate_display = round(Decimal(division.user_count) / Decimal(service.total_user_count()) * service.cost_estimate(), 2)
        context.update({
            "division": division,
            "services": services,
            "created": timezone.now().date,
        })
        return context
    