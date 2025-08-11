from django.shortcuts import*
from django.db import transaction
from django.http import JsonResponse

from .models import*

def Accueil(request):
    produits = Produit.objects.all()
    context = { 'produits': produits }
    return render(request, 'liste_produit.html', context)

def ajout_produits(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        prix = request.POST.get('prix')
        quantite = request.POST.get('quantite')
        date_expiration = request.POST.get('date_expiration')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        categorie_id = request.POST.get('categorie')

        categorie = Categorie.objects.get(pk=categorie_id) if categorie_id else None

        produit = Produit(
            nom=nom,
            prix=prix or 0,
            quantite=quantite or 0,
            date_expiration=date_expiration or None,
            description=description or '',
            image=image,
            categorie=categorie
        )
        produit.save()
        return redirect('liste')
    else:
        categories = Categorie.objects.all()

    return render(request, 'ajout_produits.html', { 'categories': categories })


def liste_produit(request):
    produits = Produit.objects.all()
    return render(request, 'liste_produit.html', { 'produits': produits })


def vendre_produit(request, produit_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

    quantite = int(request.POST.get('quantite', 0))
    customer = request.POST.get('customer', '').strip()

    if quantite <= 0 or not customer:
        return JsonResponse({'error': 'Quantité ou client invalide'}, status=400)

    produit = get_object_or_404(Produit, pk=produit_id)

    if produit.quantite < quantite:
        return JsonResponse({'error': 'Stock insuffisant'}, status=400)

    with transaction.atomic():
        produit.quantite -= quantite
        produit.save()
        total = produit.prix * quantite
        Vente.objects.create(
            produit=produit,
            quantite=quantite,
            customer=customer,
            total_vente=total
        )

    return JsonResponse({'success': True, 'nouveau_stock': produit.quantite})
 



