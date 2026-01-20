from django.contrib import admin
from django.utils.html import format_html
from .models import Ingredient, MenuItemIngredient, StockTransaction


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['name', 'current_stock', 'minimum_stock', 'unit', 'stock_status_badge', 'supplier', 'cost_per_unit']
    list_filter = ['unit', 'created_at']
    search_fields = ['name', 'supplier']
    ordering = ['name']

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return ['created_at', 'updated_at', 'is_low_stock']
        return ['created_at', 'updated_at']  # Adding a new object

    def get_fieldsets(self, request, obj=None):
        if obj:  # Editing an existing object
            return (
                ('Basic Information', {
                    'fields': ('name', 'unit', 'supplier')
                }),
                ('Stock Levels', {
                    'fields': ('current_stock', 'minimum_stock', 'is_low_stock', 'last_restocked')
                }),
                ('Pricing', {
                    'fields': ('cost_per_unit',)
                }),
                ('Timestamps', {
                    'fields': ('created_at', 'updated_at'),
                    'classes': ('collapse',)
                }),
            )
        else:  # Adding a new object
            return (
                ('Basic Information', {
                    'fields': ('name', 'unit', 'supplier')
                }),
                ('Stock Levels', {
                    'fields': ('current_stock', 'minimum_stock', 'last_restocked')
                }),
                ('Pricing', {
                    'fields': ('cost_per_unit',)
                }),
            )

    def stock_status_badge(self, obj):
        if obj.pk and obj.is_low_stock:
            return format_html(
                '<span style="background-color: #dc3545; color: white; padding: 3px 10px; border-radius: 3px;">LOW STOCK</span>'
            )
        return format_html(
            '<span style="background-color: #28a745; color: white; padding: 3px 10px; border-radius: 3px;">OK</span>'
        )
    stock_status_badge.short_description = 'Status'


@admin.register(MenuItemIngredient)
class MenuItemIngredientAdmin(admin.ModelAdmin):
    list_display = ['menu_item', 'ingredient', 'quantity_required', 'get_unit']
    list_filter = ['menu_item__category', 'ingredient']
    search_fields = ['menu_item__name', 'ingredient__name']
    ordering = ['menu_item']

    def get_unit(self, obj):
        return obj.ingredient.unit
    get_unit.short_description = 'Unit'


@admin.register(StockTransaction)
class StockTransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'ingredient', 'transaction_type', 'quantity', 'created_by', 'created_at']
    list_filter = ['transaction_type', 'created_at']
    search_fields = ['ingredient__name', 'notes']
    readonly_fields = ['created_at']
    ordering = ['-created_at']

    fieldsets = (
        ('Transaction Details', {
            'fields': ('ingredient', 'transaction_type', 'quantity', 'created_by')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Timestamp', {
            'fields': ('created_at',)
        }),
    )
