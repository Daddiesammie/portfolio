from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('reference', 'user', 'project', 'amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('reference', 'user__username', 'project__title')
    readonly_fields = ('reference', 'created_at', 'updated_at')
    
    def has_delete_permission(self, request, obj=None):
        return True  # Enable deletion for all payments
    
    def has_change_permission(self, request, obj=None):
        if obj and obj.status == 'success':
            return True  # Enable editing even for successful payments
        return True
