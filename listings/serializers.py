from rest_framework import serializers

from .models import Property


class PropertyListSerializer(serializers.ModelSerializer):
    PropertyName = serializers.CharField(source='name')
    PropertyAddress = serializers.CharField(source='address')
    propertyType = serializers.CharField(source='type')
    propertyBedrooms = serializers.IntegerField(source='bedrooms')
    propertyAC = serializers.BooleanField(source='ac')
    PropertyRate = serializers.SerializerMethodField()
    PropertyRatePerDay = serializers.DecimalField(source='rate_per_day', max_digits=10, decimal_places=2)
    PropertyRatePerMonth = serializers.DecimalField(source='rate_per_month', max_digits=10, decimal_places=2)
    # PropertySide = serializers.CharField(source='side')
    PropertyOrderNumber = serializers.IntegerField(source='order_number')
    PropertyMainPhoto = serializers.ImageField(source='main_photo', allow_null=True)

    class Meta:
        model = Property
        fields = [
            'id',
            'PropertyName',
            'PropertyAddress',
            'propertyType',
            'propertyBedrooms',
            'propertyAC',
            # 'PropertySide',
            'PropertyRatePerDay',
            'PropertyRatePerMonth',
            'PropertyRate',
            'PropertyOrderNumber',
            'PropertyMainPhoto',

        ]

    def get_PropertyRate(self, obj):
        period = self.context.get('period', 'Short-Term')
        if period == 'Long-Term':
            return f'${obj.rate_per_month}/month' if obj.has_long_term else 'N/A'
        return f'${obj.rate_per_day}/day' if obj.has_short_term else 'N/A'


from rest_framework import serializers
from django.conf import settings

class PropertyDetailSerializer(serializers.ModelSerializer):
    propertyID = serializers.IntegerField(source='id')
    propertyName = serializers.CharField(source='name')
    propertyCity = serializers.CharField(source='city')
    propertySide = serializers.CharField(source='side')
    propertyDescription = serializers.CharField(source='description')
    propertyAddress = serializers.CharField(source='address')
    propertyRateShortTerm = serializers.SerializerMethodField()
    propertyRateLongTerm = serializers.SerializerMethodField()
    propertyType = serializers.CharField(source='type')
    propertyGPS = serializers.SerializerMethodField()
    propertyBedrooms = serializers.IntegerField(source='bedrooms')
    propertyLanguages = serializers.CharField(source='languages')
    propertyAC = serializers.SerializerMethodField()
    propertyTV = serializers.SerializerMethodField()
    propertyMicrowave = serializers.SerializerMethodField()
    propertyBBQFacility = serializers.SerializerMethodField()
    propertyInternet = serializers.SerializerMethodField()
    propertyHotWater = serializers.SerializerMethodField()
    propertyParking = serializers.SerializerMethodField()
    propertyPool = serializers.SerializerMethodField()
    propertyRoofAccess = serializers.SerializerMethodField()
    propertyBalcony = serializers.SerializerMethodField()
    propertyWashingMachine = serializers.SerializerMethodField()
    propertyWhatsapp = serializers.CharField(source='whatsapp')
    propertyMinStay = serializers.IntegerField(source='min_stay')
    propertyBookedDates = serializers.SerializerMethodField()
    propertyBlockedDates = serializers.SerializerMethodField()
    propertyMaxStay = serializers.IntegerField(source='max_stay')
    propertyImages = serializers.SerializerMethodField()
    propertyVideo = serializers.URLField(source='video', allow_blank=True)
    propertyOwnerName = serializers.CharField(source='owner_name', allow_blank=True)
    propertyOwnerPhoto = serializers.SerializerMethodField()  # Changed to method for absolute URL
    contactUrl = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = [
            'propertyID',
            'propertyName',
            'propertyCity',
            'propertySide',
            'propertyDescription',
            'propertyAddress',
            'propertyRateShortTerm',
            'propertyRateLongTerm',
            'propertyType',
            'propertyGPS',
            'propertyBedrooms',
            'propertyLanguages',
            'propertyAC',
            'propertyTV',
            'propertyMicrowave',
            'propertyBBQFacility',
            'propertyInternet',
            'propertyHotWater',
            'propertyParking',
            'propertyPool',
            'propertyRoofAccess',
            'propertyBalcony',
            'propertyWashingMachine',
            'propertyWhatsapp',
            'propertyMinStay',
            'propertyMaxStay',
            'propertyBookedDates',
            'propertyBlockedDates',
            'propertyImages',
            'propertyVideo',
            'propertyOwnerName',
            'propertyOwnerPhoto',
            'contactUrl',
        ]

    def get_full_url(self, request, path):
        """Helper method to get full absolute URL"""
        if not path:
            return None
        if request:
            return request.build_absolute_uri(path)
        return path

    def get_propertyRateShortTerm(self, obj):
        return f'${obj.rate_per_day}/day' if obj.has_short_term else 'N/A'

    def get_propertyRateLongTerm(self, obj):
        return f'${obj.rate_per_month}/month' if obj.has_long_term else 'N/A'

    def get_propertyGPS(self, obj):
        if obj.gps_lat is None or obj.gps_lng is None:
            return ''
        return f'{obj.gps_lat},{obj.gps_lng}'

    def _boolean_text(self, value):
        return 'yes' if value else 'no'

    def get_propertyAC(self, obj):
        return self._boolean_text(obj.ac)

    def get_propertyTV(self, obj):
        return self._boolean_text(obj.tv)

    def get_propertyMicrowave(self, obj):
        return self._boolean_text(obj.microwave)

    def get_propertyBBQFacility(self, obj):
        return self._boolean_text(obj.bbq_facility)

    def get_propertyInternet(self, obj):
        return self._boolean_text(obj.internet)

    def get_propertyHotWater(self, obj):
        return self._boolean_text(obj.hot_water)

    def get_propertyParking(self, obj):
        return self._boolean_text(obj.parking)

    def get_propertyPool(self, obj):
        return self._boolean_text(obj.pool)

    def get_propertyRoofAccess(self, obj):
        return self._boolean_text(obj.roof_access)

    def get_propertyBalcony(self, obj):
        return self._boolean_text(obj.balcony)

    def get_propertyWashingMachine(self, obj):
        return self._boolean_text(obj.washing_machine)

    def get_propertyBookedDates(self, obj):
        """Get all booked dates for the property"""
        return list(obj.get_booked_dates())

    def get_propertyBlockedDates(self, obj):
        """Get all blocked dates for the property"""
        return list(obj.get_blocked_dates())

    def get_contactUrl(self, obj):
        number = ''.join(ch for ch in obj.whatsapp if ch.isdigit())
        return f'https://wa.me/{number}' if number else None

    def get_propertyOwnerPhoto(self, obj):
        """Return full URL for owner photo"""
        if obj.owner_photo:
            request = self.context.get('request')
            return self.get_full_url(request, obj.owner_photo.url)
        return None

    def get_propertyImages(self, obj):
        """Return organized images by category with full absolute URLs"""
        request = self.context.get('request')
        
        images = {
            'main': None,
            'living_room': None,
            'bedroom': None,
            'building': None,
            'land': None,
            'all_images': []  # For backward compatibility or easy access
        }
        
        # Helper to add image with full URL
        def add_image(category, image_field):
            if image_field:
                full_url = self.get_full_url(request, image_field.url)
                if full_url:
                    image_data = {
                        'category': category,
                        'url': full_url,  # Now returns full absolute URL
                        'name': image_field.name.split('/')[-1] if image_field.name else None
                    }
                    images[category] = image_data
                    images['all_images'].append(image_data)
        
        # Add all images
        add_image('main', obj.main_photo)
        add_image('living_room', obj.living_room_photo)
        add_image('bedroom', obj.bedroom_photo)
        add_image('building', obj.building_photo)
        add_image('land', obj.land_photo)
        
        return images