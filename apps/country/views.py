
from .models import *
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CountryForm, TownForm, AgencyForm
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


class TownCreateView(LoginRequiredMixin, CreateView):
    model = Town
    form_class = TownForm
    template_name = 'country/town_add.html'
    success_url = reverse_lazy('towns_list')





class TownListView(LoginRequiredMixin, ListView):
    model = Town
    template_name = 'country/town_list.html'
    context_object_name = 'towns'
    paginate_by = 10
    ordering = ['name']


class TownEditView(LoginRequiredMixin, UpdateView):
    model = Town
    form_class = TownForm
    template_name = 'country/town_add.html'
    success_url = reverse_lazy('towns_list')


class TownDeleteView(LoginRequiredMixin, DeleteView):
    model = Town
    success_url = reverse_lazy('towns_list')


class AgencyCreateView(LoginRequiredMixin, CreateView):
    model = Agency
    form_class = AgencyForm
    template_name = 'country/agency_add.html'
    success_url = reverse_lazy('agencies_list')


class AgencyListView(LoginRequiredMixin, ListView):
    model = Agency
    template_name = 'country/agency_list.html'
    context_object_name = 'agencies'
    paginate_by = 10
    ordering = ['name']


class AgencyEditView(LoginRequiredMixin, UpdateView):
    model = Agency
    form_class = AgencyForm
    template_name = 'country/agency_add.html'
    success_url = reverse_lazy('agencies_list')


class AgencyDeleteView(LoginRequiredMixin, DeleteView):
    model = Agency
    success_url = reverse_lazy('agencies_list')