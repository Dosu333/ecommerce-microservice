from django.urls import path
from .views import ProductAPIView, CategoryAPIView, ReviewAPIView


urlpatterns = [
    path('products/', ProductAPIView.as_view(), name='products'),
    path('products/<str:product_id>/', ProductAPIView.as_view(), name='product'),
    path('categories/', CategoryAPIView.as_view(), name='categories'),
    path('categories/<str:category_id>/', CategoryAPIView.as_view(), name='category'),
    path('reviews/', ReviewAPIView.as_view(), name="reviews")
]