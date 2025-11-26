
import os
import logging
from flask import Flask, request, session
from flask_mail import Mail
from flask_migrate import Migrate
from flask_session import Session
from flask_compress import Compress
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_talisman import Talisman
from flask_wtf.csrf import CSRFProtect
import json

from database import db
from translations import get_text, get_available_languages

# App initialization
app = Flask(__name__)
csrf = CSRFProtect()

# Basic app configuration
log_level = logging.INFO if os.environ.get('FLASK_ENV') == 'production' else logging.DEBUG
logging.basicConfig(level=log_level)

session_secret = os.environ.get("SESSION_SECRET")
if not session_secret:
    raise RuntimeError("SESSION_SECRET environment variable is required.")
app.secret_key = session_secret
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure Flask-Session
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_USE_SIGNER"] = True
app.config["SESSION_FILE_THRESHOLD"] = 100
Session(app)

# Configure database
database_url = os.environ.get("DATABASE_URL", "sqlite:///bruggen_innovation.db")
app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_ECHO"] = False
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_recycle": 300, "pool_pre_ping": True}

# Initialize extensions
db.init_app(app)
Mail(app)
Compress(app)
Migrate(app, db)
csrf.init_app(app)

# Security with Talisman
if os.environ.get('FLASK_ENV') == 'production':
    Talisman(app, force_https=True)
else:
    Talisman(app, force_https=False, content_security_policy=None)

# Jinja2 filter
def from_json_filter(value):
    try:
        return json.loads(value) if value else []
    except (json.JSONDecodeError, TypeError):
        return []
app.jinja_env.filters['from_json'] = from_json_filter

# Import models and create tables
with app.app_context():
    import models
    try:
        db.create_all()
        logging.info("Database tables created successfully")
    except Exception as e:
        logging.error(f"Database initialization error: {e}")

# Import routes at the end to avoid circular dependency
from routes import *

@app.context_processor
def inject_translations():
    return dict(
        get_text=get_text,
        lang=session.get('language', 'en'),
        available_languages=get_available_languages()
    )

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
