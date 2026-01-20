from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    readonly_fields = ['unit_price', 'total_price']
    fields = ['menu_item', 'quantity', 'special_instructions', 'unit_price', 'total_price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'status', 'table_number', 'formatted_total', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['customer__name', 'customer__email']
    readonly_fields = ['subtotal', 'tax', 'total', 'created_at', 'updated_at']
    inlines = [OrderItemInline]
    ordering = ['-created_at']

    fieldsets = (
        ('Order Information', {
            'fields': ('customer', 'status', 'table_number', 'notes')
        }),
        ('Order Items', {
            'description': 'Add items to this order below. Totals will be calculated automatically.',
            'fields': ()
        }),
        ('Billing Summary', {
            'fields': ('discount', 'subtotal', 'tax', 'total'),
            'description': 'Totals are calculated automatically based on order items.'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if obj.items.exists():
            obj.calculate_totals()

    def save_formset(self, request, form, formset, change):
        """Save the formset and recalculate totals"""
        instances = formset.save(commit=False)
        for instance in instances:
            instance.save()
        for obj in formset.deleted_objects:
            obj.delete()
        formset.save_m2m()

        # Recalculate order totals after items are saved
        if form.instance.pk and form.instance.items.exists():
            form.instance.calculate_totals()

    def formatted_total(self, obj):
        return f"₹{obj.total}"
    formatted_total.short_description = 'Total'
    formatted_total.admin_order_field = 'total'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'menu_item', 'quantity', 'unit_price', 'total_price']
    list_filter = ['created_at']
    search_fields = ['order__id', 'menu_item__name']
    readonly_fields = ['unit_price', 'total_price', 'created_at']
