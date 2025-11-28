from flask import Blueprint, render_template

errors_bp = Blueprint("errors", __name__)


@errors_bp.app_errorhandler(404)
def not_found_error(error):
    return render_template("pages/404.html")


@errors_bp.app_errorhandler(500)
def internal_error(error):
    return render_template("pages/500.html")