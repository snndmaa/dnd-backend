from django.core.validators import FileExtensionValidator, MinValueValidator
from django.db import models


CITY_CHOICES = [
    ('All in Mauritius', 'All in Mauritius'),
    ('Flic En Flac', 'Flic En Flac'),
    ('GrandBaie', 'GrandBaie'),
    ('Tamarin', 'Tamarin'),
]

SIDE_CHOICES = [
    ('West', 'West'),
    ('North', 'North'),
    ('East', 'East'),
    ('South', 'South'),
    ('Center', 'Center'),
]

PROPERTY_TYPE_CHOICES = [
    ('Appartment', 'Appartment'),
    ('Villa', 'Villa'),
]


class Property(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=PROPERTY_TYPE_CHOICES)
    city = models.CharField(max_length=32, choices=CITY_CHOICES)
    side = models.CharField(max_length=16, choices=SIDE_CHOICES)
    description = models.TextField(blank=True)
    order_number = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    rate_per_day = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    rate_per_month = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    gps_lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    gps_lng = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    address = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=100, blank=True)
    languages = models.CharField(max_length=255, blank=True, help_text='Comma-separated list of languages')
    owner_name = models.CharField(max_length=255, blank=True)
    
    checkin_date = models.DateField(null=True, blank=True)
    checkout_date = models.DateField(null=True, blank=True)
    min_stay = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)], help_text='Minimum nights stay')
    max_stay = models.PositiveIntegerField(default=30, validators=[MinValueValidator(1)], help_text='Maximum nights stay')
    bedrooms = models.PositiveIntegerField(default=0)
    ac = models.BooleanField(default=False)
    internet = models.BooleanField(default=False)
    hot_water = models.BooleanField(default=False)
    parking = models.BooleanField(default=False)
    pool = models.BooleanField(default=False)
    roof_access = models.BooleanField(default=False)
    balcony = models.BooleanField(default=False)
    washing_machine = models.BooleanField(default=False)
    whatsapp = models.CharField(max_length=32, blank=True)
    tv=models.BooleanField(default=False)
    microwave=models.BooleanField(default=False)
    bbq_facility=models.BooleanField(default=False)

    # Media fields
    main_photo = models.ImageField(upload_to='properties/images/main/', blank=True, null=True)
    living_room_photo = models.ImageField(upload_to='properties/images/living_room/', blank=True, null=True)
    bedroom_photo = models.ImageField(upload_to='properties/images/bedroom/', blank=True, null=True)
    vc_photo = models.ImageField(upload_to='properties/images/vc/', blank=True, null=True)
    building_photo = models.ImageField(upload_to='properties/images/building/', blank=True, null=True)
    land_photo = models.ImageField(upload_to='properties/images/land/', blank=True, null=True)

    video = models.URLField(blank=True, max_length=500)

    class Meta:
        ordering = ['order_number']

    def __str__(self):
        return f'{self.name} — {self.city}'

    @property
    def has_short_term(self):
        return self.rate_per_day > 0

    @property
    def has_long_term(self):
        return self.rate_per_month > 0
