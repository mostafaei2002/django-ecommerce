from django.contrib import admin

from .models import Address, User

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "first_name", "last_name"]


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ["province"]
