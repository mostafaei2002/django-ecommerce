import random

from accounts.models import User
from core.models import Product, Review
from django.core.management.base import BaseCommand
from django.template.defaultfilters import slugify
from faker import Faker


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("num_reviews", type=int)

    def handle(self, *args, **options):
        num_products = options["num_reviews"]
        fake = Faker()
        all_products = list(Product.objects.all())
        all_reviews = list(Product.objects.all())

        for _ in range(num_products):
            review_rating = round(random.randint(1, 5))
            review_comment = fake.text(max_nb_chars=150)
            review_product = random.choice(all_products)
            review_user = random.choice(all_reviews)

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
            Review.objects.create(
                rating=review_rating,
                comment=review_comment,
                product=review_product,
                user=review_user,
            )
