from django.contrib import admin
from .models import Product, Category


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'created_at', 'updated_at')

    list_filter = ('category', 'created_at', 'updated_at')

    search_fields = ('name', 'description', 'category__name') # Use '__' to search related fields


    date_hierarchy = 'created_at'

    ordering = ('-created_at',) # Order by creation date, newest first



class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at')

    search_fields = ('name', 'description')

    ordering = ('name',) # Order categories alphabetically by name


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
