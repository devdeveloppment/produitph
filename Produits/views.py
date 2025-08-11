from django.shortcuts import*
from django.db import transaction
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.urls import reverse
from django.db.models import Sum, Count

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


def modifier_produit(request, produit_id):
    produit = get_object_or_404(Produit, pk=produit_id)
    if request.method == 'POST':
        produit.nom = request.POST.get('nom') or produit.nom
        produit.prix = request.POST.get('prix') or produit.prix
        produit.quantite = request.POST.get('quantite') or produit.quantite
        produit.date_expiration = request.POST.get('date_expiration') or produit.date_expiration
        produit.description = request.POST.get('description') or produit.description
        if request.FILES.get('image'):
            produit.image = request.FILES.get('image')
        categorie_id = request.POST.get('categorie')
        if categorie_id:
            produit.categorie = get_object_or_404(Categorie, pk=categorie_id)
        produit.save()
        return redirect('liste')
    categories = Categorie.objects.all()
    return render(request, 'edit_produits.html', { 'produit': produit, 'categories': categories })


def supprimer_produit(request, produit_id):
    if request.method != 'POST':
        return HttpResponse(status=405)
    produit = get_object_or_404(Produit, pk=produit_id)
    produit.delete()
    return redirect('liste')


def liste_produit(request):
    produits = Produit.objects.all()
    # Filtres
    q = request.GET.get('q', '').strip()
    categorie_id = request.GET.get('categorie')
    if q:
        produits = produits.filter(nom__icontains=q)
    if categorie_id:
        produits = produits.filter(categorie_id=categorie_id)
    categories = Categorie.objects.all()
    customers = Customer.objects.all().order_by('name')
    return render(request, 'liste_produit.html', { 'produits': produits, 'categories': categories, 'customers': customers, 'q': q, 'categorie_id': categorie_id })


def vendre_produit(request, produit_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

    quantite = int(request.POST.get('quantite', 0))
    customer_name = request.POST.get('customer', '').strip()
    customer_id = request.POST.get('customer_id')

    if quantite <= 0:
        return JsonResponse({'error': 'Quantité invalide'}, status=400)

    produit = get_object_or_404(Produit, pk=produit_id)
    if produit.quantite < quantite:
        return JsonResponse({'error': 'Stock insuffisant'}, status=400)

    # Résoudre client
    client_obj = None
    if customer_id:
        client_obj = get_object_or_404(Customer, pk=customer_id)
        customer_name = client_obj.name
    elif customer_name:
        client_obj, _ = Customer.objects.get_or_create(name=customer_name)
    else:
        return JsonResponse({'error': 'Client requis'}, status=400)

    with transaction.atomic():
        produit.quantite -= quantite
        produit.save()
        total = produit.prix * quantite
        vente = Vente.objects.create(
            produit=produit,
            quantite=quantite,
            customer=customer_name,
            total_vente=total
        )
        FactureClient.objects.create(
            customer=client_obj,
            quantite=quantite,
            date_achat=timezone.now(),
            total_vente=vente,
            produit=produit
        )

    # Pour usage non-AJAX, rediriger vers liste
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'nouveau_stock': produit.quantite})
    return redirect('liste')


def liste_clients(request):
    q = request.GET.get('q', '').strip()
    clients = Customer.objects.all()
    if q:
        clients = clients.filter(name__icontains=q)
    return render(request, 'clients_list.html', { 'clients': clients, 'q': q })


def ajout_client(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if name:
            Customer.objects.get_or_create(name=name)
            return redirect('clients')
    return render(request, 'client_form.html', { 'action': 'ajout' })


def modifier_client(request, client_id):
    client = get_object_or_404(Customer, pk=client_id)
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if name:
            client.name = name
            client.save()
            return redirect('clients')
    return render(request, 'client_form.html', { 'action': 'modifier', 'client': client })


def supprimer_client(request, client_id):
    if request.method != 'POST':
        return HttpResponse(status=405)
    client = get_object_or_404(Customer, pk=client_id)
    client.delete()
    return redirect('clients')


def liste_ventes(request):
    ventes = Vente.objects.select_related('produit').all().order_by('-sale_date')
    return render(request, 'ventes_list.html', { 'ventes': ventes })


def facture_pdf(request, vente_id):
    # Générer un PDF simple pour une vente donnée
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4

    vente = get_object_or_404(Vente, pk=vente_id)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="facture_{vente_id}.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    y = height - 50
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, y, "Facture d'achat")
    y -= 30

    p.setFont("Helvetica", 12)
    p.drawString(50, y, f"Date: {vente.sale_date.strftime('%d/%m/%Y %H:%M')}")
    y -= 20
    p.drawString(50, y, f"Client: {vente.customer}")
    y -= 20
    p.drawString(50, y, f"Produit: {vente.produit.nom}")
    y -= 20
    p.drawString(50, y, f"Quantité: {vente.quantite}")
    y -= 20
    p.drawString(50, y, f"Prix unitaire: {vente.produit.prix} €")
    y -= 20
    p.drawString(50, y, f"Total: {vente.total_vente} €")

    p.showPage()
    p.save()
    return response


def statistiques(request):
    total_produits = Produit.objects.count()
    total_stock = Produit.objects.aggregate(total=Sum('quantite'))['total'] or 0
    total_ventes = Vente.objects.aggregate(total=Sum('total_vente'))['total'] or 0
    nb_ventes = Vente.objects.count()
    top_produits = (Vente.objects.values('produit__nom')
                    .annotate(q=Sum('quantite'))
                    .order_by('-q')[:5])
    # Produits proches de la rupture
    faibles = Produit.objects.filter(quantite__lte=10).count()

    return render(request, 'stats.html', {
        'total_produits': total_produits,
        'total_stock': total_stock,
        'total_ventes': total_ventes,
        'nb_ventes': nb_ventes,
        'top_produits': top_produits,
        'faibles': faibles,
    })


def notifications(request):
    # Notifications basiques: produits en rupture/ faibles + expirations proches
    alerts = []
    for p in Produit.objects.all():
        if p.quantite == 0:
            alerts.append({ 'type': 'danger', 'message': f"Rupture: {p.nom}" })
        elif p.quantite <= 10:
            alerts.append({ 'type': 'warning', 'message': f"Stock faible ({p.quantite}): {p.nom}" })
        if p.date_expiration:
            from datetime import date, timedelta
            if p.date_expiration <= date.today() + timedelta(days=7):
                alerts.append({ 'type': 'info', 'message': f"Expire bientôt ({p.date_expiration}): {p.nom}" })
    return render(request, 'notifications.html', { 'alerts': alerts })


def inbox(request):
    # Boîte de réception simple: dernières ventes assimilées à messages
    messages = Vente.objects.select_related('produit').order_by('-sale_date')[:20]
    return render(request, 'inbox.html', { 'messages': messages })
 



