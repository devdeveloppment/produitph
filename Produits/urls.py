from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('', liste_produit , name='liste'),
    path('ajout/', ajout_produits, name='ajout-produit'),
    path('modifier/<int:produit_id>/', modifier_produit, name='modifier-produit'),
    path('supprimer/<int:produit_id>/', supprimer_produit, name='supprimer-produit'),
    path('vendre/<int:produit_id>/', vendre_produit, name='vendre-produit'),

    path('clients/', liste_clients, name='clients'),
    path('clients/ajout/', ajout_client, name='ajout-client'),
    path('clients/modifier/<int:client_id>/', modifier_client, name='modifier-client'),
    path('clients/supprimer/<int:client_id>/', supprimer_client, name='supprimer-client'),

    path('ventes/', liste_ventes, name='ventes'),
    path('facture/<int:vente_id>/', facture_pdf, name='facture-pdf'),

    path('stats/', statistiques, name='stats'),
    path('notifications/', notifications, name='notifications'),
    path('inbox/', inbox, name='inbox'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  
