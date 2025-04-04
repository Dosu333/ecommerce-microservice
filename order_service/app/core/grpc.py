from decouple import config
import grpc
import product_pb2
import product_pb2_grpc

PRODUCT_SERVICE_GRPC = config("PRODUCT_SERVICE_GRPC")
channel = grpc.insecure_channel(PRODUCT_SERVICE_GRPC)
stub = product_pb2_grpc.ProductServiceStub(channel)

def check_product_availability(product_id, quantity):
    product_request = product_pb2.ProductRequest(id=product_id, quantity=quantity)
    product_response = stub.CheckStock(product_request)
    return product_response

def get_product_detail(product_id):
    product_request = product_pb2.ProductIdRequest(id=product_id)
    product_response = stub.GetProduct(product_request)
    return product_response

def reduce_product_stock(order_items):
    """
    Reduces stock for multiple products in a single gRPC request.

    :param order_items: List of dicts containing 'product_id' and 'quantity'
    :return: ReduceStockResponse object with success status and messages
    """
    stock_items = [
        product_pb2.ReduceStockItem(id=str(item.product_id), quantity=item.quantity)
        for item in order_items
    ]

    stock_request = product_pb2.ReduceStockRequest(items=stock_items)
    stock_response = stub.ReduceStock(stock_request)
    
    return stock_response