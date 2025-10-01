from django.contrib.auth import logout
from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from .forms import CustomLoginForm
from django.http import request
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from apps.core.models import Enterprise
from apps.country.models import  *


class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = 'accounts/login.html'

    # affichage du logo
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        enterprise = Enterprise.objects.first()  # récupérer la première entreprise
        if enterprise and enterprise.logo:
            context['logo'] = enterprise.logo.url  # récupérer l'URL de l'image
        else:
            context['logo'] = None
        return context


    def form_valid(self, form):
        user = form.get_user()
        selected_agency = form.cleaned_data.get('agency')
        # vérifier si l'utilisateur a des succursales assignées
        if not user.agencies.exists():
            messages.error(self.request, "Vous n'êtes assigné à aucune agence.")
            return redirect('login')

        # Vérifier si le pays est assignée à l'utilisateur
        if selected_agency and selected_agency not in user.agencies.all():
            messages.error(self.request, "Vous n'êtes pas autorisé à accéder à cette agence.")
            return redirect("login")

        # Enregistrer l'agence dans la session
        if selected_agency:
            self.request.session['agency_id'] = selected_agency.id
            self.request.session['name'] = selected_agency.name
            self.request.session['country_id'] = selected_agency.country.id


        # vérifier l'option remember me
        if form.cleaned_data.get('remember_me'):
            # prolonger la session si "remember me est activé"
            self.request.session.set_expiry(604800)  # une semaine en seconde
        else:
            self.request.session.set_expiry(0)  # la session expirera à la fermeture du navigateur

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Le nom d'utilisateur ou le mot de passe est incorrect ou le compte est inactif")

        return self.render_to_response(self.get_context_data(form=form))


class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        # deconnecter explicitement l'utilisateur
        logout(request)
        # messages flash
        messages.success(request, "Vous avez été déconnecté(e) avec succès")
        return redirect('login')
