from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from flask_login import UserMixin
from app import login

class Item(db.Model):
    __tablename__ = "item"

    food_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(30), nullable=False)
    type = db.Column(db.Enum('Appetizer', 'Entree', 'Dessert'), nullable=False)
    description = db.Column(db.VARCHAR(100))
    photo = db.Column(db.VARCHAR(1024), nullable=False)

    def __init__(self, food_id, name, type, description, photo):
        self.food_id = food_id
        self.name = name
        self.type = type
        self.description = description
        self.photo = photo

class My_User(UserMixin, db.Model):
    __tablename__ = "my_user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.VARCHAR(30), unique=True, nullable=False)
    phone = db.Column(db.BigInteger, unique=True, nullable=False)
    first_name = db.Column(db.VARCHAR(30), nullable=False)
    last_name = db.Column(db.VARCHAR(30), nullable=False)
    password = db.Column(db.VARCHAR(128), nullable=False)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __init__(self, id, username, phone, first_name, last_name, password):
        self.id = id
        self.username = username
        self.phone = phone
        self.first_name = first_name
        self.last_name = last_name
        self.password = generate_password_hash(password)

@login.user_loader
def load_user(id):
    return My_User.query.get(id)

class My_Order(db.Model):
    __tablename__ = "my_order"

    order_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(My_User.id), nullable=False)
    message = db.Column(db.VARCHAR(140))
    submit = db.Column(db.TIMESTAMP)

    def __init__(self, order_id, user_id, message, submit):
        self.order_id = order_id
        self.user_id = user_id
        self.message = message
        self.submit = submit

class My_Order2(db.Model):
    __tablename__ = "my_order2"

    __table_args__ = (db.PrimaryKeyConstraint('order_id', 'food_id'),)

    order_id = db.Column(db.Integer, db.ForeignKey(My_Order.order_id), nullable=False)
    food_id = db.Column(db.Integer, db.ForeignKey(Item.food_id), nullable=False)
    message = db.Column(db.VARCHAR(40))

    def __init__(self, order_id, food_id, message):
        self.order_id = order_id
        self.food_id = food_id
        self.message = message