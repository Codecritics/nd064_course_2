from app.udaconnect.models import Person  # noqa
from app.udaconnect.schemas import PersonSchema  # noqa


def register_routes(api, app, root="api"):
    from app.udaconnect.controllers import api as person_service

    api.add_namespace(person_service, path=f"/{root}")
