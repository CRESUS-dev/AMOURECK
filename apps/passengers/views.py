
from .models import *
from apps.country.models import *
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import TicketForm
from django.urls import reverse_lazy
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Sum
from django.db.models.functions import TruncDate
from django.utils.dateparse import parse_date
from datetime import datetime, time
from django.utils.timezone import make_aware
from djmoney.money import Money



class TicketCreateView(LoginRequiredMixin, CreateView):
    model = Ticket
    form_class = TicketForm
    template_name = 'passengers/ticket_add.html'
    success_url = reverse_lazy('ticket_list')


    def get_context_data(self, **kwargs):
        customer_id =0
        # retrieve the existant context
        context = super().get_context_data(**kwargs)
        # ✅ add customers for the bootstrap model
        context['customers'] = Customer.objects.all().order_by('lastName')

        # --- PRESERVE selected customer when the form is re-rendered (POST with errors) ---
        selected =None

        if self.request.method == "POST":
            customer_id = self.request.POST.get('customer_id')
        else:
            customer_id = self.request.GET.get('customer_id')

        if customer_id:
            try:
                selected = Customer.objects.get(pk=customer_id)
            except Customer.DoesNotExist:
                selected = None

        context['selected_customer'] = selected

        return context


    # get the selected country currency
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


    def form_valid(self, form):
        agency_id = self.request.session.get('agency_id')
        customer_id = self.request.POST.get('customer_id')

        form.instance.agency_id = agency_id

        # associer le client sélectionné
        if customer_id:
            from apps.customer.models import Customer
            form.instance.customer_id = customer_id
        return super().form_valid(form)


class TicketListView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = 'passengers/tickets_list.html'
    context_object_name = "tickets"
    paginate_by = 10
    ordering = ['-updated_at']


    def get_context_data(self, **kwargs):
        """injecter la liste des agences dans le context"""
        context = super().get_context_data(**kwargs)
        agencies = Agency.objects.order_by('name').distinct()
        context['agencies'] = agencies
        return context

class TicketEditView(LoginRequiredMixin, UpdateView):

    model = Ticket
    form_class = TicketForm
    template_name = 'passengers/ticket_add.html'
    success_url = reverse_lazy('ticket_list')
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customers'] = Customer.objects.all().order_by('lastName')

        # Récupère le client du ticket en édition
        ticket = self.object
        context['selected_customer'] = getattr(ticket, 'customer', None)
        return context

class TicketDeleteView(LoginRequiredMixin, DeleteView):
    model = Ticket
    success_url = reverse_lazy('ticket_list')


class TicketDetailView(LoginRequiredMixin, DetailView):
    model = Ticket
    template_name = "passengers/ticket_detail.html"
    context_object_name = "ticket"

# def ticket_render_pdf_view(request, *args, **kwargs):
#     pk = kwargs.get('pk')
#     ticket = get_object_or_404(Ticket, pk=pk)
#
#     template_path = 'passengers/ticket_pdf_print.html'
#     context = {'ticket':ticket}
#     # create a Django response object, and specify content_type as pdf
#     response = HttpResponse(content_type='application/pdf')
#     # if download
#     # response['Content-Disposition'] = 'attachement; filename="ticket_2.pdf"'
#     # if display
#     response['Content-Disposition'] = 'filename="ticket.pdf"'
#
#     # find the template and render it.
#     template = get_template(template_path)
#     html = template.render(context)
#
#     # create a pdf
#     pisa_status = pisa.CreatePDF(html, dest=response)
#     # if error then show some funy view
#     if pisa_status.err:
#         return HttpResponse("We had some errors <pre> " + html + '<pre>')
#     return response
def ticket_render_pdf_view(request, *args, **kwargs):
    pk = kwargs.get('pk')
    ticket = get_object_or_404(Ticket, pk=pk)

    template_path = 'passengers/ticket_pdf_print.html'

    #  Nettoyer les None → chaîne vide
    clean_ticket = {}
    for field, value in ticket.__dict__.items():
        clean_ticket[field] = "" if value is None  or str(value).lower() == "none" else value

    # Construction du chemin complet du logo
    logo_url = ''
    if ticket.agency.logo:
        logo_path = os.path.join(settings.MEDIA_ROOT, str(ticket.agency.logo))
        if os.path.exists(logo_path):
            logo_url = request.build_absolute_uri(settings.MEDIA_URL + str(ticket.agency.logo))

    context = {
        'ticket': ticket,
        'logo_url': logo_url,
        'clean_ticket':clean_ticket

    }


    # Crée la réponse PDF
    response = HttpResponse(content_type='application/pdf')

    # Nom dynamique basé sur le code du ticket
    filename = f"ticket_{ticket.ticket_code}.pdf"
    # Pour afficher dans le navigateur (inline)
    response['Content-Disposition'] = f'inline; filename="{filename}"'


    # --- APERÇU HTML ---
    if request.GET.get("preview") == "1":
        # Affiche le HTML dans le navigateur, aucun téléchargement
        return render(request, "passengers/ticket_pdf_print.html", context)

    # Rendre le HTML du template
    template = get_template(template_path)
    # request=request applique les context_processors, les variables globales, etc.
    html = template.render(context, request=request)

    # Créer le PDF
    pisa_status = pisa.CreatePDF(html, dest=response)

    # En cas d’erreur
    if pisa_status.err:
        return HttpResponse("Erreur lors de la génération du PDF.<pre>" + html + "</pre>")

    return response

def ticket_dashboard_data(request):
    date_from = request.GET.get("date_from")
    date_to   = request.GET.get("date_to")

    qs = Ticket.objects.all()

    if date_from:
        d_from = parse_date(date_from)
        dt_from = make_aware(datetime.combine(d_from, time.min))
        qs = qs.filter(updated_at__gte=dt_from)

    if date_to:
        d_to = parse_date(date_to)
        dt_to = make_aware(datetime.combine(d_to, time.max))
        qs = qs.filter(updated_at__lte=dt_to)

    # --- Tickets count per agency (for chart)
    counts = (
        qs.values("agency__name")
        .annotate(total=Count("id"))
        .order_by("agency__name")
    )

    # --- Amount per agency (same qs, grouped)
    amounts = (
        qs.values("agency__name", "ticket_price_currency")
        .annotate(total_amount=Sum("ticket_price"))
        .order_by("agency__name")
    )

    return JsonResponse({
        "labels": [c["agency__name"] for c in counts],
        "values": [c["total"] for c in counts],
        "amounts": list(amounts),
    })

def ticket_dashboard(request):
    return render(request,"passengers/ticket_dashboard.html")






