from django.contrib import admin
from django.utils.html import format_html
from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'loyalty_points', 'vip_badge', 'total_orders', 'created_at']
    list_filter = ['is_vip', 'created_at']
    search_fields = ['name', 'email', 'phone']
    readonly_fields = ['loyalty_points', 'is_vip', 'total_orders', 'total_spent', 'created_at', 'updated_at']
    ordering = ['name']

    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'email', 'phone', 'address', 'date_of_birth')
        }),
        ('Loyalty & Status', {
            'fields': ('loyalty_points', 'is_vip', 'total_orders', 'total_spent')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def vip_badge(self, obj):
        if obj.is_vip:
            return format_html(
                '<span style="background-color: #ffc107; color: black; padding: 3px 10px; border-radius: 3px; font-weight: bold;">VIP</span>'
            )
        return format_html(
            '<span style="background-color: #6c757d; color: white; padding: 3px 10px; border-radius: 3px;">Regular</span>'
        )
    vip_badge.short_description = 'Status'
