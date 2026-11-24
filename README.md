# FoodShare
### Système distribué de gestion et de redistribution des dons alimentaires

## 1. Présentation du projet

FoodShare est un système informatique conçu pour faciliter la gestion et la redistribution des dons alimentaires entre un serveur central et plusieurs associations.

Le système permet aux associations d'envoyer des demandes de produits alimentaires. Le serveur reçoit ces demandes, vérifie la disponibilité des produits dans le stock et décide d'accepter ou de refuser chaque demande.

L'objectif principal est d'éviter les erreurs de distribution, notamment lorsque plusieurs associations demandent simultanément les mêmes produits.

## 2. Objectifs

- Gérer un stock alimentaire centralisé.
- Permettre aux associations de communiquer avec le serveur.
- Traiter plusieurs demandes simultanément.
- Éviter la distribution d'une quantité supérieure au stock disponible.
- Calculer des statistiques sur les produits disponibles.
- Découvrir les concepts de programmation distribuée et parallèle en Python.

## 3. Architecture du système

FoodShare utilise une architecture client-serveur.

Le serveur central gère le stock et traite les demandes reçues. Les associations jouent le rôle de clients et communiquent avec le serveur à travers des sockets TCP.

```text
       Association A
             |
       Association B
             |
       Association C
             |
          TCP / Socket
             |
      Serveur FoodShare
             |
       File d'attente
             |
          Workers
             |
       Gestion du stock
             |
         stocks.json
```

Les demandes sont placées dans une file d'attente. Plusieurs threads workers récupèrent les demandes et les traitent.

Un verrou (`Lock`) protège l'accès au stock afin d'éviter que plusieurs threads modifient les mêmes données en même temps.

## 4. Technologies utilisées

- **Python** : langage de programmation.
- **Sockets TCP** : communication entre les clients et le serveur.
- **Threading** : traitement concurrent des demandes.
- **Queue** : file d'attente des demandes.
- **Multiprocessing** : calcul parallèle des statistiques.
- **JSON** : stockage des données du stock.
- **PyCharm** : environnement de développement.

## 5. Organisation du projet

```text
PythonProject1/
│
├── server/
│   ├── main_server.py
│   ├── stock_manager.py
│   └── request_handler.py
│
├── clients/
│   └── association_client.py
│
├── data/
│   └── stocks.json
│
├── utils/
│   └── statistics.py
│
├── test_stock.py
├── test_concurrent.py
└── README.md
```

## 6. Fonctionnement

### Gestion des demandes

Une association envoie une demande contenant son nom, le produit demandé et la quantité souhaitée.

Le serveur vérifie les informations et consulte le stock.

- Si la quantité est disponible, la demande est acceptée et le stock est mis à jour.
- Si la quantité est insuffisante, la demande est refusée.
- Si la quantité demandée est invalide ou le produit inexistant, la demande est refusée.

### Traitement concurrent

Le serveur utilise plusieurs threads workers pour traiter les demandes reçues.

La file d'attente permet de transmettre les demandes aux workers. Un verrou protège la partie critique de la gestion du stock.

### Calcul parallèle

Le module de statistiques utilise plusieurs processus pour effectuer différents calculs :

- Calcul de la quantité totale disponible.
- Comptage des produits différents.
- Recherche du produit ayant la quantité maximale.

Les résultats sont transmis à l'aide d'une `Queue` multiprocessing.

## 7. Installation et exécution

### Prérequis

- Python 3 installé.
- PyCharm ou un autre éditeur Python.

### Démarrer le serveur

Depuis le dossier racine du projet :

```bash
python -m server.main_server
```

Le serveur doit rester ouvert pendant les tests.

### Lancer un client association

Dans un deuxième terminal :

```bash
python -m clients.association_client
```

Saisir le nom de l'association, le produit et la quantité demandée.

### Tester les demandes simultanées

```bash
python test_concurrent.py
```

Ce test envoie plusieurs demandes de manière concurrente.

### Calculer les statistiques

```bash
python utils/statistics.py
```

## 8. Tests réalisés

Les tests permettent de vérifier :

- La consultation du stock.
- L'acceptation d'une demande valide.
- Le refus d'une demande lorsque le stock est insuffisant.
- Le traitement de demandes simultanées.
- La protection du stock contre les modifications concurrentes.
- Le calcul parallèle des statistiques.

Dans le test de concurrence, plusieurs associations demandent simultanément 30 unités de riz alors que le stock initial est de 50 unités.

Le résultat attendu est qu'une seule demande soit acceptée et que les autres soient refusées. Le stock ne doit jamais devenir négatif.

## 9. Limites et améliorations possibles

La version actuelle utilise un fichier JSON pour sauvegarder le stock et une communication TCP testée localement.

Des améliorations futures pourraient inclure :

- Une interface graphique pour les associations.
- Une base de données pour stocker les dons.
- Une authentification des associations.
- Une communication entre plusieurs ordinateurs sur un réseau.
- Un historique des distributions.
- Des notifications lorsqu'un produit devient presque épuisé.

## 10. Conclusion

FoodShare est une application client-serveur qui met en pratique plusieurs concepts de programmation distribuée et parallèle avec Python.

Le projet permet de comprendre la communication par sockets, le traitement concurrent avec les threads, la synchronisation des accès au stock et le calcul parallèle avec multiprocessing.

Il propose une solution informatique simple pour améliorer la gestion et la redistribution des dons alimentaires.