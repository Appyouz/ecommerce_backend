from django.contrib import admin
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    fields = ('product', 'quantity', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')

    # extra forms to display initilly, set value = 0 if dont want empty forms
    extra = 0
    # Show raw ids for product if have many products
    raw_id_fields = ('product',)

class CartAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')

    # search_fields: Fields to include in the search bar
    # Search by username of the related user
    search_fields = ('user__username',)

    # inlines: Add the CartItemInline to display CartItems on the Cart detail page
    inlines = [CartItemInline]

    # readonly_fields: Make timestamps read-only
    readonly_fields = ('created_at', 'updated_at')


# Customize CartItem Admin Display
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'cart', 'product', 'quantity', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('product__name', 'cart__user__username') # Search by product name or user username
    readonly_fields = ('created_at', 'updated_at')



admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
