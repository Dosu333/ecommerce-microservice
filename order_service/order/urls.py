from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, RetryPaymentView

app_name = 'order'

router = DefaultRouter()

router.register('orders', OrderViewSet, basename='orderviewsets')

urlpatterns = [
    path('', include(router.urls)),
    path('retry-payment/<str:order_id>/', RetryPaymentView.as_view()),
]