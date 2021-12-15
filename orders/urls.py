from django.urls import path

from orders import views


app_name = "orders"

urlpatterns = [
    path("", views.OrdersAPIView.as_view(), name="create_and_list"),
]
