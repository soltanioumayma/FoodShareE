
import json
import queue

from server.stock_manager import traiter_demande


# File d'attente partagee
request_queue = queue.Queue()


def handle_client(client_socket, address):

    print(f"Nouvelle connexion : {address}")

    try:
        # Recevoir la demande
        with client_socket.makefile("r", encoding="utf-8") as fichier:
            ligne = fichier.readline()

        if not ligne:
            client_socket.close()
            return

        demande = json.loads(ligne)

        # Ajouter la demande dans la file d'attente
        request_queue.put((demande, client_socket))

        print("Demande ajoutee a la file d'attente.")

    except Exception as erreur:
        print("Erreur de reception :", erreur)

        try:
            reponse = {"erreur": "Demande invalide"}
            client_socket.sendall(
                (json.dumps(reponse) + "\n").encode("utf-8")
            )
        except OSError:
            pass

        client_socket.close()


def worker():

    while True:

        # Recuperer une demande dans la file
        demande, client_socket = request_queue.get()

        try:
            association = demande["association"]
            produit = demande["produit"]
            quantite = demande["quantite"]

            # Traiter la demande
            resultat = traiter_demande(
                association, produit, quantite
            )

            # Envoyer le resultat au client
            reponse = {"resultat": resultat}

            client_socket.sendall(
                (json.dumps(reponse) + "\n").encode("utf-8")
            )

            print("Demande traitee :", resultat)

        except Exception as erreur:
            print("Erreur de traitement :", erreur)

            try:
                reponse = {"erreur": "Impossible de traiter la demande"}
                client_socket.sendall(
                    (json.dumps(reponse) + "\n").encode("utf-8")
                )
            except OSError:
                pass

        finally:
            client_socket.close()
            request_queue.task_done()
