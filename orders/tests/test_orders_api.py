from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from orders.models import Food, FoodCategory, Restaurant, Order

CREATE_ORDER_URL = reverse("orders:create_and_list")
LIST_ORDER_URL = reverse("orders:create_and_list")


class OrdersAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="12345")
        food_category = FoodCategory.objects.create(name="test_category")
        restaurant = Restaurant.objects.create(name="test_restaurant")
        self.food = Food.objects.create(
            name="testfood", price=10, category=food_category, restaurant=restaurant
        )

    def test_create_order(self):
        payload = {"user": self.user.id, "foods": [self.food.id]}
        response = self.client.post(CREATE_ORDER_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_list_order(self):
        order = Order(user=self.user)
        order.save()
        order.foods.add(self.food)
        order.save()

        response = self.client.get(LIST_ORDER_URL)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
