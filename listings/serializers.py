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
    propertyType = serializers.CharField(source='type')
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
    propertyVideo = serializers.URLField(source='video', allow_blank=True)
    contactUrl = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = [
            'propertyID',
            'propertyName',
            'propertyCity',
            'propertySide',
            'propertyDescription',
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
            'propertyVideo',
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

    # def get_contactStatus(self, obj):
    #     user = self.context.get('request').user
    #     if not user or not user.is_authenticated or not user.is_active:
    #         return 'login_required'
    #     return 'whatsapp' if user.is_premium else 'payment_required'

    def get_contactUrl(self, obj):
        # user = self.context.get('request').user
        # if not user or not user.is_authenticated or not user.is_premium:
        #     return None
        number = ''.join(ch for ch in obj.whatsapp if ch.isdigit())
        return f'https://wa.me/{number}' if number else None

    def get_propertyImages(self, obj):
        """Return organized images by category"""
        images = {
            'main': None,
            'living_room': None,
            'bedroom': None,
            'vc': None,
            'building': None,
            'land': None,
            'all_images': []  # For backward compatibility or easy access
        }
        
        # Main photo
        if obj.main_photo:
            images['main'] = {
                'category': 'main',
                'url': obj.main_photo.url,
                'name': obj.main_photo.name.split('/')[-1] if obj.main_photo.name else None
            }
            images['all_images'].append(images['main'])
        
        # Living room photo
        if obj.living_room_photo:
            images['living_room'] = {
                'category': 'living_room',
                'url': obj.living_room_photo.url,
                'name': obj.living_room_photo.name.split('/')[-1] if obj.living_room_photo.name else None
            }
            images['all_images'].append(images['living_room'])
        
        # Bedroom photo
        if obj.bedroom_photo:
            images['bedroom'] = {
                'category': 'bedroom',
                'url': obj.bedroom_photo.url,
                'name': obj.bedroom_photo.name.split('/')[-1] if obj.bedroom_photo.name else None
            }
            images['all_images'].append(images['bedroom'])
        
        # VC (Virtual Conference?) photo
        if obj.vc_photo:
            images['vc'] = {
                'category': 'vc',
                'url': obj.vc_photo.url,
                'name': obj.vc_photo.name.split('/')[-1] if obj.vc_photo.name else None
            }
            images['all_images'].append(images['vc'])
        
        # Building photo
        if obj.building_photo:
            images['building'] = {
                'category': 'building',
                'url': obj.building_photo.url,
                'name': obj.building_photo.name.split('/')[-1] if obj.building_photo.name else None
            }
            images['all_images'].append(images['building'])
        
        # Land photo
        if obj.land_photo:
            images['land'] = {
                'category': 'land',
                'url': obj.land_photo.url,
                'name': obj.land_photo.name.split('/')[-1] if obj.land_photo.name else None
            }
            images['all_images'].append(images['land'])
        
        return images
