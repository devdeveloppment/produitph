from django.contrib import admin

from .models import *

admin.site.register(Categorie)
admin.site.register(Produit)
admin.site.register(Customer)
admin.site.register(Vente)
admin.site.register(FactureClient)
