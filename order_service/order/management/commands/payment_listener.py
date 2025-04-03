from django.core.management.base import BaseCommand
from decouple import config
from core.grpc import reduce_product_stock
from order.models import Order
import redis
import time

host = config("REDIS_HOST")
port = config("REDIS_PORT")
redis_client = redis.Redis(host=host, port=port, db=0, decode_responses=True)

class Command(BaseCommand):
    help = "Listen to the payment_stream and update order status"

    def handle(self, *args, **kwargs):
        last_id = "0"
        self.stdout.write("Listening for payment...")

        while True:
            try:
                result = redis_client.xread({"payment_stream": last_id}, block=5000, count=10)

                if result:
                    stream, messages = result[0]
                    for message_id, message_data in messages:
                        order_id = message_data.get("order_id")
                        status = message_data.get("status")

                        self.stdout.write(f"Received payment update for order: {order_id}, status: {status}")

                        if status == "paid":
                            order = Order.objects.filter(id=order_id)
                            if not order.first().is_paid:  
                                updated_count = order.update(is_paid=True)
                                if updated_count > 0:
                                    order_instance = order.first()
                                    order_items = order_instance.items.all()
                                    reduce_product_stock(order_items)
                                    self.stdout.write(f"Order {order_id} marked as paid.")
                                else:
                                    self.stdout.write(f"No matching order found for ID: {order_id}")
                            else:
                                self.stdout.write(f"Order for ID: {order_id} is already paid for")

                        last_id = message_id

            except Exception as e:
                self.stdout.write(f"Error listening to payment stream: {e}")
                time.sleep(2)
