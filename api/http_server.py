"""
Thin HTTP API for the FoodShare frontend.
Reuses the exact same stock_manager logic (lock + JSON).
Does NOT modify the existing TCP server.
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from server.stock_manager import consulter_stocks, traiter_demande

app = Flask(__name__)
CORS(app)


@app.get("/api/health")
def health():
    return jsonify({"status": "ok", "service": "FoodShare API"})


@app.get("/api/stock")
def get_stock():
    try:
        stocks = consulter_stocks()
        items = [{"name": name, "quantity": qty} for name, qty in stocks.items()]
        items.sort(key=lambda x: x["name"])
        return jsonify({
            "stock": items,
            "total": sum(stocks.values()),
            "count": len(stocks),
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.post("/api/request")
def submit_request():
    data = request.get_json(silent=True) or {}

    association = (data.get("association") or "").strip()
    produit = (data.get("produit") or "").strip()
    quantite = data.get("quantite")

    if not association:
        return jsonify({"success": False, "message": "Le nom de l'association est obligatoire."}), 400
    if not produit:
        return jsonify({"success": False, "message": "Le produit est obligatoire."}), 400
    try:
        quantite = float(quantite)
    except (TypeError, ValueError):
        return jsonify({"success": False, "message": "La quantite doit etre un nombre."}), 400
    if quantite <= 0:
        return jsonify({"success": False, "message": "La quantite doit etre superieure a zero."}), 400

    try:
        resultat = traiter_demande(association, produit, quantite)
        accepted = resultat.lower().startswith("demande acceptee")
        return jsonify({
            "success": accepted,
            "message": resultat,
            "association": association,
            "produit": produit,
            "quantite": quantite,
        })
    except Exception as e:
        return jsonify({"success": False, "message": f"Erreur serveur : {e}"}), 500


@app.get("/api/statistics")
def statistics():
    try:
        stocks = consulter_stocks()
        if not stocks:
            return jsonify({
                "total": 0,
                "count": 0,
                "max_product": None,
                "max_quantity": 0,
                "products": [],
            })

        total = sum(stocks.values())
        count = len(stocks)
        max_product = max(stocks, key=stocks.get)
        max_quantity = stocks[max_product]

        top = sorted(
            [{"name": k, "quantity": v} for k, v in stocks.items()],
            key=lambda x: x["quantity"],
            reverse=True,
        )[:10]

        return jsonify({
            "total": total,
            "count": count,
            "max_product": max_product,
            "max_quantity": max_quantity,
            "products": top,
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print("FoodShare HTTP API running on http://127.0.0.1:8000")
    app.run(host="127.0.0.1", port=8000, debug=False)