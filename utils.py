# Импортируем стандартный модуль JSON
import json


def get_users_all():
    """
    Чтение данных из JSON файла users
    """
    with open('data/users.json', 'r', encoding='utf=8') as file:
        data = json.load(file)
        return data


def get_orders_all():
    """
    Чтение данных из JSON файла orders
    """
    with open('data/orders.json', 'r', encoding='utf=8') as file:
        data = json.load(file)
        return data


def get_offers_all():
    """
    Чтение данных из JSON файла offers
    """
    with open('data/offers.json', 'r', encoding='utf=8') as file:
        data = json.load(file)
        return data
