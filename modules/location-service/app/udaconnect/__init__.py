from app.udaconnect.models import Location  # noqa
from app.udaconnect.schemas import LocationSchema  # noqa


def register_routes(api, app, root="api"):
    from app.udaconnect.controllers import api as location_service

    api.add_namespace(location_service, path=f"/{root}")