
import json
import threading
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
STOCK_FILE = BASE_DIR / "data" / "stocks.json"

stock_lock = threading.Lock()

def consulter_stocks():
    with stock_lock:
        with open(STOCK_FILE, "r", encoding="utf-8") as fichier:
            stocks = json.load(fichier)

        return stocks

def traiter_demande(association, produit, quantite):

    with stock_lock:

        with open(STOCK_FILE, "r", encoding="utf-8") as fichier:
            stocks = json.load(fichier)

        if quantite <= 0:
            return "Refus : quantité invalide"

        if produit not in stocks:
            return "Refus : produit inexistant"

        if stocks[produit] >= quantite:

            stocks[produit] -= quantite

            with open(STOCK_FILE, "w", encoding="utf-8") as fichier:
                json.dump(stocks, fichier, indent=4)

            return (
                f"Demande acceptee pour {association}. "
                f"{quantite} de {produit} distribues."
            )

        else:
            return (
                f"Demande refusee pour {association}. "
                f"Stock insuffisant."
            )
