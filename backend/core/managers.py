import logging

from django.db import models
from django.db.models import Avg, Count, Sum

logger = logging.getLogger("django")


class CategoryManager(models.Manager):

    def get_top_level_categories(self):
        top_level_categories = self.filter(parent_category=None)
        return top_level_categories


class ProductQuerySet(models.QuerySet):

    def order_items(self, by):
        if by == "price":
            return self.order_by("-price")
        elif by == "created_at":
            return self.order_by("-created_at")
        elif by == "num_ratings":
            return self.annotate(num_ratings=Count("reviews")).order_by("-num_ratings")
        elif by == "rating":
            return self.annotate(avg_rating=Avg("reviews__rating")).order_by(
                "-avg_rating"
            )
        elif by == "sales":
            return self.annotate(num_sales=Sum("order_item__quantity")).order_by(
                "-num_sales"
            )
        else:
            return self
