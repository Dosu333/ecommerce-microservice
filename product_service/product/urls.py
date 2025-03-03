from django.urls import path
from .views import ProductAPIView, CategoryAPIView


urlpatterns = [
    path('products/', ProductAPIView.as_view(), name='products'),
    path('products/<str:product_id>/', ProductAPIView.as_view(), name='product'),
    path('categories/', CategoryAPIView.as_view(), name='categories'),
]