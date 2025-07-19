from django.db import models

class Categorie(models.Model):
    nom = models.CharField(max_length=250)

    def __str__(self):
        return self.nom

class Produit(models.Model):
    nom = models.CharField(max_length=100)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    prix = models.IntegerField()
    quantite = models.PositiveIntegerField(default=0)
    description = models.TextField()
    date_ajout = models.DateTimeField(auto_now_add=True)
    date_expiration = models.DateField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='media/')

    class Meta:
        ordering = ['-date_ajout']

    def statut_quantite(self):
        if self.quantite > 10:
            return 'rouge'
        elif self.quantite <= 10:
            return 'orange'
        else:
            return 'vert'

    def __str__(self):
        return self.nom

class Customer(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Vente(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    sale_date = models.DateTimeField(auto_now_add=True)
    quantite = models.PositiveIntegerField()
    customer = models.CharField(max_length=100)
    total_vente = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.produit)

class FactureClient(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()
    date_achat = models.DateTimeField()
    total_vente = models.ForeignKey(Vente, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)

    def __str__(self):
        return f'le reçu de {self.customer.name}'
