import grpc
import location_pb2
import location_pb2_grpc


print("Sending sample payload...")

channelL = grpc.insecure_channel("localhost:5005")
stub = location_pb2_grpc.LocationServiceStub(channelL)

location_id = location_pb2.Location(id=20)

response = stub.Get(location_id)
print(response)


channelP = grpc.insecure_channel("localhost:5005")
stub = location_pb2_grpc.PersonServiceStub(channelP)

person_id = location_pb2.Person(id=21)

response = stub.Get(person_id)
print(response)