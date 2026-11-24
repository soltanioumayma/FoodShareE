
from server.stock_manager import traiter_demande, consulter_stocks

print("=== STOCKS INITIAUX ===")
print(consulter_stocks())

print("\n=== DEMANDE DE L'ASSOCIATION A ===")
resultat = traiter_demande("Association A", "riz", 20)
print(resultat)

print("\n=== STOCKS APRES DISTRIBUTION ===")
print(consulter_stocks())
