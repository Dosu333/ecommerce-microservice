import grpc
from concurrent import futures
import product_pb2
import product_pb2_grpc
from core.database import products_collection


class ProductService(product_pb2_grpc.ProductServiceServicer):
    def CheckStock(self, request, context):
        product = products_collection.find_one({"id": request.id})
        if product:
            return product_pb2.ProductResponse(available=product["stock"] > request.quantity, price=product["price"], vendor=product["vendor_id"], name=product['name'], slug=product["slug"])
        return product_pb2.ProductResponse(available=False, price=0.0, vendor="", name="", slug="")
    
    def GetProduct(self, request, context):
        product = products_collection.find_one({"id": request.id})
        if product:
            return product_pb2.ProductDetailResponse(id=product['id'], name=product['name'], slug=product['slug'], price=product['price'])
        return product_pb2.ProductDetailResponseResponse(id="", slug="", name="", price=0.0)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    product_pb2_grpc.add_ProductServiceServicer_to_server(ProductService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("gRPC Product Service is running on port 50051...")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
