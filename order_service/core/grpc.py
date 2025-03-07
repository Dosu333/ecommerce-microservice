from decouple import config
import grpc
import product_pb2
import product_pb2_grpc

PRODUCT_SERVICE_GRPC = config("PRODUCT_SERVICE_GRPC")

def check_product_availability(product_id, quantity):
    channel = grpc.insecure_channel(PRODUCT_SERVICE_GRPC)
    stub = product_pb2_grpc.ProductServiceStub(channel)
    product_request = product_pb2.ProductRequest(id=product_id, quantity=quantity)
    product_response = stub.CheckStock(product_request)
    return product_response