from django.urls import path, include
from .views import *
from . import views

urlpatterns = [
    path("operator/Add/", PhoneOperatorCreateView.as_view(), name="operator_add"),
    path("operator/list/", PhoneOperatorListView.as_view(), name="operators_list"),
    path(
        "operator/edit/<int:pk>/", PhoneOperatorEditView.as_view(), name="operator_edit"
    ),
    path(
        "operator/delete/<int:pk>/",
        PhoneOperatorDeleteView.as_view(),
        name="operator_delete",
    ),
    path("sim/list/", SimCardListView.as_view(), name="simcards_list"),
    path("sim/Add/", SimCardCreateView.as_view(), name="simcard_add"),
    path("sim/edit/<int:pk>/", SimCardEditView.as_view(), name="simcard_edit"),
    path("sim/delete/<int:pk>/", SimCardDeleteView.as_view(), name="simcard_delete"),
    # path("sim-info/<int:sim_id>/", get_sim_info, name="sim-info"),
    path("transfert/list/", TransferListView.as_view(), name="transfert_list"),
    path("transfert/Add/", TransfertAddView.as_view(), name="transfert_add"),
    path(
        "transfert/ajax/simcard-context/",
        views.simcard_context,
        name="simcard_context",
    ),
    # path('sim/edit/<int:pk>/', SimCardEditView.as_view(), name='simcard_edit'),
    # path('sim/delete/<int:pk>/', SimCardDeleteView.as_view(), name='simcard_delete'),
]
