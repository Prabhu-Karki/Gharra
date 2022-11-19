from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

STATE_CHOICES = (

    ('Province 1', ' Province 1'),
    ('Madesh Pradesh', 'Madesh Pradesh'),
    ('Bagmati Pradesh', 'Bagmati Pradesh'),
    ('Gandaki Pradesh', 'Gandaki Pradesh'),
    ('Lumbini Pradesh', "Lumbini Pradesh"),
    ('Karnali Pradesh', 'Karnali Pradesh'),
    ('Sudhurpaschim Pradesh', "Sudhurpaschim Pradesh")
)

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    name = models.CharField(max_length=50)
    locality=models.CharField(max_length=250)
    city =models.CharField(max_length=50)
    email = models.EmailField()   
    phone = models.PositiveIntegerField(blank=False)   
    state = models.CharField(choices=STATE_CHOICES, max_length=50)

    def __str__(self):
        return str(self.id)

CATEGORY_CHOICES = (
    ('M', "Mobile"),
    ('L', "Laptop"),
)
BRAND_CHOICES = (
    ('AP', "Apple"),
    ('XI', "Xiaomi"),
    ('DE', "Dell"),
    ('HP', "HP"),
    ('SA', "Samsung"),
)
PRODUCT_STATUS = (
    ('NA', 'New Arrival'),
    ('SP', "Special Product")
)
class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    brand = models.CharField(choices=BRAND_CHOICES, max_length=2)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    primary_image = models.ImageField(upload_to= 'productimg')
    secondary_image = models.ImageField(upload_to= 'productimg')
    product_status = models.CharField(choices=PRODUCT_STATUS, max_length=2)


    def __str__(self):
        return str(self.id)

class Cart(models.Model):
    cart_user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    product_color = models.CharField(max_length = 30, blank= True, default='Black')
    product_storage = models.PositiveIntegerField(default=64)

    def __str__(self):
        return str(self.cart_product)

    @property
    def total_cost(self):
        return self.quantity * self.cart_product.discounted_price

class BuyNow(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    color = models.CharField(max_length = 30, blank= True, default='Black')
    storage = models.PositiveIntegerField(default=64)

    def __str__(self):
        return str(self.product)

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

STATUS_CHOICES = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On Your Way', 'On Your Way '), 
    ('Delivered', 'Delivered'),
    ('Cancel', 'Cancel'),
)

class Review(models.Model):
    customer_name = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    review_date = models.DateField(auto_now_add=True)
    review = models.TextField(max_length=500)
    rating = models.FloatField(default=0, null=True)

class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    payment_method = models.CharField(default= 'pending', max_length=50)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOICES, default='pending', max_length=50)

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price
