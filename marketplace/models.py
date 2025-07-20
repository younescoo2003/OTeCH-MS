from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Category(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
    )
    slug = models.SlugField(
        unique=True
    )

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(
        max_length=255
    )
    description = models.TextField()
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products'

    )
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )
    image = models.ImageField(
        upload_to='products/',
        null=True,
        blank=True
    )
    is_available = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.name

class CartItem(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart_items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(
        default=1
    )

    def total_price(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"