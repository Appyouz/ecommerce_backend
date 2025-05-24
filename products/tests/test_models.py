import pytest
from products.models import Product, Category

@pytest.mark.django_db
def test_category_creation():
    """
    Test that a Category can be created and has the correct name.
    """
    category = Category.objects.create(name='Electronics')
    assert category.name == 'Electronics'
    assert Category.objects.count() == 1
    print("Category creation test passed!")

@pytest.mark.django_db
def test_product_creation():
    """
    Test that a Product can be created with a Category
    """
    category = Category.objects.create(name='Clothing')
    product = Product.objects.create(
        name='T-Shirt',
        description='Comfortable cotton t-shirt',
        price=19.99,
        stock=100,
        category=category
    )

    assert product.name == 'T-Shirt'
    assert product.price == 19.99
    assert product.stock == 100
    assert product.category == category
    assert Product.objects.count() == 1
    print("Product creation test passed!")


@pytest.mark.django_db
def test_product_str_method():
    """
    Test the __str__ method of the Product model.
    """
    category = Category.objects.create(name='Books')
    product = Product.objects.create(
        name='Python Basics',
        description='A book about Python',
        price=29.99,
        stock=50,
        category=category
    )
    assert str(product) == 'Python Basics'
    print("Product __str__ method test passed!") 
