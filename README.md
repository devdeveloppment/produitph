# GestionPharmacie

Application Django de gestion de pharmacie (produits, clients, ventes, factures PDF, statistiques, notifications, inbox).

## Prérequis
- Python 3.10+
- pip
- (Optionnel) virtualenv/venv

## Installation
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

## URLs principales
- Produits: `/`
- Ajouter produit: `/ajout/`
- Clients: `/clients/`
- Ventes: `/ventes/`
- Statistiques: `/stats/`
- Notifications: `/notifications/`
- Boîte de réception: `/inbox/`
- Facture PDF (ex): `/facture/1/`

## Notes
- Les fichiers upload (images) se trouvent dans `media/`.
- Le projet est configuré pour SQLite par défaut (`db.sqlite3`).
- Pour l’admin Django, créez un superuser:
```bash
python manage.py createsuperuser
```