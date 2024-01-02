from django.contrib import admin

from .models import Category, Product, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]
    prepopulated_fields = {"slug": ["name"]}
    fields = ["name", "image", "slug", "description", "parent_category"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["title", "price", "updated_at", "categories"]
    prepopulated_fields = {"slug": ["title"]}


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass
