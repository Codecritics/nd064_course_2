import os
from datetime import datetime

from app.udaconnect.models import Location
from app.udaconnect.schemas import LocationSchema
from app.udaconnect.services import LocationService
from flask import request
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource
from kafka import KafkaProducer
from typing import Optional, List
from json import dumps

KAFKA_HOST = os.environ['KAFKA_HOST']
KAFKA_PORT = os.environ['KAFKA_PORT']
KAFKA_TOPIC = os.environ['KAFKA_TOPIC']

DATE_FORMAT = "%Y-%m-%d"
producer = KafkaProducer(bootstrap_servers=[f'{KAFKA_HOST}: {KAFKA_PORT}'],
                         value_serializer=lambda x: dumps(x).encode('utf-8'))
api = Namespace("udaconnect-location", description="Locations of Persons.")  # noqa


@api.route("/locations")
@api.route("/locations/<location_id>")
@api.param("location_id", "Unique ID for a given Location", _in="query")
class LocationResource(Resource):
    @accepts(schema=LocationSchema)
    @responds(schema=LocationSchema)
    def post(self) -> Location:
        try:
            payload = request.get_json()
            creation_time = request["creation_time"].isoformat()
            request_body = {
                "id": payload["id"],
                "person_id": payload["person_id"],
                "longitude": payload["longitude"],
                "latitude": payload["latitude"],
                "creation_time": creation_time
            }
            producer.send(KAFKA_TOPIC, request_body)
            producer.flush()

            return request_body
        except Exception as e:
            return {"error": str(e)}, 400

    @responds(schema=LocationSchema)
    def get(self, location_id) -> Location:
        location: Location = LocationService.retrieve(location_id)
        return location
