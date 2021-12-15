from rest_framework import serializers

from orders.models import Order, Food
from django.contrib.auth.models import User


class OrderSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    status = serializers.CharField(required=False)
    foods = serializers.PrimaryKeyRelatedField(many=True, queryset=Food.objects.all())

    class Meta:
        model = Order
        fields = ("id", "user", "status", "foods")
