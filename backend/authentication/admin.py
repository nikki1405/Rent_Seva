from django.contrib import admin
from .models import EstimateHistory

@admin.register(EstimateHistory)
class EstimateHistoryAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'location', 'bhk', 'sqft', 'predicted_rent', 'created_at']
    list_filter = ['location', 'bhk', 'created_at']
    search_fields = ['user_id', 'location']
    ordering = ['-created_at']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user_id',)
        }),
        ('Property Details', {
            'fields': ('location', 'bhk', 'sqft')
        }),
        ('Prediction Details', {
            'fields': ('predicted_rent', 'created_at')
        })
    )
