from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

order_item_assoc = db.Table("order_item_assoc", db.Model.metadata,
    db.Column("order_id", db.Integer, db.ForeignKey("order.id")),
    db.Column("item_id", db.Integer, db.ForeignKey("item.id"))
)

class Item(db.Model):
    __tablename__ = "item"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable = False)
    price = db.Column(db.Integer, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    # many-to-many relationship
    orders = db.relationship("Order", secondary=order_item_assoc, back_populates="items")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "stock": self.stock,
            "price": self.price,
        }

    def serialize_short(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
        }

class Order(db.Model):
    __tablename__ = "order"
    id = db.Column(db.Integer, primary_key=True)
    total = db.Column(db.Integer, nullable=False)
    submitted = db.Column(db.Boolean, nullable=False)
    # one-to-many relationship
    buyer_id = db.Column(db.Integer,db.ForeignKey("buyer.id"), nullable=False)
    # many-to-many relationship
    items = db.relationship("Item", secondary = order_item_assoc, back_populates="orders")


    def serialize(self):
        return {
            "id": self.id,
            "total": self.total,
            "items": [item.serialize_short() for item in self.items]
        }

    def serialize_short(self):
        return {
            "total": self.total,
            "items": [item.serialize_short() for item in self.items]
        }


class Buyer(db.Model):
    __tablename__ = "buyer"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    balance = db.Column(db.Integer, nullable=False)
    #1-to-many relationship
    orders = db.relationship("Order", cascade="delete")

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "balance": self.balance,
            "cart": [order.serialize_short() for order in self.orders if order.submitted == False],
            "orders": [order.serialize() for order in self.orders if order.submitted == True],
        }
