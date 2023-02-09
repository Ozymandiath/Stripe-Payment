from django.urls import path

from .views import ItemView, BuyItemIDView

urlpatterns = [
    path("buy/<int:pk>", BuyItemIDView.as_view(), name="buy"),
    path("item/<int:pk>", ItemView.as_view(), name="item"),
]
