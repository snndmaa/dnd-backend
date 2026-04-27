from datetime import timedelta

from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator, MinValueValidator
from django.db import models
from django.utils import timezone


CITY_CHOICES = [
    ('GrandBaie', 'Grand Baie'),
    ('Cap Malheureux', 'Cap Malheureux'),
    ('Pereybere', 'Pereybere'),
    ('Trou aux Biches', 'Trou aux Biches'),
    ('Mont Choisy', 'Mont Choisy'),
    ('Pointe aux Piments', 'Pointe aux Piments'),
    ('Goodlands', 'Goodlands'),
    ('Calodyne', 'Calodyne'),
    
    # West Region
    ('Flic En Flac', 'Flic En Flac'),
    ('Tamarin', 'Tamarin'),
    ('Black River', 'Black River (Rivière Noire)'),
    ('La Gaulette', 'La Gaulette'),
    ('Le Morne', 'Le Morne'),
    ('Wolmar', 'Wolmar'),
    ('Cascavelle', 'Cascavelle'),
    
    # East Region
    ('Belle Mare', 'Belle Mare'),
    ('Trou d\'Eau Douce', 'Trou d\'Eau Douce'),
    ('Palmar', 'Palmar'),
    ('Flacq', 'Centre de Flacq'),
    ('Poste Lafayette', 'Poste Lafayette'),
    ('Quatre Cocos', 'Quatre Cocos'),
    
    # South Region
    ('Blue Bay', 'Blue Bay'),
    ('Mahebourg', 'Mahébourg'),
    ('Bel Ombre', 'Bel Ombre'),
    ('Souillac', 'Souillac'),
    ('Riambel', 'Riambel'),
    ('Pointe d\'Esny', 'Pointe d\'Esny'),
    
    # Center/Plains
    ('Curepipe', 'Curepipe'),
    ('Quatre Bornes', 'Quatre Bornes'),
    ('Vacoas', 'Vacoas-Phoenix'),
    ('Phoenix', 'Phoenix'),
    ('Beau Bassin', 'Beau Bassin-Rose Hill'),
    ('Rose Hill', 'Rose Hill'),
    ('Moka', 'Moka'),
    ('Reduit', 'Réduit'),
    
    # Other popular areas
    ('Port Louis', 'Port Louis (Capital)'),
    ('Pamplemousses', 'Pamplemousses'),
    ('Plaine Magnien', 'Plaine Magnien (Airport area)'),
    ('Quartier Militaire', 'Quartier Militaire'),
    ('Saint Pierre', 'Saint Pierre'),
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
    owner_photo = models.ImageField(upload_to='owners/photos/', blank=True, null=True)
    
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

    def is_available(self, start_date, end_date):
        """Check if property is available for given date range"""
        from django.db.models import Q
        # Check for overlapping bookings
        overlapping_bookings = self.bookings.filter(
            Q(check_in__lt=end_date, check_out__gt=start_date)
        ).exclude(status='cancelled')
        if overlapping_bookings.exists():
            return False
        # Check for blocked dates
        blocked_overlap = self.blocked_dates.filter(
            Q(start_date__lt=end_date, end_date__gt=start_date)
        )
        return not blocked_overlap.exists()

    def get_booked_dates(self):
        """Get all booked dates for this property as date strings"""
        booked_dates = set()
        for booking in self.bookings.exclude(status='cancelled'):
            current = booking.check_in
            while current <= booking.check_out:
                booked_dates.add(current.strftime('%Y-%m-%d'))
                current += timedelta(days=1)
        return booked_dates

    def get_blocked_dates(self):
        """Get all blocked dates for this property as date strings"""
        blocked_dates = set()
        for blocked in self.blocked_dates.all():
            current = blocked.start_date
            while current <= blocked.end_date:
                blocked_dates.add(current.strftime('%Y-%m-%d'))
                current += timedelta(days=1)
        return blocked_dates


class Booking(models.Model):
    """Individual booking for a property"""
    BOOKING_STATUS = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    customer_name = models.CharField(max_length=255)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20)

    check_in = models.DateField()
    check_out = models.DateField()
    guests = models.PositiveIntegerField(default=1)

    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=BOOKING_STATUS, default='pending')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['check_in']
        indexes = [
            models.Index(fields=['property', 'check_in', 'check_out']),
        ]

    def __str__(self):
        return f"{self.property.name} - {self.check_in} to {self.check_out}"

    def clean(self):
        """Validate booking dates"""
        if self.check_in >= self.check_out:
            raise ValidationError("Check-out must be after check-in")

        # Check min/max stay
        stay_duration = (self.check_out - self.check_in).days
        if stay_duration < self.property.min_stay:
            raise ValidationError(f"Minimum stay is {self.property.min_stay} nights")
        if stay_duration > self.property.max_stay:
            raise ValidationError(f"Maximum stay is {self.property.max_stay} nights")

        # Check availability (skip for cancelled bookings)
        if self.status != 'cancelled' and self.pk is None:
            if not self.property.is_available(self.check_in, self.check_out):
                raise ValidationError("Property is not available for these dates")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class BlockedDate(models.Model):
    """Manually block dates when property is unavailable (maintenance, etc.)"""
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='blocked_dates'
    )
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['start_date']

    def __str__(self):
        return f"{self.property.name} blocked: {self.start_date} to {self.end_date}"
