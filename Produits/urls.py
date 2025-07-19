from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('', liste_produit , name='liste'),
    path('ajout/', ajout_produits, name='ajout-produit'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  
