from unicodedata import name
from core.models import *
from django.utils import timezone
from django.contrib.auth.models import User
from faker import Faker
import random
import os
import django


def create_post(N):
    fake = Faker()
    Flowers = ['Jasmine', 'Rose',
               'Areca catechu(pakku flower)', 'Avarampoo (Senna flower)',
               'kakada', 'Crossandra(Kangabaram)', 'Tulsi String', 'Yellow Chrysanthemum']
    for _ in range(N):
        category = random.randint(1, 4)
        flower_name = random.choice(Flowers)
        price = random.randint(250, 700)
        discount_price = price - random.randint(25, 100)
        is_auctioned = False
        description = fake.text()
        Posts.objects.create(flower_name=flower_name,
                             price=price, discount_price=discount_price,
                             category=Category.objects.get(
                                 id=category),
                             description=description,
                             is_auctioned=is_auctioned
                             )


if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'collegeblog.settings')
    django.setup()
    create_post(5)
