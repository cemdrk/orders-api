from django.db import models

from django.contrib.auth.models import User


class Restaurant(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)


class FoodCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)


class Food(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    category = models.ForeignKey(FoodCategory, on_delete=models.CASCADE)
    price = models.FloatField()


class Order(models.Model):
    PENDING = "P"
    ACCEPTED = "A"
    REJECTED = "R"

    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (ACCEPTED, "Accepted"),
        (REJECTED, "Rejected"),
    ]

    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default=PENDING)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    foods = models.ManyToManyField(Food)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def accept(self):
        self.status = Order.ACCEPTED
        self.save()
