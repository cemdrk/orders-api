from rest_framework import status, views
from rest_framework.response import Response

from ordersapi.message_queue import publish
from orders.models import Order
from orders.serializers import OrderSerializer


class OrdersAPIView(views.APIView):
    def get_queryset(self):
        queryset = Order.objects.all()
        status = self.request.query_params.get("status")
        if status is not None:
            queryset = queryset.filter(status=status)
        return queryset

    def post(self, request, *args, **kwargs):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            publish(serializer.data.get("id"))
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        orders = self.get_queryset()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
