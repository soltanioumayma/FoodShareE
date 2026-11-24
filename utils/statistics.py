import json
from pathlib import Path
from multiprocessing import Process, Queue

BASE_DIR = Path(__file__).resolve().parent.parent
STOCK_FILE = BASE_DIR / "data" / "stocks.json"


def calculer_total(stock, queue):
    total = sum(stock.values())
    queue.put(("total", total))


def compter_produits(stock, queue):
    nombre = len(stock)
    queue.put(("nombre", nombre))


def produit_max(stock, queue):
    produit = max(stock, key=stock.get)
    quantite = stock[produit]
    queue.put(("maximum", produit, quantite))


if __name__ == "__main__":

    with open(STOCK_FILE, "r", encoding="utf-8") as fichier:
        stock = json.load(fichier)

    queue = Queue()

    p1 = Process(target=calculer_total, args=(stock, queue))
    p2 = Process(target=compter_produits, args=(stock, queue))
    p3 = Process(target=produit_max, args=(stock, queue))

    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()

    print("=== STATISTIQUES FOODSHARE ===")

    for i in range(3):
        resultat = queue.get()

        if resultat[0] == "total":
            print("Quantite totale :", resultat[1])

        elif resultat[0] == "nombre":
            print("Nombre de produits :", resultat[1])

        elif resultat[0] == "maximum":
            print("Produit le plus disponible :", resultat[1])
            print("Quantite :", resultat[2])