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
    city = models.CharField(max_length=32, choices=CITY_CHOICES)
    side = models.CharField(max_length=16, choices=SIDE_CHOICES)
    description = models.TextField(blank=True)
    order_number = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    rate_per_day = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    rate_per_month = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPE_CHOICES)
    gps_lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    gps_lng = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    property_address = models.CharField(max_length=255, blank=True)
    property_country = models.CharField(max_length=100, blank=True)
    property_languages = models.CharField(max_length=255, blank=True, help_text='Comma-separated list of languages')
    
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
    image_1 = models.ImageField(upload_to='properties/images/', blank=True, null=True)
    image_2 = models.ImageField(upload_to='properties/images/', blank=True, null=True)
    image_3 = models.ImageField(upload_to='properties/images/', blank=True, null=True)
    image_4 = models.ImageField(upload_to='properties/images/', blank=True, null=True)
    image_5 = models.ImageField(upload_to='properties/images/', blank=True, null=True)
    image_6 = models.ImageField(upload_to='properties/images/', blank=True, null=True)
    image_7 = models.ImageField(upload_to='properties/images/', blank=True, null=True)
    image_8 = models.ImageField(upload_to='properties/images/', blank=True, null=True)
    image_9 = models.ImageField(upload_to='properties/images/', blank=True, null=True)
    image_10 = models.ImageField(upload_to='properties/images/', blank=True, null=True)

    video_1 = models.FileField(
        upload_to='properties/videos/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['mp4', 'avi', 'mov', 'mkv'])]
    )

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
