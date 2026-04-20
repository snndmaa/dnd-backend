from rest_framework import serializers

from .models import Property


class PropertyListSerializer(serializers.ModelSerializer):
    PropertyName = serializers.CharField(source='name')
    PropertyCity = serializers.CharField(source='city')
    PropertyRate = serializers.SerializerMethodField()
    PropertyRatePerDay = serializers.DecimalField(source='rate_per_day', max_digits=10, decimal_places=2)
    PropertyRatePerMonth = serializers.DecimalField(source='rate_per_month', max_digits=10, decimal_places=2)
    PropertySide = serializers.CharField(source='side')

    PropertyOrderNumber = serializers.IntegerField(source='order_number')

    class Meta:
        model = Property
        fields = [
            'id',
            'PropertyName',
            'PropertyCity',
            'PropertySide',
            'PropertyRatePerDay',
            'PropertyRatePerMonth',
            'PropertyRate',
            'PropertyOrderNumber',
        ]

    def get_PropertyRate(self, obj):
        period = self.context.get('period', 'Short-Term')
        if period == 'Long-Term':
            return f'${obj.rate_per_month}/month' if obj.has_long_term else 'N/A'
        return f'${obj.rate_per_day}/day' if obj.has_short_term else 'N/A'


class PropertyDetailSerializer(serializers.ModelSerializer):
    propertyID = serializers.IntegerField(source='id')
    propertyName = serializers.CharField(source='name')
    propertyCity = serializers.CharField(source='city')
    propertySide = serializers.CharField(source='side')
    propertyDescription = serializers.CharField(source='description')
    propertyRateShortTerm = serializers.SerializerMethodField()
    propertyRateLongTerm = serializers.SerializerMethodField()
    propertyType = serializers.CharField(source='property_type')
    propertyGPS = serializers.SerializerMethodField()
    propertyBedrooms = serializers.IntegerField(source='bedrooms')
    propertyAC = serializers.SerializerMethodField()
    propertyInternet = serializers.SerializerMethodField()
    propertyHotWater = serializers.SerializerMethodField()
    propertyParking = serializers.SerializerMethodField()
    propertyPool = serializers.SerializerMethodField()
    propertyRoofAccess = serializers.SerializerMethodField()
    propertyBalcony = serializers.SerializerMethodField()
    propertyWashingMachine = serializers.SerializerMethodField()
    propertyWhatsapp = serializers.CharField(source='whatsapp')
    propertyCheckinDate = serializers.DateField(source='checkin_date', allow_null=True)
    propertyCheckoutDate = serializers.DateField(source='checkout_date', allow_null=True)
    propertyMinStay = serializers.IntegerField(source='min_stay')
    propertyMaxStay = serializers.IntegerField(source='max_stay')
    propertyImages = serializers.SerializerMethodField()
    propertyVideos = serializers.SerializerMethodField()
    propertyAvailability = serializers.SerializerMethodField()
    contactStatus = serializers.SerializerMethodField()
    contactUrl = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = [
            'propertyID',
            'propertyName',
            'propertyCity',
            'propertySide',
            'propertyDescription',
            'propertyAvailability',
            'propertyRateShortTerm',
            'propertyRateLongTerm',
            'propertyType',
            'propertyGPS',
            'propertyBedrooms',
            'propertyAC',
            'propertyInternet',
            'propertyHotWater',
            'propertyParking',
            'propertyPool',
            'propertyRoofAccess',
            'propertyBalcony',
            'propertyWashingMachine',
            'propertyWhatsapp',
            'propertyCheckinDate',
            'propertyCheckoutDate',
            'propertyMinStay',
            'propertyMaxStay',
            'propertyImages',
            'propertyVideos',
            'contactStatus',
            'contactUrl',
        ]

    def get_propertyRateShortTerm(self, obj):
        return f'${obj.rate_per_day}/day' if obj.has_short_term else 'N/A'

    def get_propertyRateLongTerm(self, obj):
        return f'${obj.rate_per_month}/month' if obj.has_long_term else 'N/A'

    def get_propertyGPS(self, obj):
        if obj.gps_lat is None or obj.gps_lng is None:
            return ''
        return f'{obj.gps_lat},{obj.gps_lng}'

    def get_propertyAvailability(self, obj):
        return [availability.month_year for availability in obj.availabilities.all()]

    def _boolean_text(self, value):
        return 'yes' if value else 'no'

    def get_propertyAC(self, obj):
        return self._boolean_text(obj.ac)

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

    def get_contactStatus(self, obj):
        user = self.context.get('request').user
        if not user or not user.is_authenticated or not user.is_active:
            return 'login_required'
        return 'whatsapp' if user.is_premium else 'payment_required'

    def get_contactUrl(self, obj):
        user = self.context.get('request').user
        if not user or not user.is_authenticated or not user.is_premium:
            return None
        number = ''.join(ch for ch in obj.whatsapp if ch.isdigit())
        return f'https://wa.me/{number}' if number else None

    def get_propertyImages(self, obj):
        images = []
        for i in range(1, 11):
            image_field = getattr(obj, f'image_{i}')
            if image_field:
                images.append({
                    'id': i,
                    'url': image_field.url,
                    'name': image_field.name.split('/')[-1]
                })
        return images

    def get_propertyVideos(self, obj):
        videos = []
        for i in range(1, 4):
            video_field = getattr(obj, f'video_{i}')
            if video_field:
                videos.append({
                    'id': i,
                    'url': video_field.url,
                    'name': video_field.name.split('/')[-1]
                })
        return videos
