import os
import django
import random
from decimal import Decimal
from datetime import date, timedelta
from faker import Faker
from django.core.files.base import ContentFile
from io import BytesIO
import requests
from PIL import Image, ImageDraw, ImageFont
import uuid

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dnd_backend.settings')
django.setup()

from listings.models import Property, CITY_CHOICES, SIDE_CHOICES, PROPERTY_TYPE_CHOICES
from listings.models import Booking, BlockedDate

# Initialize Faker
fake = Faker()

# Realistic Mauritian property names
PROPERTY_NAMES = {
    'Villa': [
        "Villa du Soleil", "Villa Belle Vue", "Villa des Palmiers", "Villa Hibiscus",
        "Villa Océane", "Villa des Îles", "Villa Tropicale", "Villa Paradis",
        "Villa Alizée", "Villa Coco", "Villa des Anges", "Villa Harmony",
        "Villa Serenity", "Villa Horizon", "Villa Lagoon", "Villa Sakura"
    ],
    'Appartment': [
        "Sunset Apartments", "Beachfront Residences", "Garden View Apartment",
        "Sea Breeze Complex", "Palm Grove Residence", "Azure Bay Apartments",
        "Tropical Nest", "Harbour View Loft", "Lagoon Heights", "Coastal Living",
        "Island Pearl", "Bamboo Court", "Flamboyant Suites", "Coral Reef Apartments"
    ]
}

# YouTube video URLs (Mauritius travel/property related)
YOUTUBE_VIDEOS = [
    "https://www.youtube.com/watch?v=Xt1lka1y7k4",
    "https://www.youtube.com/watch?v=zDgBz2gXV8w",
    "https://www.youtube.com/watch?v=Kj9fIK70KfM",
    "https://www.youtube.com/watch?v=wHR6HcLJK3M",
    "https://www.youtube.com/watch?v=8c2Kd-jPpxM",
    "https://www.youtube.com/watch?v=UvzE5K2K8YI",
    "https://www.youtube.com/watch?v=Q_9vYg5JfqM",
    "https://www.youtube.com/watch?v=3YrYq5Z9L6I",
    "https://www.youtube.com/watch?v=7MxP5V9jJlY",
    "https://www.youtube.com/watch?v=GxVzL9qL5jE",
]

# Realistic Mauritian names for owners
MAURITIAN_OWNER_NAMES = [
    "Jean-Pierre Robert", "Marie-Claire Lagesse", "Ashvin Ramtoola", "Sunita Boodhoo",
    "Alain Wong", "Isabelle de Rosnay", "Rajesh Boolaky", "Patricia Ah-Chuen",
    "Michel Vadamootoo", "Nalini Soodhun", "Philippe Etienne", "Catherine Li",
    "Dinesh Seebaluck", "Francoise Bax", "Yashvin Gungadin", "Veronique Koenig",
    "Ravi Beesoondial", "Christelle Mamet", "Sanjay Bhoyroo", "Anne-Laure Ng"
]

def download_person_photo(width=400, height=400):
    """Download a random person photo for owner from ThisPersonDoesNotExist or generate one"""
    try:
        # Using randomuser.me API for realistic person photos
        response = requests.get("https://randomuser.me/api/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            image_url = data['results'][0]['picture']['large']
            img_response = requests.get(image_url, timeout=10)
            
            if img_response.status_code == 200:
                img = Image.open(BytesIO(img_response.content))
                
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Resize to square
                img = img.resize((width, height), Image.Resampling.LANCZOS)
                
                img_byte_arr = BytesIO()
                img.save(img_byte_arr, format='JPEG', quality=85)
                img_byte_arr.seek(0)
                
                return ContentFile(img_byte_arr.getvalue(), name=f"owner_{uuid.uuid4().hex[:8]}.jpg")
    except Exception as e:
        print(f"  ⚠️  Could not download person photo: {e}")
    
    # Fallback: create a colored avatar with initials
    return create_avatar_placeholder(width, height)

def create_avatar_placeholder(width=400, height=400):
    """Create a colored avatar with person icon or initials"""
    # Random pleasant color
    colors = [
        (52, 152, 219), (46, 204, 113), (155, 89, 182), (241, 196, 15),
        (230, 126, 34), (231, 76, 60), (26, 188, 156), (52, 73, 94)
    ]
    color = random.choice(colors)
    img = Image.new('RGB', (width, height), color=color)
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("arial.ttf", int(width * 0.4))
    except:
        font = ImageFont.load_default()
    
    # Draw a simple person silhouette (circle for head, shape for body)
    center_x, center_y = width // 2, height // 2
    head_radius = int(width * 0.15)
    body_height = int(height * 0.25)
    
    # Draw head (circle)
    draw.ellipse([
        center_x - head_radius, center_y - head_radius - body_height//2,
        center_x + head_radius, center_y + head_radius - body_height//2
    ], fill='white', outline='white')
    
    # Draw body (rectangle)
    body_width = int(width * 0.25)
    draw.rectangle([
        center_x - body_width//2, center_y - body_height//4,
        center_x + body_width//2, center_y + body_height//2
    ], fill='white')
    
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)
    
    return ContentFile(img_byte_arr.getvalue(), name=f"owner_avatar_{uuid.uuid4().hex[:8]}.jpg")

def download_placeholder_image(category, width=1200, height=800):
    """Download a placeholder image from Unsplash or generate a colored one"""
    try:
        image_url = f"https://picsum.photos/id/{random.randint(1, 200)}/{width}/{height}"
        response = requests.get(image_url, timeout=10)
        
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            img_byte_arr = BytesIO()
            img.save(img_byte_arr, format='JPEG', quality=85)
            img_byte_arr.seek(0)
            
            return ContentFile(img_byte_arr.getvalue(), name=f"{category}_{uuid.uuid4().hex[:8]}.jpg")
    except Exception as e:
        print(f"  ⚠️  Could not download image for {category}: {e}")
    
    return create_colored_placeholder(category, width, height)

def create_colored_placeholder(category, width=1200, height=800):
    """Create a colored placeholder image with text"""
    colors = {
        'main_photo': (52, 152, 219),
        'living_room_photo': (46, 204, 113),
        'bedroom_photo': (155, 89, 182),
        'building_photo': (230, 126, 34),
        'land_photo': (39, 174, 96),
    }
    
    color = colors.get(category, (128, 128, 128))
    img = Image.new('RGB', (width, height), color=color)
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("arial.ttf", 60)
    except:
        font = ImageFont.load_default()
    
    text = category.replace('_', ' ').title()
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    
    draw.text((x, y), text, fill='white', font=font)
    
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)
    
    return ContentFile(img_byte_arr.getvalue(), name=f"{category}_{uuid.uuid4().hex[:8]}.jpg")

def generate_coordinates(city):
    """Generate realistic GPS coordinates for different cities"""
    coordinates = {
        'Flic En Flac': (Decimal('-20.279722'), Decimal('57.370833')),
        'GrandBaie': (Decimal('-20.009444'), Decimal('57.580278')),
        'Tamarin': (Decimal('-20.325000'), Decimal('57.373889')),
    }
    base_lat, base_lng = coordinates.get(city, (Decimal('-20.200000'), Decimal('57.500000')))
    
    lat_offset = Decimal(str(random.uniform(-0.05, 0.05)))
    lng_offset = Decimal(str(random.uniform(-0.05, 0.05)))
    
    return base_lat + lat_offset, base_lng + lng_offset

def generate_rate(property_type, side, is_monthly=False):
    """Generate realistic rates based on property type and side"""
    base_rates = {
        'Villa': {'day': (8000, 25000), 'month': (150000, 450000)},
        'Appartment': {'day': (3000, 12000), 'month': (50000, 200000)}
    }
    
    side_multiplier = {
        'West': 1.0, 'North': 1.2, 'East': 0.8, 'South': 0.7, 'Center': 0.9
    }
    
    rate_range = base_rates[property_type]['month' if is_monthly else 'day']
    base_rate = random.randint(*rate_range)
    multiplier = side_multiplier.get(side, 1.0)
    
    return Decimal(str(int(base_rate * multiplier / 100) * 100))

def generate_description(property_name, property_type, city, amenities):
    """Generate realistic property descriptions"""
    templates = [
        f"{property_name} is a beautiful {property_type.lower()} located in {city}, Mauritius. "
        f"This stunning property offers breathtaking views and modern amenities including {', '.join(amenities[:3])}.",
        
        f"Welcome to {property_name}, your perfect getaway in {city}. "
        f"This {property_type.lower()} combines luxury with comfort for an unforgettable stay. "
        f"Features include {', '.join(amenities[:4])}.",
        
        f"Experience the best of Mauritian hospitality at {property_name}. "
        f"Located in the heart of {city}, this {property_type.lower()} offers everything you need "
        f"including {', '.join(amenities[:3])} and more.",
        
        f"Escape to paradise at {property_name}. This charming {property_type.lower()} in {city} "
        f"features {', '.join(random.sample(amenities, min(4, len(amenities))))} and more. "
        f"Perfect for families and couples alike."
    ]
    
    return random.choice(templates)

def get_active_amenities(property_type, property_class='standard'):
    """Determine which amenities are available based on property type"""
    AMENITY_PATTERNS = {
        'Villa': {
            'ac': 0.9, 'internet': 0.95, 'hot_water': 1.0, 'parking': 0.95,
            'pool': 0.8, 'roof_access': 0.4, 'balcony': 0.85, 'washing_machine': 0.9,
            'tv': 0.95, 'microwave': 0.9, 'bbq_facility': 0.7
        },
        'Appartment': {
            'ac': 0.85, 'internet': 0.95, 'hot_water': 1.0, 'parking': 0.7,
            'pool': 0.5, 'roof_access': 0.2, 'balcony': 0.75, 'washing_machine': 0.85,
            'tv': 0.95, 'microwave': 0.85, 'bbq_facility': 0.3
        }
    }
    
    pattern = AMENITY_PATTERNS[property_type]
    amenities = {}
    for amenity, probability in pattern.items():
        amenities[amenity] = random.random() < probability
    
    if property_class == 'luxury':
        for amenity in amenities:
            amenities[amenity] = amenities[amenity] or random.random() < 0.3
    
    return amenities

def create_random_bookings(property_obj, start_date, end_date):
    """Create random bookings for a property"""
    bookings_created = []
    num_bookings = random.randint(0, 5)
    
    for _ in range(num_bookings):
        booking_start = start_date + timedelta(days=random.randint(0, 180))
        stay_duration = random.randint(
            property_obj.min_stay, 
            min(property_obj.max_stay, 30)
        )
        booking_end = booking_start + timedelta(days=stay_duration)
        
        if booking_end > end_date:
            continue
        
        overlapping = Booking.objects.filter(
            property=property_obj,
            check_in__lt=booking_end,
            check_out__gt=booking_start
        ).exists()
        
        if not overlapping:
            customer_name = fake.name()
            customer_email = fake.email()
            customer_phone = f"+230 {random.randint(5, 6)}{random.randint(1000000, 9999999)}"
            total_nights = stay_duration
            total_price = property_obj.rate_per_day * total_nights
            
            status = random.choices(
                ['confirmed', 'pending', 'completed', 'cancelled'],
                weights=[60, 20, 15, 5]
            )[0]
            
            booking = Booking.objects.create(
                property=property_obj,
                customer_name=customer_name,
                customer_email=customer_email,
                customer_phone=customer_phone,
                check_in=booking_start,
                check_out=booking_end,
                guests=random.randint(1, 8),
                total_price=total_price,
                status=status
            )
            bookings_created.append(booking)
    
    return bookings_created

def create_random_blocked_dates(property_obj, start_date, end_date):
    """Create random blocked dates for maintenance or unavailability"""
    blocked_entries = []
    num_blocks = random.randint(0, 3)
    
    for _ in range(num_blocks):
        block_start = start_date + timedelta(days=random.randint(30, 200))
        block_duration = random.randint(3, 14)
        block_end = block_start + timedelta(days=block_duration)
        
        if block_end > end_date:
            continue
        
        reasons = ['Maintenance', 'Renovation', 'Owner occupied', 'Seasonal closure', 'Private event']
        
        blocked = BlockedDate.objects.create(
            property=property_obj,
            start_date=block_start,
            end_date=block_end,
            reason=random.choice(reasons)
        )
        blocked_entries.append(blocked)
    
    return blocked_entries

def create_properties(count=20, include_images=True, include_owner_photos=True, create_availability=True):
    """Create fake property data with random bookings and blocked dates"""
    print(f"Creating {count} fake properties...")
    properties_created = []
    all_bookings = []
    all_blocked_dates = []
    
    # Date range for availability (next 12 months)
    today = date.today()
    availability_end = today + timedelta(days=365)
    
    for i in range(count):
        print(f"\n📝 Creating property {i+1}/{count}...")
        
        # Random selection
        property_type = random.choice([choice[0] for choice in PROPERTY_TYPE_CHOICES])
        city = random.choice([choice[0] for choice in CITY_CHOICES])
        side = random.choice([choice[0] for choice in SIDE_CHOICES])
        
        # Generate name
        name = random.choice(PROPERTY_NAMES[property_type])
        if random.random() < 0.3:
            name = f"{name} {random.choice(['Luxury', 'Premium', 'Deluxe', 'Exclusive'])}"
        
        print(f"  Name: {name}")
        
        # Generate coordinates
        gps_lat, gps_lng = generate_coordinates(city)
        
        # Get address
        MAURITIAN_ADDRESSES = {
            'Flic En Flac': ["Coastal Road", "Avenue des Palmiers", "Royal Road", "Beach Lane", "Sunset Avenue", "Lagoon View Drive", "Marina Street"],
            'GrandBaie': ["Royal Road", "Coastal Road", "La Salette Road", "Morcellement de Grand Baie", "Pereybere Street", "Sunset Boulevard"],
            'Tamarin': ["Coastal Road", "Avenue des Manguiers", "Black Rock Road", "Bay Street", "Tamarin Boulevard", "Surf Avenue"],
        }
        
        if city in MAURITIAN_ADDRESSES:
            address = random.choice(MAURITIAN_ADDRESSES[city])
            if random.random() < 0.5:
                address = f"{random.randint(1, 50)} {address}"
        else:
            address = fake.street_address()
        
        # Generate rates
        rate_per_day = generate_rate(property_type, side, is_monthly=False)
        rate_per_month = generate_rate(property_type, side, is_monthly=True)
        
        # Determine property class
        property_class = random.choices(
            ['budget', 'standard', 'luxury'],
            weights=[20, 60, 20]
        )[0]
        
        # Get amenities
        amenities = get_active_amenities(property_type, property_class)
        
        # Generate amenities text list
        active_amenities_list = [amenity.replace('_', ' ').title() 
                                for amenity, active in amenities.items() if active]
        
        # Generate description
        description = generate_description(name, property_type, city, active_amenities_list[:5])
        
        # Bedrooms
        if property_type == 'Villa':
            bedrooms = random.choices([2, 3, 4, 5, 6], weights=[15, 35, 30, 15, 5])[0]
            if property_class == 'luxury':
                bedrooms = random.randint(4, 6)
        else:
            bedrooms = random.choices([1, 2, 3, 4], weights=[30, 40, 20, 10])[0]
        
        # Stay duration
        min_stay = random.choices([1, 2, 3, 7], weights=[40, 30, 20, 10])[0]
        max_stay = random.randint(min_stay, min_stay + 28)
        
        # WhatsApp number
        whatsapp = f"+230 {random.randint(5, 6)}{random.randint(1000000, 9999999)}"
        
        # Languages
        LANGUAGES_LIST = [
            "English", "French", "English, French", "English, French, German",
            "English, French, Hindi", "English, Mandarin", "French, English",
            "English, German", "French, English, Italian"
        ]
        
        # Video URL
        video_url = random.choice(YOUTUBE_VIDEOS)
        print(f"  Video: {video_url}")
        
        # Owner name (realistic Mauritian name)
        owner_name = random.choice(MAURITIAN_OWNER_NAMES)
        print(f"  Owner: {owner_name}")
        
        # Create property object
        property_obj = Property(
            name=name,
            type=property_type,
            city=city,
            side=side,
            description=description,
            order_number=i,
            rate_per_day=rate_per_day,
            rate_per_month=rate_per_month,
            gps_lat=gps_lat,
            gps_lng=gps_lng,
            address=address,
            country="Mauritius",
            languages=random.choice(LANGUAGES_LIST),
            owner_name=owner_name,
            min_stay=min_stay,
            max_stay=max_stay,
            bedrooms=bedrooms,
            ac=amenities['ac'],
            internet=amenities['internet'],
            hot_water=amenities['hot_water'],
            parking=amenities['parking'],
            pool=amenities['pool'],
            roof_access=amenities['roof_access'],
            balcony=amenities['balcony'],
            washing_machine=amenities['washing_machine'],
            whatsapp=whatsapp,
            tv=amenities['tv'],
            microwave=amenities['microwave'],
            bbq_facility=amenities['bbq_facility'],
            video=video_url,
        )
        
        # Add owner photo if requested
        if include_owner_photos:
            print(f"  Adding owner photo...")
            owner_photo = download_person_photo()
            property_obj.owner_photo.save(f"owner_{owner_name.replace(' ', '_')}.jpg", owner_photo, save=False)
            print(f"    ✅ Owner photo added")
        
        # Add property images if requested
        if include_images:
            print(f"  Adding property images...")
            
            main_photo = download_placeholder_image('main_photo')
            property_obj.main_photo.save(f"main_{name.replace(' ', '_')}.jpg", main_photo, save=False)
            
            living_room_photo = download_placeholder_image('living_room_photo')
            property_obj.living_room_photo.save(f"living_{name.replace(' ', '_')}.jpg", living_room_photo, save=False)
            
            bedroom_photo = download_placeholder_image('bedroom_photo')
            property_obj.bedroom_photo.save(f"bedroom_{name.replace(' ', '_')}.jpg", bedroom_photo, save=False)
            
            # vc_photo removed - line deleted
            
            building_photo = download_placeholder_image('building_photo')
            property_obj.building_photo.save(f"building_{name.replace(' ', '_')}.jpg", building_photo, save=False)
            
            land_photo = download_placeholder_image('land_photo')
            property_obj.land_photo.save(f"land_{name.replace(' ', '_')}.jpg", land_photo, save=False)
        
        property_obj.save()
        properties_created.append(property_obj)
        
        # Create random bookings and blocked dates
        if create_availability:
            print(f"  Creating availability data...")
            bookings = create_random_bookings(property_obj, today, availability_end)
            blocked = create_random_blocked_dates(property_obj, today, availability_end)
            all_bookings.extend(bookings)
            all_blocked_dates.extend(blocked)
            print(f"    ✅ {len(bookings)} bookings created")
            print(f"    ✅ {len(blocked)} blocked periods created")
        
        print(f"  ✅ Created: {name} - {rate_per_day} Rs/day | {bedrooms} BR | {city}")
    
    # Print summary
    print(f"\n✅ Successfully created {len(properties_created)} properties!\n")
    print("=" * 50)
    print("📊 SUMMARY")
    print("=" * 50)
    print(f"  - Villas: {len([p for p in properties_created if p.type == 'Villa'])}")
    print(f"  - Apartments: {len([p for p in properties_created if p.type == 'Appartment'])}")
    print(f"\n  Properties by city:")
    for city, _ in CITY_CHOICES:
        count_city = len([p for p in properties_created if p.city == city])
        if count_city > 0:
            print(f"      {city}: {count_city}")
    
    print(f"\n  Properties with images: {len([p for p in properties_created if p.main_photo])}")
    print(f"  Properties with video: {len([p for p in properties_created if p.video])}")
    
    if include_owner_photos:
        print(f"  Properties with owner photos: {len([p for p in properties_created if p.owner_photo])}")
    
    if create_availability:
        print(f"\n  📅 AVAILABILITY DATA:")
        print(f"    - Total bookings created: {len(all_bookings)}")
        print(f"    - Total blocked periods: {len(all_blocked_dates)}")
        
        # Show sample booking
        if all_bookings:
            sample_booking = random.choice(all_bookings)
            print(f"\n    Sample booking:")
            print(f"      Property: {sample_booking.property.name}")
            print(f"      Dates: {sample_booking.check_in} to {sample_booking.check_out}")
            print(f"      Status: {sample_booking.status}")
        
        # Show sample blocked date
        if all_blocked_dates:
            sample_blocked = random.choice(all_blocked_dates)
            print(f"\n    Sample blocked period:")
            print(f"      Property: {sample_blocked.property.name}")
            print(f"      Dates: {sample_blocked.start_date} to {sample_blocked.end_date}")
            print(f"      Reason: {sample_blocked.reason}")
    
    return properties_created, all_bookings, all_blocked_dates

def clear_all_properties():
    """Clear all existing properties, bookings, and blocked dates from the database"""
    property_count = Property.objects.count()
    booking_count = Booking.objects.count()
    blocked_count = BlockedDate.objects.count()
    
    total = property_count + booking_count + blocked_count
    
    if total > 0:
        print(f"\n⚠️  Existing data:")
        print(f"    - Properties: {property_count}")
        print(f"    - Bookings: {booking_count}")
        print(f"    - Blocked dates: {blocked_count}")
        
        confirm = input("\nDelete ALL existing data? (y/n): ")
        if confirm.lower() == 'y':
            # Delete image files
            for prop in Property.objects.all():
                if prop.main_photo:
                    prop.main_photo.delete(save=False)
                if prop.living_room_photo:
                    prop.living_room_photo.delete(save=False)
                if prop.bedroom_photo:
                    prop.bedroom_photo.delete(save=False)
                # vc_photo removed from deletion
                if prop.building_photo:
                    prop.building_photo.delete(save=False)
                if prop.land_photo:
                    prop.land_photo.delete(save=False)
                if prop.owner_photo:
                    prop.owner_photo.delete(save=False)
            
            # Delete all data
            BlockedDate.objects.all().delete()
            Booking.objects.all().delete()
            Property.objects.all().delete()
            
            print(f"✅ Deleted all properties, bookings, and blocked dates")
            return True
        else:
            print("❌ Operation cancelled")
            return False
    return True

def show_availability_summary():
    """Show summary of all availability data in the database"""
    properties = Property.objects.all()
    
    if not properties:
        print("\nNo properties found in database.")
        return
    
    print("\n" + "=" * 60)
    print("📅 AVAILABILITY SUMMARY")
    print("=" * 60)
    
    for prop in properties:
        bookings = Booking.objects.filter(property=prop, status__in=['confirmed', 'pending'])
        blocked = BlockedDate.objects.filter(property=prop)
        
        print(f"\n🏠 {prop.name}")
        print(f"   Owner: {prop.owner_name}")
        print(f"   Has owner photo: {'✅' if prop.owner_photo else '❌'}")
        print(f"   Total bookings: {bookings.count()}")
        print(f"   Blocked periods: {blocked.count()}")
        
        if bookings.exists():
            upcoming = bookings.filter(check_in__gte=date.today()).order_by('check_in').first()
            if upcoming:
                print(f"   Next booking: {upcoming.check_in} to {upcoming.check_out}")

if __name__ == "__main__":
    print("=" * 50)
    print("🏠 Property Database Populator with Owner Photos")
    print("=" * 50)
    
    # Ask for number of properties
    try:
        num_properties = int(input("\nHow many properties to create? (default: 10): ") or "10")
    except ValueError:
        num_properties = 10
    
    # Ask whether to include images
    include_images = input("Include property placeholder images? (y/n, default: y): ").lower() != 'n'
    
    # Ask whether to include owner photos
    include_owner_photos = input("Include owner photos? (y/n, default: y): ").lower() != 'n'
    
    # Ask whether to create availability data
    create_availability = input("Create random bookings and blocked dates? (y/n, default: y): ").lower() != 'n'
    
    # Ask whether to clear existing data
    clear_existing = input("Clear existing properties first? (y/n, default: n): ").lower() == 'y'
    
    if clear_existing:
        if not clear_all_properties():
            exit()
    
    # Create properties
    print(f"\n🚀 Generating {num_properties} properties with realistic data...\n")
    properties, bookings, blocked = create_properties(
        num_properties, 
        include_images=include_images,
        include_owner_photos=include_owner_photos,
        create_availability=create_availability
    )
    
    # Show random sample
    if properties:
        print("\n📋 RANDOM SAMPLE PROPERTY:")
        sample = random.choice(properties)
        print(f"\n  Name: {sample.name}")
        print(f"  Type: {sample.type}")
        print(f"  Location: {sample.city} ({sample.side})")
        print(f"  Rate: Rs {sample.rate_per_day}/day or Rs {sample.rate_per_month}/month")
        print(f"  Bedrooms: {sample.bedrooms}")
        print(f"  Min/Max Stay: {sample.min_stay}/{sample.max_stay} nights")
        print(f"  Owner: {sample.owner_name}")
        print(f"  Owner Photo: {bool(sample.owner_photo)}")
        print(f"  Video URL: {sample.video}")
        print(f"  Has Images: {bool(sample.main_photo)}")
        print(f"  Amenities: {', '.join([attr for attr in ['AC', 'Pool', 'Internet', 'Parking'] if getattr(sample, attr.lower().replace(' ', '_'))])}")
        
        # Show availability for sample
        if create_availability:
            sample_bookings = Booking.objects.filter(property=sample)
            if sample_bookings.exists():
                print(f"\n  Sample bookings for this property:")
                for booking in sample_bookings[:2]:
                    print(f"    - {booking.check_in} to {booking.check_out} ({booking.status})")
    
    # Show full availability summary
    if create_availability:
        show_availability_summary()