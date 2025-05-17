from django.contrib import admin
from django.contrib import messages
from .models import Order, OrderItem



# TabularInline displays related objects in a table format
class OrderItemInline(admin.TabularInline):
    # Specify the model that this inline is for (the related model)
    model = OrderItem
    # Fields to display for each OrderItem in the inline table
    # Include fields copied from the product at the time of order
    fields = ('product', 'product_name', 'product_price', 'quantity', 'get_total_item_price', 'created_at')
    # Make these fields read-only in the inline display
    readonly_fields = ('product_name', 'product_price', 'get_total_item_price', 'created_at')
    extra = 0
    raw_id_fields = ('product',)


# Customize Order Admin Display 
class OrderAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user', 'total_amount', 'status', 'created_at', 'updated_at')

    # list_filter: Fields to add a filter sidebar
    list_filter = ('status', 'created_at', 'updated_at')

    # search_fields: Fields to include in the search bar
    # Search by order ID or username of the related user
    search_fields = ('id', 'user__username')

    # inlines: Add the OrderItemInline to display OrderItems on the Order detail page
    inlines = [OrderItemInline]

    # readonly_fields: Make fields that should not be changed manually read-only
    readonly_fields = ('user', 'total_amount', 'created_at', 'updated_at')

   # Group fields on the detail page
    fieldsets = (
        (None, {
            'fields': ('user', 'total_amount', 'status')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',), # Optional: collapse this section
        }),
    )
    
    def mark_as_processing(self, request, queryset):
        """
        Admin action to mark selected orders as 'Processing'.
        """
        updated_count = queryset.update(status='Processing')

        if updated_count == 1:
            message = "1 order was successfully marked as Processing."
        else:
            message = f"{updated_count} orders were successfully marked as Processing."
        
        self.message_user(request, message, messages.SUCCESS) 

        
    mark_as_processing.short_description = "Mark selected orders as Processing"
    actions = [mark_as_processing]



#Customize OrderItem Admin Display 
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'order', 'product', 'product_name', 'quantity', 'get_total_item_price', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('product_name', 'order__user__username') 
    readonly_fields = ('product_name', 'product_price', 'get_total_item_price', 'created_at', 'updated_at')


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
