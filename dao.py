from db import db, Item, Buyer, Order

# your methods here

#Items Methods
def get_all_items():
    return [item.serialize() for item in Item.query.all()]

def create_item(name, price, stock):
    new_item = Item (
        name = name,
        price = price,
        stock = stock
    )
    db.session.add(new_item)
    db.session.commit()
    return new_item.serialize()

def get_item_by_id(item_id):
    item = Item.query.filter_by(id = item_id).first()
    if item is None:
        return None
    return item.serialize()

def get_item_object(item_id):
    item = Item.query.filter_by(id = item_id).first()
    if item is None:
        return None
    return item

def update_item_price(item_id, price):
    item = get_item_object(item_id)
    if item is None:
        return None
    item.price = price
    db.session.commit()
    return item.serialize()

#Buyer Methods

def get_all_buyers():
    return [buyer.serialize() for buyer in Buyer.query.all()]

def create_buyer(username, balance):
    new_buyer = Buyer (
        username = username,
        balance = balance,
    )
    db.session.add(new_buyer)
    db.session.commit()
    create_order(new_buyer.id)
    return new_buyer.serialize()

def get_buyer_object(buyer_id):
    buyer = Buyer.query.filter_by(id = buyer_id).first()
    if buyer is None:
        return None
    return buyer

def get_buyer_by_id(buyer_id):
    buyer = Buyer.query.filter_by(id = buyer_id).first()
    if buyer is None:
        return None
    return buyer.serialize()

def delete_buyer_by_id(buyer_id):
    buyer = Buyer.query.filter_by(id=buyer_id).first()
    if buyer is None:
        return None
    db.session.delete(buyer)
    db.session.commit()
    return buyer.serialize()

#Order Methods

def create_order(buyer_id):
    new_order = Order (
        total = 0,
        buyer_id = buyer_id,
        submitted = False
    )
    db.session.add(new_order)
    db.session.commit()
    return new_order.serialize()

def get_order_by_id(order_id):
    order = Order.query.filter_by(id = order_id).first()
    if order is None:
        return None
    return order.serialize()


def get_order_object(order_id):
    order = Order.query.filter_by(id = order_id).first()
    if order is None:
        return None
    return order

def assign_item_to_order(item_id, order_id):
    order = get_order_object(order_id)
    if order is None:
        return None
    item_object = get_item_object(item_id)
    if item_object is None:
        return None
    order.items.append(item_object)
    db.session.commit()
    return order.serialize()

def get_cart_for_buyer(buyer_id):
    return Order.query.filter_by(buyer_id = buyer_id, submitted = False).first()

def add_item_to_cart(item_id, buyer_id):
    order_object = get_cart_for_buyer(buyer_id)
    item_object = get_item_object(item_id)
    if order_object is None:
        return None
    if item_object is None:
        return None
    temp_items = [item for item in order_object.items if item.id == item_id]
    if len(temp_items) != 0:
        return 404
    if (item_object.stock > 0):
        item_object.stock -= 1
        order_object.total += item_object.price
        order_object.items.append(item_object)
        db.session.commit()
        return order_object.serialize()
    else:
        return None

def remove_item_from_cart(item_id, buyer_id):
    cart = get_cart_for_buyer(buyer_id)
    orig_length = len(cart.items)
    updated_items = [item for item in cart.items if item.id != item_id]
    if (orig_length == len(updated_items)):
        return None
    else:
        cart.items = updated_items
        removed_item = get_item_object(item_id)
        cart.total -= removed_item.price
        removed_item.stock+= 1
        db.session.commit()
        return cart.serialize()

def checkout_cart(buyer_id):
    cart = get_cart_for_buyer(buyer_id)
    if len(cart.items) == 0:
        return 404
    buyer = get_buyer_object(buyer_id)
    if (buyer.balance >= cart.total):
        buyer.balance -= cart.total
        cart.submitted = True
        create_order(buyer_id)
        db.session.commit()
        return buyer.serialize()
    else:
        return None

