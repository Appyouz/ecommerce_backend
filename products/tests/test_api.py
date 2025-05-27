import pytest
from rest_framework import status
from products.models import Product, Category
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model
User = get_user_model()


@pytest.mark.django_db # Always need this if interacting with the database
def test_product_list(client):
    """
    Test that the product list API endpoint returns a 200 OK status.
    """
    Category.objects.create(name='Electronics')
    Product.objects.create(
        name='Laptop',
        description="Zephyrus",
        price=1500.00,
        stock=50,
        category=Category.objects.first()
    )

    Product.objects.create(
        name="Mouse",
        description="Gaming mouse",
        price=250.00,
        stock=100,
        category=Category.objects.first()
    )

    # Make a GET request to the produt list endpoint
    response = client.get('/api/products/')

    # Assert or verfiy
    # First check the status code (200)ok
    assert response.status_code == status.HTTP_200_OK

    # Second, check the content of the response. It should be a JSON array
    data = response.json()
    assert isinstance(data, list) # check if its a list for multiple products
    assert len(data) == 2 # check if the no.of products from above were created

    # We ordered by 'name' in ProductViewSet, so 'Laptop' should come before 'Mouse'.
    assert data[0]['name'] == 'Laptop'
    assert data[1]['name'] == 'Mouse'

@pytest.mark.django_db
def test_create_product_unauthenticated(client):
    """
    Test that an unauthenticated user cannot create a product.
    """
    category = Category.objects.create(name='Books')
    product_data = {
        'name': 'The Test Book',
        'description': 'A book for testing.',
        'price': 9.99,
        'stock': 10,
        'category_id': category.id,
    }

    response = client.post('/api/products/', data=product_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert Product.objects.count() == 0

@pytest.mark.django_db
def test_create_product_authenticated(client):
    """
    Test that an authenticated user can create a product.
    """
    category = Category.objects.create(name='Electronics')
    user = User.objects.create_user(username='testuser', password='Testpassword123')

    # Generate a jwt access token for the user
    access_token = str(AccessToken.for_user(user))

    # Prepare headers
    headers = {
    'Content-Type': 'application/json' ,
    'HTTP_AUTHORIZATION': f'Bearer {access_token}', 
    }


    client.force_login(user)
    product_data = {
        'name': 'Authenticated Product',
        'description': 'Created by an authenticated user',
        'price': 49.99,
        'stock': 20,
        'category_id': category.id,
    }

    response = client.post('/api/products/', data=product_data, **headers)
    
    assert response.status_code == status.HTTP_201_CREATED
    assert Product.objects.count() == 1
    created_product = Product.objects.first()
    assert created_product.name == product_data['name']
    assert created_product.description == product_data['description']
    assert float(created_product.price) == product_data['price']
    assert created_product.stock == product_data['stock']
    assert created_product.category ==  category

    # Optionally check the response body if it returns the created object
    response_data = response.json()
    assert response_data['name'] == product_data['name']
    assert float(created_product.price) == product_data['price']
    assert response_data['price'] == str(product_data['price'])
