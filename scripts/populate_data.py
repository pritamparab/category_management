import os
import sys
import django
import requests

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from core.models import Product

def populate_products():
    fetch_products = "https://fakestoreapi.com/products"

    response = requests.get(fetch_products)
    products = response.json()

    for product_data in products:
        Product.objects.get_or_create(
            title=product_data["title"],
            defaults={
                "price": product_data["price"],
                "description": product_data["description"],
                "category": product_data["category"],
                "image_url": product_data["image"],
            }
        )
    print("Products populated successfully!")

def populate_premium_products():
    data = [
        {
            "title": "Samsung 22 Ultra",
            "price": 68990,
            "description": "It is a premium flagship smartphone with a 6.8-inch QHD+ Dynamic AMOLED 2X display, S-Pen stylus support, quad rear cameras (108MP + 12MP + 10MP + 10MP), and a 40MP selfie camera1",
            "category": "Mobile Phone",
            "image_url": "https://images.pexels.com/photos/11772524/pexels-photo-11772524.jpeg"
        },
        {
            "title": "Pixel 8 Pro",
            "price": 79999,
            "description": "The Pixel 8 Pro boosts productivity with a powerful chipset, Google AI for stunning photos, a 6.2-inch display, and IP68 protection. Key features include Audio Magic Eraser, safety tools, and up to 72 hours of battery life with Extreme Battery Saver mode.",
            "category": "Mobile Phone",
            "image_url": "https://images.pexels.com/photos/3585090/pexels-photo-3585090.jpeg"
        },
        {
            "title": "IPhone 16 pro max",
            "price": 164900,
            "description": "The iPhone 16 Pro Max features a 6.9-inch Super Retina XDR display, an A18 Pro chip, and a triple-camera system with enhanced low-light performance.",
            "category": "Mobile Phone",
            "image_url": "https://images.pexels.com/photos/29020349/pexels-photo-29020349/free-photo-of-modern-smartphone-on-wooden-surface.jpeg"
        },
        {
            "title": "Xiomi 14 Ultra",
            "price": 99999,
            "description": "The phone features 6.73″ display, Snapdragon 8 Gen 3 chipset, 5000 mAh battery, 1024 GB storage, 16 GB RAM, Xiaomi Shield Glass / Xiaomi Longjing Glass.",
            "category": "Mobile Phone",
            "image_url": "https://images.pexels.com/photos/27598326/pexels-photo-27598326/free-photo-of-samsung-galaxy-s10e-review.jpeg"
        }
    ]

    for product_data in data:
        Product.objects.get_or_create(
            title=product_data["title"],
            defaults={
                "price": product_data["price"],
                "description": product_data["description"],
                "category": product_data["category"],
                "image_url": product_data["image_url"],
            }
        )
    print("Products populated successfully!")

if __name__ == "__main__":
    populate_products()
    populate_premium_products()