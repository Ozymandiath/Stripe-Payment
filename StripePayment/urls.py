from django.urls import path

from .views import ItemView, BuyItemIDView, OrderView, DeleteItemView

urlpatterns = [
    path("buy/", BuyItemIDView.as_view(), name="buy"),
    path("buy/<int:pk>", BuyItemIDView.as_view(), name="buy"),
    path("item/<int:pk>", ItemView.as_view(), name="item"),
    path("order/", OrderView.as_view(), name="order_redirect"),
    path("delete/<int:pk>/<int:pk1>", DeleteItemView.as_view(), name="delete"),
]
