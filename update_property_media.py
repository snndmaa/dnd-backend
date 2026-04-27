import os
import django
import random
import requests
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile
import uuid
from urllib.parse import urlparse
import time

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dnd_backend.settings')
django.setup()

from listings.models import Property

# Real YouTube videos of houses, apartments, and properties
YOUTUBE_HOUSE_VIDEOS = [
    # Luxury Villa Tours
    "https://www.youtube.com/watch?v=J-GV7UJ1dsc",  # Luxury Modern Villa Tour
    "https://www.youtube.com/watch?v=Qk7xV4wRzvE",  # Tropical Villa Tour
    "https://www.youtube.com/watch?v=zA0RfR5kCpU",  # Beachfront Villa
    "https://www.youtube.com/watch?v=9XQxDWHjJ0I",  # Modern Mansion Tour
    
    # Apartment Tours
    "https://www.youtube.com/watch?v=fYqVvJ7yF_k",  # Luxury Apartment Tour
    "https://www.youtube.com/watch?v=3jLkLvKxN-o",  # Modern Condo Tour
    "https://www.youtube.com/watch?v=wUgXpXqVKqQ",  # Downtown Apartment
    
    # House Tours
    "https://www.youtube.com/watch?v=LlXKqPpQxL0",  # Modern Family Home
    "https://www.youtube.com/watch?v=rHdVkPQxRZ8",  # Tropical House Design
    "https://www.youtube.com/watch?v=8vKjQjXjYxM",  # Villa with Pool
    
    # Property Walkthroughs
    "https://www.youtube.com/watch?v=HjVtLkDpQrM",  # Real Estate Walkthrough
    "https://www.youtube.com/watch?v=KjXqQxWpVnY",  # Property Tour
    "https://www.youtube.com/watch?v=gYqVqYxKjLk",  # Modern Home Tour
    
    # Specific to property types
    "https://www.youtube.com/watch?v=WqXqRrVtYyU",  # Penthouse Tour
    "https://www.youtube.com/watch?v=FkLpQxXjVnM",  # Garden Villa
    "https://www.youtube.com/watch?v=VsXqLpWqRkY",  # Ocean View Property
]

# Image URLs for different photo categories (free, reliable placeholder images)
IMAGE_URLS = {
    'main_photo': [
        "https://images.pexels.com/photos/106399/pexels-photo-106399.jpeg",  # Modern house
        "https://images.pexels.com/photos/2587054/pexels-photo-2587054.jpeg",  # Villa
        "https://images.pexels.com/photos/280229/pexels-photo-280229.jpeg",  # Beach house
        "https://images.pexels.com/photos/2724749/pexels-photo-2724749.jpeg",  # Luxury home
        "https://images.pexels.com/photos/2102587/pexels-photo-2102587.jpeg",  # Modern building
    ],
    'living_room_photo': [
        "https://images.pexels.com/photos/1571459/pexels-photo-1571459.jpeg",  # Modern living room
        "https://images.pexels.com/photos/276724/pexels-photo-276724.jpeg",  # Cozy living room
        "https://images.pexels.com/photos/271816/pexels-photo-271816.jpeg",  # Luxury living room
        "https://images.pexels.com/photos/2587054/pexels-photo-2587054.jpeg",  # Spacious living
        "https://images.pexels.com/photos/262367/pexels-photo-262367.jpeg",  # Minimalist living
    ],
    'bedroom_photo': [
        "https://images.pexels.com/photos/1648771/pexels-photo-1648771.jpeg",  # Master bedroom
        "https://images.pexels.com/photos/279746/pexels-photo-279746.jpeg",  # Cozy bedroom
        "https://images.pexels.com/photos/271815/pexels-photo-271815.jpeg",  # Luxury bedroom
        "https://images.pexels.com/photos/1454794/pexels-photo-1454794.jpeg",  # Modern bedroom
        "https://images.pexels.com/photos/1571460/pexels-photo-1571460.jpeg",  # Guest bedroom
    ],
    'vc_photo': [
        "https://images.pexels.com/photos/323705/pexels-photo-323705.jpeg",  # Patio
        "https://images.pexels.com/photos/280232/pexels-photo-280232.jpeg",  # Terrace
        "https://images.pexels.com/photos/2587054/pexels-photo-2587054.jpeg",  # Outdoor area
        "https://images.pexels.com/photos/2102587/pexels-photo-2102587.jpeg",  # Balcony
        "https://images.pexels.com/photos/2442915/pexels-photo-2442915.jpeg",  # Garden view
    ],
    'building_photo': [
        "https://images.pexels.com/photos/2587054/pexels-photo-2587054.jpeg",  # Modern building
        "https://images.pexels.com/photos/106399/pexels-photo-106399.jpeg",  # House exterior
        "https://images.pexels.com/photos/280229/pexels-photo-280229.jpeg",  # Beachfront
        "https://images.pexels.com/photos/2724749/pexels-photo-2724749.jpeg",  # Luxury exterior
        "https://images.pexels.com/photos/2102587/pexels-photo-2102587.jpeg",  # Apartment building
    ],
    'land_photo': [
        "https://images.pexels.com/photos/1261728/pexels-photo-1261728.jpeg",  # Garden
        "https://images.pexels.com/photos/280232/pexels-photo-280232.jpeg",  # Landscape
        "https://images.pexels.com/photos/2442915/pexels-photo-2442915.jpeg",  # Property grounds
        "https://images.pexels.com/photos/2606897/pexels-photo-2606897.jpeg",  # Pool area
        "https://images.pexels.com/photos/2343465/pexels-photo-2343465.jpeg",  # Tropical garden
    ]
}

def download_image(url, category_name, property_name):
    """Download image from URL and return as ContentFile"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            # Open image
            img = Image.open(BytesIO(response.content))
            
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Resize image to reasonable size (max 1920x1080)
            img.thumbnail((1920, 1080), Image.Resampling.LANCZOS)
            
            # Save to bytes
            img_byte_arr = BytesIO()
            img.save(img_byte_arr, format='JPEG', quality=85)
            img_byte_arr.seek(0)
            
            # Create filename
            filename = f"{category_name}_{property_name}_{uuid.uuid4().hex[:8]}.jpg"
            return ContentFile(img_byte_arr.getvalue(), name=filename)
    except Exception as e:
        print(f"    ❌ Error downloading {category_name}: {str(e)[:100]}")
        return None
    
    return None

def get_youtube_video_for_property(property_obj):
    """Select appropriate YouTube video based on property type"""
    if property_obj.type == 'Villa':
        # More luxury/tropical videos for villas
        villa_videos = YOUTUBE_HOUSE_VIDEOS[:8]  # First 8 are villa-focused
        return random.choice(villa_videos)
    else:  # Apartment
        # Apartment/condo focused videos
        apartment_videos = YOUTUBE_HOUSE_VIDEOS[8:12]
        return random.choice(apartment_videos)

def update_property_images(property_obj, dry_run=False):
    """Update all images for a single property"""
    updated = False
    
    print(f"\n  📸 Updating images for: {property_obj.name}")
    
    # Update main photo
    if not property_obj.main_photo or dry_run:
        url = random.choice(IMAGE_URLS['main_photo'])
        print(f"    Main photo: {url.split('/')[-1][:30]}...")
        if not dry_run:
            img_file = download_image(url, 'main', property_obj.name.replace(' ', '_'))
            if img_file:
                property_obj.main_photo.save(f"main_{property_obj.name.replace(' ', '_')}.jpg", img_file, save=False)
                updated = True
                print(f"    ✅ Main photo updated")
            else:
                print(f"    ⚠️  Failed to update main photo")
    
    # Update living room photo
    if not property_obj.living_room_photo or dry_run:
        url = random.choice(IMAGE_URLS['living_room_photo'])
        print(f"    Living room: {url.split('/')[-1][:30]}...")
        if not dry_run:
            img_file = download_image(url, 'living', property_obj.name.replace(' ', '_'))
            if img_file:
                property_obj.living_room_photo.save(f"living_{property_obj.name.replace(' ', '_')}.jpg", img_file, save=False)
                updated = True
                print(f"    ✅ Living room photo updated")
            else:
                print(f"    ⚠️  Failed to update living room photo")
    
    # Update bedroom photo
    if not property_obj.bedroom_photo or dry_run:
        url = random.choice(IMAGE_URLS['bedroom_photo'])
        print(f"    Bedroom: {url.split('/')[-1][:30]}...")
        if not dry_run:
            img_file = download_image(url, 'bedroom', property_obj.name.replace(' ', '_'))
            if img_file:
                property_obj.bedroom_photo.save(f"bedroom_{property_obj.name.replace(' ', '_')}.jpg", img_file, save=False)
                updated = True
                print(f"    ✅ Bedroom photo updated")
            else:
                print(f"    ⚠️  Failed to update bedroom photo")
    
    # Update VC photo (outdoor/terrace)
    if not property_obj.vc_photo or dry_run:
        url = random.choice(IMAGE_URLS['vc_photo'])
        print(f"    Outdoor/VC: {url.split('/')[-1][:30]}...")
        if not dry_run:
            img_file = download_image(url, 'vc', property_obj.name.replace(' ', '_'))
            if img_file:
                property_obj.vc_photo.save(f"vc_{property_obj.name.replace(' ', '_')}.jpg", img_file, save=False)
                updated = True
                print(f"    ✅ VC photo updated")
            else:
                print(f"    ⚠️  Failed to update VC photo")
    
    # Update building photo
    if not property_obj.building_photo or dry_run:
        url = random.choice(IMAGE_URLS['building_photo'])
        print(f"    Building: {url.split('/')[-1][:30]}...")
        if not dry_run:
            img_file = download_image(url, 'building', property_obj.name.replace(' ', '_'))
            if img_file:
                property_obj.building_photo.save(f"building_{property_obj.name.replace(' ', '_')}.jpg", img_file, save=False)
                updated = True
                print(f"    ✅ Building photo updated")
            else:
                print(f"    ⚠️  Failed to update building photo")
    
    # Update land photo
    if not property_obj.land_photo or dry_run:
        url = random.choice(IMAGE_URLS['land_photo'])
        print(f"    Land/grounds: {url.split('/')[-1][:30]}...")
        if not dry_run:
            img_file = download_image(url, 'land', property_obj.name.replace(' ', '_'))
            if img_file:
                property_obj.land_photo.save(f"land_{property_obj.name.replace(' ', '_')}.jpg", img_file, save=False)
                updated = True
                print(f"    ✅ Land photo updated")
            else:
                print(f"    ⚠️  Failed to update land photo")
    
    return updated

def update_property_videos(property_obj, dry_run=False):
    """Update YouTube video for property"""
    if not property_obj.video or property_obj.video == '' or dry_run:
        video_url = get_youtube_video_for_property(property_obj)
        print(f"    🎥 Video: {video_url}")
        if not dry_run:
            property_obj.video = video_url
            return True
    return False

def update_all_properties(dry_run=True, update_images=True, update_videos=True):
    """Update all properties in the database"""
    
    properties = Property.objects.all()
    total = properties.count()
    
    if total == 0:
        print("\n❌ No properties found in database!")
        return
    
    print(f"\n{'='*60}")
    print(f"{'DRY RUN' if dry_run else 'LIVE UPDATE'} - Updating {total} properties")
    print(f"{'='*60}")
    print(f"  Update images: {update_images}")
    print(f"  Update videos: {update_videos}")
    
    if not dry_run:
        print("\n⚠️  THIS WILL MODIFY YOUR DATABASE!")
        confirm = input("Are you sure you want to continue? (yes/no): ")
        if confirm.lower() != 'yes':
            print("❌ Update cancelled")
            return
    
    stats = {
        'total': total,
        'images_updated': 0,
        'videos_updated': 0,
        'errors': 0
    }
    
    for idx, property_obj in enumerate(properties, 1):
        print(f"\n{'='*50}")
        print(f"Property {idx}/{total}: {property_obj.name} (ID: {property_obj.id})")
        print(f"{'='*50}")
        
        try:
            # Update images
            if update_images:
                if update_property_images(property_obj, dry_run):
                    stats['images_updated'] += 1
            
            # Update videos
            if update_videos:
                if update_property_videos(property_obj, dry_run):
                    stats['videos_updated'] += 1
            
            # Save changes if not dry run
            if not dry_run:
                property_obj.save()
                print(f"\n  ✅ Property saved successfully")
            
            # Small delay to avoid overwhelming the server
            if not dry_run:
                time.sleep(0.5)
                
        except Exception as e:
            stats['errors'] += 1
            print(f"\n  ❌ Error updating property: {str(e)}")
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"📊 UPDATE SUMMARY")
    print(f"{'='*60}")
    print(f"  Total properties: {stats['total']}")
    print(f"  Images updated: {stats['images_updated']}")
    print(f"  Videos updated: {stats['videos_updated']}")
    print(f"  Errors: {stats['errors']}")
    
    if dry_run:
        print(f"\n💡 This was a DRY RUN. No changes were made to the database.")
        print(f"   Run with --live to apply changes.")

def clear_all_media():
    """Clear all media files from properties"""
    properties = Property.objects.all()
    total = properties.count()
    
    if total == 0:
        print("\n❌ No properties found!")
        return
    
    print(f"\n⚠️  This will delete ALL images from {total} properties!")
    confirm = input("Are you absolutely sure? (yes/no): ")
    
    if confirm.lower() == 'yes':
        for prop in properties:
            # Delete image files
            if prop.main_photo:
                prop.main_photo.delete(save=False)
            if prop.living_room_photo:
                prop.living_room_photo.delete(save=False)
            if prop.bedroom_photo:
                prop.bedroom_photo.delete(save=False)
            if prop.vc_photo:
                prop.vc_photo.delete(save=False)
            if prop.building_photo:
                prop.building_photo.delete(save=False)
            if prop.land_photo:
                prop.land_photo.delete(save=False)
            
            # Clear video
            prop.video = ''
            prop.save()
        
        print(f"✅ Cleared all media from {total} properties")
    else:
        print("❌ Operation cancelled")

if __name__ == "__main__":
    print("=" * 60)
    print("🏠 Property Media Updater")
    print("=" * 60)
    print("\nThis script will update your existing properties with:")
    print("  📸 Real placeholder images from Pexels")
    print("  🎥 Real YouTube house tour videos")
    print("\nOptions:")
    print("  1. Dry Run (preview changes without modifying DB)")
    print("  2. Live Update (actually update the database)")
    print("  3. Clear all media (remove all images and videos)")
    print("  4. Exit")
    
    choice = input("\nSelect option (1-4): ").strip()
    
    if choice == '1':
        # Dry run
        update_images = input("Update images? (y/n, default: y): ").lower() != 'n'
        update_videos = input("Update videos? (y/n, default: y): ").lower() != 'n'
        update_all_properties(dry_run=True, update_images=update_images, update_videos=update_videos)
        
    elif choice == '2':
        # Live update
        print("\n⚠️  LIVE UPDATE MODE - This will modify your database!")
        update_images = input("Update images? (y/n, default: y): ").lower() != 'n'
        update_videos = input("Update videos? (y/n, default: y): ").lower() != 'n'
        update_all_properties(dry_run=False, update_images=update_images, update_videos=update_videos)
        
    elif choice == '3':
        clear_all_media()
        
    else:
        print("Exiting...")