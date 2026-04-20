from django.contrib import admin

from .models import Property


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'side', 'property_type', 'order_number')
    list_filter = ('city', 'side', 'property_type')
    search_fields = ('name', 'description')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'city', 'side', 'description', 'order_number')
        }),
        ('Pricing', {
            'fields': ('rate_per_day', 'rate_per_month')
        }),
        ('Property Details', {
            'fields': ('property_type', 'gps_lat', 'gps_lng', 'property_address', 'property_country', 'property_languages', 'checkin_date', 'checkout_date', 'min_stay', 'max_stay', 'bedrooms')
        }),
        ('Amenities', {
            'fields': ('ac', 'internet', 'hot_water', 'parking', 'pool', 'roof_access', 'balcony', 'washing_machine')
        }),
        ('Contact', {
            'fields': ('whatsapp',)
        }),
        ('Images', {
            'fields': ('image_1', 'image_2', 'image_3', 'image_4', 'image_5', 'image_6', 'image_7', 'image_8', 'image_9', 'image_10'),
            'classes': ('collapse',)
        }),
        ('Videos', {
            'fields': ('video_1'),
            'classes': ('collapse',)
        }),
    )

