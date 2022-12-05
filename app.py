# Импортируем стандартный модуль JSON
import json
# Импортируем фреймворк Flask и его функции
from flask import Flask, request
# Импортируем SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Импортируем функции из utils.py, которые будем использовать
from utils import get_users_all, get_orders_all, get_offers_all

# Инициализируем приложение и импортируем конфигурацию
app = Flask(__name__)
app.config.from_object('config.Config')
db = SQLAlchemy(app)


# Создаём модель User с соответствуюшими сущностями
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement="auto")
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    email = db.Column(db.String(250))
    role = db.Column(db.String(250))
    phone = db.Column(db.String(250))

    def user_to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "email": self.email,
            "role": self.role,
            "phone": self.phone
        }


# Создаём модель Order с соответствуюшими сущностями и связями
class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True, autoincrement="auto")
    name = db.Column(db.String(100))
    description = db.Column(db.String(300))
    start_date = db.Column(db.String(100))
    end_date = db.Column(db.String(100))
    address = db.Column(db.String(200))
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def order_to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "address": self.address,
            "price": self.price,
            "customer_id": self.customer_id,
            "executor_id": self.executor_id,
        }


# Создаём модель Offer с соответствуюшими сущностями и связями
class Offer(db.Model):
    __tablename__ = 'offer'
    id = db.Column(db.Integer, primary_key=True, autoincrement="auto")
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def offer_to_dict(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "executor_id": self.executor_id
        }


with app.app_context():
    # Пересоздаем базу
    db.drop_all()
    db.create_all()
    # Создаем экземпляры пользователей
    users = [User(**user_data) for user_data in get_users_all()]
    orders = [Order(**order_data) for order_data in get_orders_all()]
    offers = [Offer(**offer_data) for offer_data in get_offers_all()]
    # Добавляем в сессию и коммитим
    db.session.add_all(users)
    db.session.add_all(orders)
    db.session.add_all(offers)
    db.session.commit()


@app.route("/users", methods=["GET", "POST"])
def get_users():
    """
    Представление, которое обрабатывает запросы GET /users
    и POST /users
    """
    if request.method == "GET":
        result = []
        for user in User.query.all():
            result.append(user.user_to_dict())
        return json.dumps(result), 200
    if request.method == "POST":
        user_data = json.loads(request.data)
        new_user = User(
            id=user_data["id"],
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            age=user_data["age"],
            email=user_data["email"],
            role=user_data["role"],
            phone=user_data["phone"]
        )
        db.session.add(new_user)
        db.session.commit()
        return "User created", 201


@app.route("/users/<int:uid>", methods=["GET", "PUT", "DELETE"])
def get_one_user(uid: int):
    """
    Представление, которое обрабатывает запросы GET /users/<id>,
    PUT /users/<int:uid> и DELETE /users/<id>
    """
    if request.method == "GET":
        user = User.query.get(uid)
        # return jsonify(user_to_dict(user)), 200
        return json.dumps(user.user_to_dict()), 200
    if request.method == "PUT":
        user_data = json.loads(request.data)
        user = User.query.get(uid)
        user.first_name = user_data["first_name"]
        user.last_name = user_data["last_name"]
        user.age = user_data["age"]
        user.email = user_data["email"]
        user.role = user_data["role"]
        user.phone = user_data["phone"]
        db.session.add(user)
        db.session.commit()
        return "User updated", 204
    if request.method == "DELETE":
        user = User.query.get(uid)
        db.session.delete(user)
        db.session.commit()
        return "User deleted", 204


@app.route("/orders", methods=["GET", "POST"])
def get_orders():
    """
    Представление, которое обрабатывает запросы GET /orders
    и POST /orders
    """
    if request.method == "GET":
        result = []
        for order in Order.query.all():
            result.append(order.order_to_dict())
        return json.dumps(result), 200
    if request.method == "POST":
        order_data = json.loads(request.data)
        new_order = Order(
            id=order_data["id"],
            name=order_data["name"],
            description=order_data["description"],
            start_date=order_data["start_date"],
            end_date=order_data["end_date"],
            address=order_data["address"],
            price=order_data["price"],
            customer_id=order_data["customer_id"],
            executor_id=order_data["executor_id"]
        )
        db.session.add(new_order)
        db.session.commit()
        return "Order created", 201


@app.route("/orders/<int:oid>", methods=["GET", "PUT", "DELETE"])
def get_one_order(oid: int):
    """
    Представление, которое обрабатывает запросы GET /orders/<id>,
    PUT /orders/<int:uid> и DELETE /orders/<id>
    """
    if request.method == "GET":
        order = Order.query.get(oid)
        return json.dumps(order.order_to_dict()), 200
    if request.method == "PUT":
        order_data = json.loads(request.data)
        order = Order.query.get(oid)
        order.name = order_data["name"]
        order.description = order_data["description"]
        order.start_date = order_data["start_date"]
        order.end_date = order_data["end_date"]
        order.address = order_data["address"]
        order.price = order_data["price"]
        order.customer_id = order_data["customer_id"]
        order.executor_id = order_data["executor_id"]
        db.session.add(order)
        db.session.commit()
        return "Order updated", 204
    if request.method == "DELETE":
        order = Order.query.get(oid)
        db.session.delete(order)
        db.session.commit()
        return "Order deleted", 204


@app.route("/offers", methods=["GET", "POST"])
def get_offers():
    """
    Представление, которое обрабатывает запросы GET /offers
    и POST /offers
    """
    if request.method == "GET":
        result = []
        for offer in Offer.query.all():
            result.append(offer.offer_to_dict())
        return json.dumps(result), 200
    if request.method == "POST":
        offer_data = json.loads(request.data)
        new_offer = Offer(
            id=offer_data["id"],
            order_id=offer_data["order_id"],
            executor_id=offer_data["executor_id"]
        )
        db.session.add(new_offer)
        db.session.commit()
        return "Offer created", 201


@app.route("/offers/<int:oid>", methods=["GET", "PUT", "DELETE"])
def get_one_offer(oid: int):
    """
    Представление, которое обрабатывает запросы GET /offers/<id>,
    PUT /offers/<int:uid> и offers /users/<id>
    """
    if request.method == "GET":
        offer = Offer.query.get(oid)
        return json.dumps(offer.offer_to_dict()), 200
    if request.method == "PUT":
        offer_data = json.loads(request.data)
        offer = Offer.query.get(oid)
        offer.order_id = offer_data["order_id"]
        offer.executor_id = offer_data["executor_id"]
        db.session.add(offer)
        db.session.commit()
        return "Offer updated", 204
    if request.method == "DELETE":
        offer = Offer.query.get(oid)
        db.session.delete(offer)
        db.session.commit()
        return "Offer deleted", 204


if __name__ == "__main__":
    app.run(debug=True)
