from django.db import models

from category.models import Category
from django.urls import reverse

# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=500, unique=True)
    slug = models.SlugField(max_length=300, unique=True)
    description = models.TextField(blank=True, null=True)
    price = models.PositiveIntegerField()
    images = models.ImageField(upload_to='images/store/product', blank=True, null=True)
    stock = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at =  models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name

    def get_product_detail_url(self):
        return reverse('store:product_detail', args=[self.category.slug, self.slug])

class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True)

    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True)

variation_category_choice = {
        ('color', 'color'),
        ('size', 'size'),
    }

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=50, choices=variation_category_choice)
    variation_value = models.CharField(max_length=250)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = VariationManager()

    def __str__(self):
        return str(self.variation_value)