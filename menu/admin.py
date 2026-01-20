from django.contrib import admin
from .models import Category, MenuItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['name']


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'formatted_price', 'is_available', 'is_vegetarian', 'is_vegan', 'preparation_time']
    list_filter = ['category', 'is_available', 'is_vegetarian', 'is_vegan', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_available']
    ordering = ['category', 'name']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'category', 'price', 'image')
        }),
        ('Availability & Dietary', {
            'fields': ('is_available', 'is_vegetarian', 'is_vegan', 'preparation_time')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def formatted_price(self, obj):
        return f"₹{obj.price}"
    formatted_price.short_description = 'Price'
    formatted_price.admin_order_field = 'price'
