"""Media views

Module contains routes for the media blueprint, which includes loading files
from the media folder.
"""
from flask import Blueprint
from flask import Response
from flask import send_from_directory

media_blueprint = Blueprint(name="media_blueprint", import_name=__name__, static_folder="media")


@media_blueprint.route("/media/<path>", methods=["GET"])
def get_media(path: str) -> Response:
    """Route for any media file"""
    return send_from_directory(directory="media", path=path)
