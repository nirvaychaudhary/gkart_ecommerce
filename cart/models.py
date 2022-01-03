from django.db import models
from store.models import Product, Variation
from accounts.models import Account
# Create your models here.
class Cart(models.Model):
    cart = models.CharField(max_length=250, null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart

class CartItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, null=True, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.product)

    def sub_total(self):
        return self.product.price * self.quantity 