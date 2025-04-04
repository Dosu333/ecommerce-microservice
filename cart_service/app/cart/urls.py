from django.urls import path
from .views import CartView, PersistCartView, ClearCartView

urlpatterns = [
    path("cart/", CartView.as_view(), name="cart"),
    path("cart/persist/", PersistCartView.as_view(), name="persist_cart"),
    path("cart/clear/", ClearCartView.as_view(), name="clear_cart")
]
