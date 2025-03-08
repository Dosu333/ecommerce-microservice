from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("failed", "Failed"),
        ("cancelled", "Cancelled"),
    ]

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user_id = models.UUIDField(blank=True, null=True)
    vendor_id = models.UUIDField(blank=True, null=True)
    total_price = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    address = models.CharField(max_length=225, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id}"
    
    def update_total_price(self):
        """Calculate and update total order price"""
        self.total_price = sum(item.total_price() for item in self.items.all())
        self.save()
        
class OrderItem(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product_id = models.UUIDField()
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def total_price(self):
        return self.unit_price * self.quantity

    def __str__(self):
        return f"Item {self.product_id} in Order {self.order.id}"
