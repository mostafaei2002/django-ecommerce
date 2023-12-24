from django.contrib import admin

from .models import Order, Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ["name"]
    prepopulated_fields = {"slug": ["name"]}
    exclude = ["sales"]


# Register your models here.
admin.site.register(Order)
admin.site.register(Product, ProductAdmin)
