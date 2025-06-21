from typing import override
from django.db import models
from django.contrib.auth.models import AbstractUser 

class User(AbstractUser):
    ROLE_CHOICES = (
        ('BUYER', 'Buyer'),
        ('SELLER', 'Seller'),
    )

    role = models.CharField(max_length=25, choices=ROLE_CHOICES, default='BUYER')

    def is_seller(self):
        return self.role == 'SELLER'

    def is_buyer(self):
        return self.role == 'BUYER'

class SellerProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='seller_profile',
        limit_choices_to={'role': 'SELLER'}
    )

    store_name = models.CharField(max_length=100)
    business_email = models.EmailField(null=True, blank=True, unique=True)
    phone_number = models.CharField(max_length=20)
    business_address = models.TextField(null=True, blank=True)
    tax_id = models.CharField(max_length=50, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @override
    def __str__(self):
        return f"{self.store_name} ({self.user.email})"
