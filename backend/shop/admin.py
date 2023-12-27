from django.contrib import admin

from .models import Category, Order, Product, Review, User


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]
    prepopulated_fields = {"slug": ["name"]}
    fields = ["name", "slug", "description", "parent_category"]


@admin.register(Product)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Review)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(User)
class CategoryAdmin(admin.ModelAdmin):
    pass
