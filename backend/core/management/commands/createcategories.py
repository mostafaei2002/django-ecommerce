import random

from core.models import Category
from django.core.management.base import BaseCommand
from django.template.defaultfilters import slugify

category_names = [
    "Education",
    "Anime",
    "Movie",
    "Shoes",
    "Clothing",
    "Pants",
    "Swimwear",
    "Electronics",
    "TV",
    "Computer Parts",
    "Laptop",
    "Games",
    "Technology",
    "Refrigerator",
    "Home appliances",
]


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("num_categories", type=int)

    def handle(self, *args, **options):
        num_categories = options["num_categories"]

        for _ in range(num_categories):
            category_title = random.choice(category_names)
            all_categories = list(Category.objects.all())
            parent_category = random.choice([*all_categories, None, None])

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
            Category.objects.create(
                name=category_title,
                slug=slugify(category_title),
                parent_category=parent_category,
                image="categories/default.png",
            )
