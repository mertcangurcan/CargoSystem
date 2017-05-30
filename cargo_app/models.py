from django.db import models
from users.models import User

class CorporateUser(models.Model):
    name = models.CharField(max_length=30)
    telephone = models.IntegerField()
    address = models.CharField(max_length=300)


class Category(models.Model):
    name = models.CharField(max_length=5)
    quantity = models.IntegerField(default=10)
    cat_price = models.FloatField(default=1.00)

class Shipment(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE,blank=True)
    categoryID = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    trackID = models.CharField(max_length=12)
    source_address = models.CharField(max_length=300)
    destination_address = models.CharField(max_length=300)
    sending_date = models.DateField()
    arrival_date = models.DateField(null=True, blank=True)
    isReceived = models.BooleanField(default=False)
    price = models.FloatField(default=7.00)

class CorporateShipment(models.Model):
    customer_name = models.CharField(max_length=15, default=None)
    customer_surname = models.CharField(max_length=15, default=None)
    corporateID = models.ForeignKey(CorporateUser, on_delete=models.CASCADE)
    categoryID = models.ForeignKey(Category, on_delete=models.CASCADE)
    trackID = models.CharField(max_length=12)
    source_address = models.CharField(max_length=300)
    destination_address = models.CharField(max_length=300)
    sending_date = models.DateField()
    arrival_date = models.DateField(null=True)
    isReceived = models.BooleanField(default=False)