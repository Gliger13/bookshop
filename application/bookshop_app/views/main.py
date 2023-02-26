"""Main pages views

Module contains routes for the main blueprint, which includes basic
information, home pages.
"""
from flask import Blueprint, render_template

__all__ = ["main_blueprint"]

main_blueprint = Blueprint(
    name="main_blueprint",
    import_name=__name__,
    static_folder="static",
    template_folder="templates"
)


@main_blueprint.route('/about')
def about_page():
    """Default route for home page"""
    return render_template("main/about.html")
