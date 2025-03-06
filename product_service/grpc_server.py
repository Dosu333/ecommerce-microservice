import grpc
from concurrent import futures
import product_pb2
import product_pb2_grpc

# Dummy product data
PRODUCTS = {
    "1": {"available": True, "price": 5000.0},
    "2": {"available": False, "price": 2000.0},
}

class ProductService(product_pb2_grpc.ProductServiceServicer):
    def CheckStock(self, request, context):
        product = PRODUCTS.get(request.id, None)
        if product:
            return product_pb2.ProductResponse(available=product["available"], price=product["price"])
        return product_pb2.ProductResponse(available=False, price=0.0)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    product_pb2_grpc.add_ProductServiceServicer_to_server(ProductService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("gRPC Product Service is running on port 50051...")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
