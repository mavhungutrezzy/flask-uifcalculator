from flask import Flask
from flask_squeeze import Squeeze
from scout_apm.flask import ScoutApm
from flask_wtf.csrf import CSRFProtect
from flask_caching import Cache

from config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Attach Scout APM monitoring
    ScoutApm(app)

    csrf = CSRFProtect(app)

    Squeeze(app)

    cache = Cache(app)
    app.cache = cache

    from app.routes.home import home_bp
    from app.routes.uif import uif_bp
    from app.routes.errors import errors_bp
    from app.routes.api import api_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(uif_bp)
    app.register_blueprint(errors_bp)
    app.register_blueprint(api_bp)

    csrf.exempt(api_bp)

    return app
