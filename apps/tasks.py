from time import sleep

from celery import shared_task

from apps.models import Category, Product
import random


@shared_task
def task_one(x, y):
    sleep(3)
    return x + y


def add_data():
    products = []
    for i in range(30):
        name = f"Product -{i}"
        category = random.randint(1, 10)
        price = random.randint(10, 100) * 10
        quantity = random.randint(0, 100)
        description = f"Descriptiom -{i}"
        spec = {"rangi": f"rang-{i}"}
        discount = random.randint(1, 5) * 10
        products.append(Product(name=name, category_id=category, price=price, quantity=quantity, description=description, spec=spec, discount=discount))

    Product.objects.bulk_create(products)
