
import threading
from clients.association_client import envoyer_demande


# Fonction exécutée par chaque association
def lancer_association(nom, produit, quantite):

    envoyer_demande(nom, produit, quantite)


# Liste des associations et de leurs demandes
associations = [
    ("Association A", "riz", 30),
    ("Association B", "riz", 30),
    ("Association C", "riz", 30)
]

threads = []

print("=== TEST DES DEMANDES SIMULTANEES ===")

# Créer un thread pour chaque association
for association in associations:

    thread = threading.Thread(
        target=lancer_association,
        args=association
    )

    threads.append(thread)
    thread.start()


# Attendre la fin de tous les threads
for thread in threads:
    thread.join()


print("\n=== FIN DU TEST ===")
