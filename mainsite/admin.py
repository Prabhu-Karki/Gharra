import site
from django.contrib import admin
from .models import *
from django.utils.html import format_html
from django.urls import reverse



@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'locality', 'city', 'state')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'selling_price', 'discounted_price')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart_user','cart_user_id', 'cart_product', 'quantity')

@admin.register(OrderPlaced)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'customer_info', 'product_info', 'customer', 'product', 'quantity', 'ordered_date', 'status')
    def customer_info(self, obj):
        link = reverse('admin:mainsite_customer_change', args=[obj.customer.pk])
        return format_html('<a href="{}">{}</a>', link, obj.customer.name)

    def product_info(self, obj):
        link = reverse('admin:mainsite_product_change', args=[obj.product.title])
        return format_html('<a href="{}">{}</a>', link, obj.product.selling_price)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name','review_date', 'review')

@admin.register(BuyNow)
class BuyNowAdmin(admin.ModelAdmin):
    list_display = ('id', 'buyer','product')