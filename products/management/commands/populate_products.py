import os
import json
from django.core.management.base import BaseCommand
from django.apps import apps
from django.conf import settings
from django.core.files.base import ContentFile
from products.models import Product, Category
from accounts.models import User

class Command(BaseCommand):
    help = 'Populates the database with sample products and categories for a specified seller.'

    def add_arguments(self, parser):
        parser.add_argument('seller_name', type=str, help='The username of the seller to assign products to.')
        parser.add_argument('--json_file', type=str, default='sample_products.json',
                            help='The name of the JSON file to load product data from. (e.g., sample_products_new.json)')

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting database population...'))
        
        seller_name = options['seller_name']
        json_file = options['json_file']

        # Path to the JSON file, using the provided argument.
        json_file_path = os.path.join(apps.get_app_config('products').path, json_file)

        # Get the absolute path to the media/products directory
        project_root = settings.BASE_DIR
        LOCAL_IMAGE_DIR = os.path.join(project_root, 'media', 'products')

        # Check if the JSON file exists before trying to open it.
        if not os.path.exists(json_file_path):
            self.stdout.write(self.style.ERROR(f'Error: JSON file not found at {json_file_path}'))
            return

        with open(json_file_path, 'r') as f:
            products_data = json.load(f)

        self.stdout.write(self.style.SUCCESS(f'Successfully loaded {len(products_data)} products from JSON file.'))
        self.stdout.write(f'Using JSON file: {json_file}')
        self.stdout.write(f'First product name: {products_data[0]["name"]}')
        self.stdout.write('---')
        
        # First pass: Process categories
        processed_categories = set()
        for product_item in products_data:
            category_name = product_item.get('category_name')
            if category_name and category_name not in processed_categories:
                category, created = Category.objects.get_or_create(name=category_name)
                
                if created:
                    self.stdout.write(f'Created new category: {category_name}')
                else:
                    self.stdout.write(f'Using existing category: {category_name}')
                    
                processed_categories.add(category_name)
        
        self.stdout.write(self.style.SUCCESS('Finished processing categories.'))
        self.stdout.write('---')
        self.stdout.write('Starting product creation...')
        
        try:
            seller = User.objects.get(username=seller_name)
            
            # CRITICAL VALIDATION: Check if the user is a seller using your is_seller() method
            if not seller.is_seller():
                self.stdout.write(self.style.ERROR(f"Error: User '{seller_name}' is not a seller. Products can only be assigned to a seller."))
                return

            self.stdout.write(f'Found valid seller user: {seller.username}')
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Seller user with username '{seller_name}' not found. Please create one."))
            return
            
        for product_item in products_data:
            try:
                category = Category.objects.get(name=product_item.get('category_name'))

                image_path = product_item.get('image_path')
                image_file = None
                
                if image_path:
                    # LOCAL_IMAGE_DIR is `.../media/products/`
                    # image_path is `images/kanken-backpack.jpeg`
                    full_image_path = os.path.join(LOCAL_IMAGE_DIR, image_path)
                    try:
                        self.stdout.write(f'Reading local image for {product_item["name"]}...')
                        with open(full_image_path, 'rb') as f:
                            image_file = ContentFile(f.read(), name=os.path.basename(full_image_path))
                    except FileNotFoundError:
                        self.stdout.write(self.style.ERROR(f'Local image file not found at {full_image_path}. Skipping image upload.'))

                product, created = Product.objects.get_or_create(
                    name=product_item['name'],
                    defaults={
                        'description': product_item['description'],
                        'price': product_item['price'],
                        'stock': product_item['stock'],
                        'category': category,
                        'seller': seller,
                        'image': image_file,
                    }
                )
                
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created new product: {product.name}'))
                else:
                    self.stdout.write(self.style.NOTICE(f'Product already exists, skipping: {product.name}'))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error creating product {product_item["name"]}: {e}'))

        self.stdout.write('---')
        self.stdout.write(self.style.SUCCESS('Database population finished.'))
