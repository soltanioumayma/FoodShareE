
import socket
import json

HOST = "127.0.0.1"
PORT = 5000

def envoyer_demande(association, produit, quantite):

    client = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    try:
        client.settimeout(10)
        client.connect((HOST, PORT))

        demande = {
            "association": association,
            "produit": produit,
            "quantite": quantite
        }

        message = json.dumps(demande) + "\n"
        client.sendall(message.encode("utf-8"))

        with client.makefile("r", encoding="utf-8") as fichier:
            ligne = fichier.readline()

        if not ligne:
            print("Erreur : aucune reponse du serveur.")
            return

        reponse = json.loads(ligne)

        if "resultat" in reponse:
            print("\nRéponse du serveur :")
            print(reponse["resultat"])
        else:
            print("Erreur :", reponse.get("erreur"))

    except (ConnectionError, OSError, TimeoutError) as erreur:
        print(f"Erreur de communication pour {association} : {erreur}")

    finally:
        client.close()


if __name__ == "__main__":

    print("===== FOODSHARE CLIENT =====")

    association = input("Nom de l'association : ")
    produit = input("Produit demandé : ")
    quantite = float(input("Quantité demandée : "))

    envoyer_demande(association, produit, quantite)
