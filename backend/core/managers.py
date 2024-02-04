from django.db import models


class CategoryManager(models.Manager):

    def get_top_level_categories(self):
        top_level_categories = self.filter(parent_category=None)
        return top_level_categories
