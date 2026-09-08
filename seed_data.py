import os
import sys
import random
import datetime
from PIL import Image, ImageDraw, ImageFilter

# Configure Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from gallery.models import Artwork, ArtClass, CommissionRequest, ContactMessage
from django.utils import timezone

def create_artistic_canvas(filename, title, color_scheme='gold'):
    width, height = 1200, 900
    img = Image.new('RGB', (width, height), color=(20, 20, 25))
    draw = ImageDraw.Draw(img)

    # Color palettes
    palettes = {
        'gold': [(18, 18, 22), (212, 175, 55), (139, 69, 19), (245, 222, 179), (75, 0, 130)],
        'blue': [(15, 23, 42), (30, 58, 138), (14, 165, 233), (224, 242, 254), (212, 175, 55)],
        'sunset': [(30, 10, 20), (225, 29, 72), (249, 115, 22), (250, 204, 21), (76, 29, 149)],
        'emerald': [(6, 78, 59), (16, 185, 129), (167, 243, 208), (212, 175, 55), (17, 24, 39)],
    }
    colors = palettes.get(color_scheme, palettes['gold'])

    # Layer 1: Radial gradient background
    for r in range(width, 0, -8):
        c = colors[r % len(colors)]
        draw.ellipse([width//2 - r, height//2 - r, width//2 + r, height//2 + r], fill=c)

    img = img.filter(ImageFilter.GaussianBlur(radius=40))
    draw = ImageDraw.Draw(img)

    # Layer 2: Abstract brush strokes & geometric overlays
    for _ in range(35):
        c = colors[random.randint(0, len(colors)-1)]
        x1 = random.randint(-100, width)
        y1 = random.randint(-100, height)
        x2 = x1 + random.randint(150, 600)
        y2 = y1 + random.randint(100, 400)
        draw.ellipse([x1, y1, x2, y2], fill=c, outline=colors[1], width=2)

    img = img.filter(ImageFilter.GaussianBlur(radius=15))
    draw = ImageDraw.Draw(img)

    # Layer 3: Sharp impasto textures & gold flakes
    for _ in range(80):
        x = random.randint(50, width-50)
        y = random.randint(50, height-50)
        r = random.randint(5, 45)
        c = colors[1] if random.random() > 0.4 else colors[3]
        draw.ellipse([x-r, y-r, x+r, y+r], fill=c)

    # Canvas border & signature simulation
    draw.rectangle([20, 20, width-20, height-20], outline=(212, 175, 55), width=3)
    draw.text((width - 250, height - 60), "D-Art Studio", fill=(245, 245, 245))

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    img.save(filename, quality=95)

def seed_database():
    print("Clearing old data...")
    Artwork.objects.all().delete()
    ArtClass.objects.all().delete()
    CommissionRequest.objects.all().delete()
    ContactMessage.objects.all().delete()

    media_dir = os.path.join(os.path.dirname(__file__), 'media')

    artworks_data = [
        {
            'title': "Ethereal Luminescence",
            'medium': "Oil on Canvas",
            'dimensions': '36" x 48"',
            'price': 34000.00,
            'description': "A mesmerizing exploration of ambient evening light breaking through dramatic atmospheric clouds. Rendered using classical glazing techniques with rich impasto textures by D-Art Studio.",
            'year_created': 2025,
            'is_available': True,
            'is_featured': True,
            'color': 'gold',
            'filename': 'ethereal_luminescence.jpg'
        },
        {
            'title': "Symphony of Venice",
            'medium': "Oil on Canvas",
            'dimensions': '40" x 60"',
            'price': 48000.00,
            'description': "Reflections of Venetian palazzos shimmering upon tranquil canal waters during golden hour. Vibrant warm ochres and deep ultramarine hues capture eternal Italian romance.",
            'year_created': 2025,
            'is_available': True,
            'is_featured': True,
            'color': 'sunset',
            'filename': 'symphony_of_venice.jpg'
        },
        {
            'title': "Whispers of the Golden Hour",
            'medium': "Acrylic on Canvas",
            'dimensions': '30" x 40"',
            'price': 22000.00,
            'description': "Soft lyrical abstraction depicting dusk light filtering through meadow foliage. Features hand-applied 24k gold leaf details that glow warmly under changing room lights.",
            'year_created': 2025,
            'is_available': True,
            'is_featured': True,
            'color': 'gold',
            'filename': 'golden_hour_whispers.jpg'
        },
        {
            'title': "Solitude in Azure",
            'medium': "Watercolor & Gold Leaf",
            'dimensions': '24" x 36"',
            'price': 16500.00,
            'description': "Delicate watercolor washes blending deep indigo, cobalt, and cerulean tones with organic gold metallic line work. Framed under museum-grade anti-reflective glass.",
            'year_created': 2025,
            'is_available': True,
            'is_featured': True,
            'color': 'blue',
            'filename': 'solitude_azure.jpg'
        },
        {
            'title': "Verdant Echoes",
            'medium': "Oil on Linen",
            'dimensions': '32" x 44"',
            'price': 29000.00,
            'description': "An expressive forest canopy study celebrating vitality and renewal. Layered green tones contrast against warm terracotta underpainting.",
            'year_created': 2024,
            'is_available': False,
            'is_featured': True,
            'color': 'emerald',
            'filename': 'verdant_echoes.jpg'
        },
        {
            'title': "Cosmic Resonance",
            'medium': "Mixed Media",
            'dimensions': '48" x 48"',
            'price': 52000.00,
            'description': "A large-scale statement piece combining oil paint, marble dust, sand, and gold pigment on gallery-depth canvas. A tactile centerpiece for modern minimalist interiors.",
            'year_created': 2025,
            'is_available': True,
            'is_featured': True,
            'color': 'gold',
            'filename': 'cosmic_resonance.jpg'
        },
        {
            'title': "Twilight Nocturne",
            'medium': "Acrylic on Wood",
            'dimensions': '20" x 30"',
            'price': 9500.00,
            'description': "A quiet nightscape painted on cradled birch panel. Deep twilight blues paired with subtle silver mica highlights create a tranquil, introspective mood.",
            'year_created': 2025,
            'is_available': True,
            'is_featured': False,
            'color': 'blue',
            'filename': 'twilight_nocturne.jpg'
        },
        {
            'title': "Urban Mirage",
            'medium': "Digital Fine Art Print",
            'dimensions': '24" x 30"',
            'price': 6500.00,
            'description': "Limited Edition (1 of 10) archival pigment print on Hahnemühle cotton rag paper. Hand-signed and numbered by D-Art Studio.",
            'year_created': 2024,
            'is_available': False,
            'is_featured': False,
            'color': 'sunset',
            'filename': 'urban_mirage.jpg'
        },
    ]

    for item in artworks_data:
        rel_path = f"artworks/{item['filename']}"
        full_path = os.path.join(media_dir, rel_path)
        create_artistic_canvas(full_path, item['title'], color_scheme=item['color'])

        Artwork.objects.create(
            title=item['title'],
            medium=item['medium'],
            dimensions=item['dimensions'],
            price=item['price'],
            description=item['description'],
            year_created=item['year_created'],
            is_available=item['is_available'],
            is_featured=item['is_featured'],
            image=rel_path
        )
        print(f"Created Artwork: {item['title']}")

    classes_data = [
        {
            'title': "Classical Oil Painting & Glazing Masterclass",
            'description': "Master Renaissance glazing techniques, color mixing, and tonal value control over a 2-day weekend intensive workshop.",
            'days': 7,
            'price': 3500.00,
            'location': "D-Art Studio, Silver Oak, Raipur",
            'seats_available': 6,
            'total_seats': 15,
            'instructor': "D-Art Studio Master",
            'filename': 'class_oil.jpg',
            'color': 'gold'
        },
        {
            'title': "Impasto Textures & Palette Knife Mastery",
            'description': "Learn how to build dramatic 3D sculptural textures on canvas using heavy body acrylics, marble paste, and palette knives.",
            'days': 14,
            'price': 2800.00,
            'location': "D-Art Studio, Silver Oak, Raipur",
            'seats_available': 12,
            'total_seats': 15,
            'instructor': "D-Art Studio Master",
            'filename': 'class_impasto.jpg',
            'color': 'sunset'
        },
        {
            'title': "Atmospheric Landscape & Light Studies",
            'description': "Explore plein air techniques and watercolor atmospheric perspective in an intimate evening studio session with live model studies.",
            'days': 21,
            'price': 2200.00,
            'location': "D-Art Studio, Silver Oak, Raipur",
            'seats_available': 4,
            'total_seats': 12,
            'instructor': "D-Art Studio Masters",
            'filename': 'class_watercolor.jpg',
            'color': 'blue'
        },
    ]

    for item in classes_data:
        rel_path = f"classes/{item['filename']}"
        full_path = os.path.join(media_dir, rel_path)
        create_artistic_canvas(full_path, item['title'], color_scheme=item['color'])

        class_date = timezone.now() + datetime.timedelta(days=item['days'], hours=10)
        ArtClass.objects.create(
            title=item['title'],
            description=item['description'],
            date=class_date,
            price=item['price'],
            location=item['location'],
            seats_available=item['seats_available'],
            total_seats=item['total_seats'],
            instructor=item['instructor'],
            image=rel_path
        )
        print(f"Created ArtClass: {item['title']}")

    print("Database successfully re-seeded with D-Art Studio branding!")

if __name__ == '__main__':
    seed_database()
