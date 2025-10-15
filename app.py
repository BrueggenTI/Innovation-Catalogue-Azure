import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_session import Session
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_talisman import Talisman
from flask_wtf.csrf import CSRFProtect

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
mail = Mail()

# create the app
app = Flask(__name__)

# Require SESSION_SECRET from environment - fail fast if missing
session_secret = os.environ.get("SESSION_SECRET")
if not session_secret:
    raise RuntimeError(
        "SESSION_SECRET environment variable is required but not set. "
        "Please configure SESSION_SECRET before starting the application."
    )
app.secret_key = session_secret
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure Flask-Session for Microsoft SSO
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_USE_SIGNER"] = True
app.config["SESSION_FILE_THRESHOLD"] = 100
Session(app)

# configure the database
database_url = os.environ.get("DATABASE_URL", "sqlite:///bruggen_innovation.db")
app.config["SQLALCHEMY_DATABASE_URI"] = database_url

# Configure engine options based on database type
if database_url.startswith("postgresql"):
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
        "pool_size": 10,
        "max_overflow": 20,
        "connect_args": {
            "connect_timeout": 10,
            "keepalives": 1,
            "keepalives_idle": 30,
            "keepalives_interval": 10,
            "keepalives_count": 5,
        }
    }
else:
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }

# configure mail
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', '587'))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'innovation@bruggen.com')

# initialize extensions
db.init_app(app)
mail.init_app(app)

# Configure CSRF protection
csrf = CSRFProtect(app)

# Add minimal security headers for PDF embedding only
@app.after_request
def add_security_headers(response):
    # Allow PDFs to be embedded from same origin
    if response.mimetype == 'application/pdf':
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    
    return response

# Security enhancements
# In development: Disable CSP to avoid issues with CDN source maps and debugging
# In production: Enable strict CSP
if os.environ.get('FLASK_ENV') == 'production':
    csp = {
        'default-src': "'self'",
        'script-src': "'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com",
        'style-src': "'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com https://fonts.googleapis.com",
        'font-src': "'self' https://fonts.gstatic.com https://cdnjs.cloudflare.com",
        'img-src': "'self' data: https://images.unsplash.com https://plus.unsplash.com",
        'connect-src': "'self' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com"
    }
    Talisman(app, 
             force_https=True,
             content_security_policy=csp)
else:
    # Development: Minimal CSP to allow debugging tools and source maps
    Talisman(app, 
             force_https=False,
             content_security_policy=False)  # Disable CSP in development

# Add custom Jinja2 filters
import json
def from_json_filter(value):
    try:
        return json.loads(value) if value else []
    except (json.JSONDecodeError, TypeError):
        return []

app.jinja_env.filters['from_json'] = from_json_filter

# Initialize database tables when app starts
with app.app_context():
    # import models to ensure tables are created
    import models
    try:
        db.create_all()
        logging.info("Database tables created successfully")
    except Exception as e:
        logging.error(f"Database initialization error: {e}")
        # Continue running even if DB initialization fails
        pass

# Import after app creation to avoid circular imports
from translations import get_text, get_available_languages
from flask import session

@app.context_processor
def inject_translations():
    """Make translation functions available in all templates"""
    return dict(
        get_text=get_text,
        lang=session.get('language', 'en'),
        available_languages=get_available_languages()
    )

# import routes
from routes import *
