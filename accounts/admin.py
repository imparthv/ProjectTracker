from django.contrib import admin
from .models import Account

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    ordering = ["id",]
    list_display = ["email", "first_name", "last_name", "is_staff"]
    search_fields = ["email", "first_name", "last_name"]

