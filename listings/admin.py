from django.contrib import admin

from .models import Property


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'side', 'type', 'order_number')
    list_filter = ('city', 'side', 'type', 'owner_name')
    search_fields = ('name', 'description', 'owner_name')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'city', 'side', 'description', 'order_number')
        }),
        ('Pricing', {
            'fields': ('rate_per_day', 'rate_per_month')
        }),
        ('Property Details', {
            'fields': ('type', 'gps_lat', 'gps_lng', 'address', 'country', 'languages', 'checkin_date', 'checkout_date', 'min_stay', 'max_stay', 'bedrooms', 'owner_name')
        }),
        ('Amenities', {
            'fields': ('ac', 'internet', 'hot_water', 'parking', 'pool', 'roof_access', 'balcony', 'washing_machine')
        }),
        ('Contact', {
            'fields': ('whatsapp',)
        }),
        ('Images', {
            'fields': ('main_photo', 'living_room_photo', 'bedroom_photo', 'vc_photo', 'building_photo', 'land_photo'),
            'classes': ('collapse',)
        }),
        ('Videos', {
            'fields': ('video',),
            'classes': ('collapse',)
        }),
    )

