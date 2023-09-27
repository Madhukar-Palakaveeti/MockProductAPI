from django.db import models

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=200,blank=True)
    price = models.CharField(max_length=10,blank=True)
    rating = models.CharField(max_length=4, blank=True)
    discount = models.CharField(max_length=11, blank=False, default='No Discount')