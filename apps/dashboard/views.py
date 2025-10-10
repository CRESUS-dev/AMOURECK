from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.country.models import Agency
# @login_required()

# def dashboard_view(request):
#     return render(request, 'dashboard/dashboard.html')

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'







