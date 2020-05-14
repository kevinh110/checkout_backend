import json
from flask import Flask, request
import dao
from db import db

app = Flask(__name__)
db_filename = "cms.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.drop_all()
    db.create_all()

# generalized response formats
def success_response(data, code=200):
    return json.dumps({"success": True, "data": data}), code


def failure_response(message, code=404):
    return json.dumps({"success": False, "error": message}), code

# routes for items
@app.route("/api/items/", methods=["GET"])
def get_all_items():
    return success_response(dao.get_all_items())

@app.route("/api/items/", methods=["POST"])
def create_item():
    body = json.loads(request.data)
    item = dao.create_item(
        name=body.get("name"),
        price=body.get("price"),
        stock=body.get("stock")
    )
    return success_response(item, 201)

@app.route("/api/items/<int:item_id>/", methods=["POST"])
def update_item_price(item_id):
    body = json.loads(request.data)
    response = dao.update_item_price(item_id, body.get("price"))
    if response is None:
        return failure_response("Item not found")
    else:
        return success_response(response)


#Buyer routes
@app.route("/api/buyers/", methods=["POST"])
def create_buyer():
    body = json.loads(request.data)
    buyer = dao.create_buyer(
        username=body.get("username"),
        balance=body.get("balance")
    )
    return success_response(buyer, 201)

@app.route("/api/buyers/", methods=["GET"])
def get_all_buyers():
    return success_response(dao.get_all_buyers())

@app.route("/api/buyers/<int:buyer_id>/")
def get_buyer(buyer_id):
    buyer = dao.get_buyer_by_id(buyer_id)
    if buyer is None:
        return failure_response("buyer not found!")
    return success_response(buyer)

@app.route("/api/buyers/<int:buyer_id>/", methods=["DELETE"])
def delete_buyer(buyer_id):
    buyer = dao.delete_buyer_by_id(buyer_id)
    if buyer is None:
        return failure_response("buyer not found!")
    return success_response(buyer)


#Special Routes

@app.route("/api/buyers/<int:buyer_id>/add/", methods=["POST"])
def add_to_cart(buyer_id):
    body = json.loads(request.data)
    response = dao.add_item_to_cart(body.get("item_id"), buyer_id)
    if response is None:
        return failure_response("Error: Item is out of stock", 404)
    elif response == 404:
        return failure_response("Limit 1 per customer")
    else:
        return success_response(response)

@app.route("/api/buyers/<int:buyer_id>/remove/", methods=["POST"])
def remove_from_cart(buyer_id):
    body = json.loads(request.data)
    response = dao.remove_item_from_cart(body.get("item_id"), buyer_id)
    if response is None:
        return failure_response("Error: Item not found", 404)
    else:
        return success_response(response)


@app.route("/api/buyers/<int:buyer_id>/checkout/", methods=["POST"])
def checkout_cart(buyer_id):
    response = dao.checkout_cart(buyer_id)
    if response is None:
        return failure_response("Insuffiicent Balance")
    elif response == 404:
        return failure_response("Cart is Empty")
    else:
        return success_response(response)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
