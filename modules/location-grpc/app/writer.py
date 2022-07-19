import grpc
import location_pb2
import location_pb2_grpc
from datetime import datetime

print("Sending a location payload")

channel = grpc.insecure_channel("localhost:5005")
stub = location_pb2_grpc.LocationServiceStub(channel)

location = location_pb2.LocationSchema(
    id=1,
    person_id=1,
    longitude="48.85660000000000001",
    latitude="2.352200000000000001",
    creation_time=datetime.now().isoformat(),
)

response = stub.Create(location)

print(response)
