from django.shortcuts import*

from .models import*

def Accueil(request):

    # recupération des données de la base de données
    produits = Produit.objects.all(),
    context = { 'produits':produits }


    return render(request, 'produit.html', context=context)

def ajout_produits(request):
    # recupération des données de la base de données
    if request.method == 'POST':
        name = request.POST('name')  
        price = request.POST('price')
        quantite = request.POST('quantite')
        date_expiration = request.POST('date_expiration')
        description = request.POST('description')
        image = request.FILES.get('image')


        Categorie = Categorie.objects.get(pk=request.POST('categorie'))

        savedonner = Produit(
            name=name,
            price=price,
            quantite=quantite,
            date_expiration=date_expiration,
            description=description,
            image=image,
            categorie=Categorie
        )
        savedonner.save()
        return redirct('Accueil')
    else:
        Categorie = Categorie.objects.all()

    return render(request, 'ajout_donner.html', Categorie=Categorie)


def liste_produit(request):

    produits = Produit.objects.all()
    context = {'produits':produits}

    return render(request, 'liste_produit.html', context=context)
 



