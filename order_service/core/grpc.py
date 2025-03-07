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