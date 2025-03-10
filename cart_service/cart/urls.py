from django.urls import path
from .views import CartView, PersistCartView

urlpatterns = [
    path("cart/", CartView.as_view(), name="cart"),
    path("cart/persist/", PersistCartView.as_view(), name="persist_cart"),
]
