import random

from core.models import Category, Product
from django.core.management.base import BaseCommand
from django.template.defaultfilters import slugify
from faker import Faker


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("num_products", type=int)

    def handle(self, *args, **options):
        fake = Faker()
        num_products = options["num_products"]

        for _ in range(num_products):
            product_title = fake.text(max_nb_chars=20)
            product_summary = fake.text(max_nb_chars=150)
            product_description = fake.text(max_nb_chars=1000)
            product_price = round(random.uniform(10.00, 99.99), 2)
            product_category = random.choice(list(Category.objects.all()))

            # print(
            #     product_title,
            #     "\n",
            #     product_summary,
            #     "\n",
            #     product_description,
            #     "\n",
            #     product_price,
            #     "\n",
            #     product_category,
            # )
            Product.objects.create(
                title=product_title,
                slug=slugify(product_title),
                image="products/default.png",
                summary=product_summary,
                description=product_description,
                price=product_price,
                categories=product_category,
            )
