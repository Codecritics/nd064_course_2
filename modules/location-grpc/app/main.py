import time, os
from concurrent import futures
import grpc
import location_pb2
import location_pb2_grpc
from models import session, Location
from json import dumps
from kafka import KafkaProducer
import logging

KAFKA_TOPIC = os.environ["KAFKA_TOPIC"]
KAFKA_PORT = os.environ["KAFKA_PORT"]
KAFKA_HOST = os.environ["KAFKA_HOST"]

producer = KafkaProducer(bootstrap_servers=[f'{KAFKA_HOST}:{KAFKA_PORT}'],
                         value_serializer=lambda x: dumps(x).encode('utf-8'))

logging.basicConfig(
    level=logging.DEBUG,
    filemode='w',
    format='%(name)s - %(levelname)s - %(message)s')


class LocationServicer(location_pb2_grpc.LocationServiceServicer):
    def Get(self, request, context):
        id_ = request.id
        location = session.query(Location).filter(Location.id == id_).first()
        if not location:
            return location_pb2.LocationSchema(id=id_, person_id=None, longitude=None, latitude=None, creation_time=None)
        else:
            return location_pb2.LocationSchema(**{
                "id": location.id,
                "person_id": location.person_id,
                "longitude": location.longitude,
                "latitude": location.latitude,
                "creation_time": location.creation_time.isoformat(),
            })

    def Create(self, request, context):
        logging.info("Received a message!")

        request_value = {
            "id": request.id,
            "person_id": request.person_id,
            "longitude": request.longitude,
            "latitude": request.latitude,
            "creation_time": request.creation_time,
        }

        try:
            producer.send(KAFKA_TOPIC, request_value)
            return location_pb2.LocationSchema(**request_value)
        except Exception as e:
            logging.error("Exception found: {}".format(e))
            return location_pb2.LocationSchema(**{
                "id": None,
                "person_id": None,
                "longitude": None,
                "latitude": None,
                "creation_time": None,
            })


server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
location_pb2_grpc.add_LocationServiceServicer_to_server(LocationServicer(), server)

logging.info("Server starting on port 5005...")
server.add_insecure_port("[::]:5005")
server.start()
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
