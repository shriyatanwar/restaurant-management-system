from django.contrib import admin
from .models import Table, Reservation


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ['table_number', 'capacity', 'is_available', 'location', 'created_at']
    list_filter = ['is_available', 'capacity']
    search_fields = ['table_number', 'location']
    list_editable = ['is_available']
    ordering = ['table_number']


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'table', 'reservation_date', 'reservation_time', 'number_of_guests', 'status']
    list_filter = ['status', 'reservation_date', 'created_at']
    search_fields = ['customer__name', 'customer__email', 'table__table_number']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-reservation_date', '-reservation_time']

    fieldsets = (
        ('Reservation Details', {
            'fields': ('customer', 'table', 'reservation_date', 'reservation_time', 'number_of_guests')
        }),
        ('Status & Requests', {
            'fields': ('status', 'special_requests')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        try:
            obj.full_clean()
            super().save_model(request, obj, form, change)
        except Exception as e:
            from django.contrib import messages
            messages.error(request, str(e))
