from flask import Blueprint, render_template, current_app, send_from_directory

home_bp = Blueprint("home", __name__)


@home_bp.route("/")
def index():
    return render_template("home.html")


@home_bp.route("/robots.txt")
def robots_txt():
    """Serve the robots.txt file from the static directory."""
    return send_from_directory(
        current_app.static_folder, "robots.txt", mimetype="text/plain"
    )


@home_bp.route("/sitemap.xml")
def sitemap_xml():
    """Serve the sitemap.xml file from the static directory."""
    return send_from_directory(
        current_app.static_folder, "sitemap.xml", mimetype="application/xml"
    )


@home_bp.route("/ads.txt")
def ads_txt():
    """Serve the ads.txt file from the static directory."""
    return send_from_directory(
        current_app.static_folder, "ads.txt", mimetype="text/plain"
    )
