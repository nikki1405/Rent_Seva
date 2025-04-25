from django.contrib import admin
from .models import RentPrediction
from django.utils.html import format_html

@admin.register(RentPrediction)
class RentPredictionAdmin(admin.ModelAdmin):
    """
    Admin configuration for RentPrediction model.
    
    Provides a customized admin interface for managing rent predictions,
    with filtering, search, and formatted display of monetary values.
    """
    
    list_display = ['user_id', 'location', 'bhk_display', 'sqft_display', 'predicted_rent_display', 'created_at']
    list_filter = ['location', 'bhk', ('predicted_rent', admin.EmptyFieldListFilter), 'created_at']
    search_fields = ['user_id', 'location']
    ordering = ['-created_at']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    
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
    
    def bhk_display(self, obj):
        """Format BHK display with suffix"""
        return f"{obj.bhk} BHK"
    bhk_display.short_description = 'BHK'
    
    def sqft_display(self, obj):
        """Format square footage with commas and suffix"""
        return f"{obj.sqft:,.0f} sq.ft"
    sqft_display.short_description = 'Area'
    
    def predicted_rent_display(self, obj):
        """Format predicted rent as currency with color coding"""
        color = '#28a745' if obj.predicted_rent > 0 else '#dc3545'
        return format_html(
            '<span style="color: {};">₹{:,.2f}</span>',
            color,
            obj.predicted_rent
        )
    predicted_rent_display.short_description = 'Predicted Rent'
    
    def get_readonly_fields(self, request, obj=None):
        """Make certain fields readonly if editing existing object"""
        if obj:  # Editing an existing object
            return self.readonly_fields + ('user_id', 'predicted_rent')
        return self.readonly_fields
