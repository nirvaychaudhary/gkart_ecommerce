from django.contrib import admin
from .models import *
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('product_name',)}
    list_display = ('product_name', 'slug', 'category', 'price', 'stock', 'is_available', 'created_at', 'modified_at',)

class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active', 'created_at',)
    list_editable = ('is_active',)
    list_filter = ('product', 'variation_category', 'variation_value', 'is_active',)

admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
