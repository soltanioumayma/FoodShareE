
import socket
import threading
from server.request_handler import handle_client, worker


HOST = "127.0.0.1"
PORT = 5000

# Nombre de workers
NUMBER_OF_WORKERS = 3


def start_server():

    server = socket.socket(
        #utilise l'adressage IPv4.
        socket.AF_INET,
        #utilise TC
        socket.SOCK_STREAM
    )

    server.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )

    server.bind((HOST, PORT))
    server.listen()

    print("================================")
    print("       FOODSHARE SERVER")
    print("================================")

    # Demarrer les workers
    for i in range(NUMBER_OF_WORKERS):

        thread = threading.Thread(
            target=worker,
            daemon=True
        )

        thread.start()

        print(f"Worker {i + 1} demarre.")

    print(f"Serveur en attente sur {HOST}:{PORT}")

    try:

        while True:

            # Accepter un client
            client_socket, address = server.accept()

            # Creer un thread pour recevoir sa demande
            thread = threading.Thread(
                target=handle_client,
                args=(client_socket, address)
            )

            thread.start()

    except KeyboardInterrupt:
        print("\nArret du serveur.")

    finally:
        server.close()


if __name__ == "__main__":
    start_server()
