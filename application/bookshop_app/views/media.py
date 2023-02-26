from flask import Blueprint, send_from_directory

media_blueprint = Blueprint(
    name="media_blueprint",
    import_name=__name__,
    static_folder="media"
)


@media_blueprint.route('/media/<path>', methods=["GET"])
def get_media(path: str):
    """Route for any media file"""
    return send_from_directory(directory="media", path=path)
