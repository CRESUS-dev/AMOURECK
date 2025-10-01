
from .models import *
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CountryForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import ProtectedError
from django.http import HttpResponseRedirect



class CountryListView(LoginRequiredMixin, ListView):
    model = Country
    template_name = "country/country_list.html"
    context_object_name = "countries"
    paginate_by = 10
    ordering = ['name']


class CountryCreateView(LoginRequiredMixin, CreateView):
    model = Country
    form_class = CountryForm
    template_name = "country/country_add.html"
    success_url = reverse_lazy('countries_list')


class CountryEditView(LoginRequiredMixin, UpdateView):
    model = Country
    form_class = CountryForm
    template_name = "country/country_add.html"
    success_url = reverse_lazy('countries_list')


class CountryDeleteView(LoginRequiredMixin, DeleteView):
    model = Country
    success_url = reverse_lazy('countries_list')

    def post(self, request, *args, **kwargs):

        try :
            response = super().post(request, *args, **kwargs)
            messages.success(request,"Le pays a été supprimé avec succès")
            return response
        except ProtectedError:
            messages.error(request,"Vous ne pouvez pas supprimez ce pays, il est lié à des villes")
            """ redirect to countries list in case of error"""
            return HttpResponseRedirect(self.success_url)

