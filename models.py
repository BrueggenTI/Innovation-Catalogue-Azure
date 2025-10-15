from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100))
    position = db.Column(db.String(100))
    department = db.Column(db.String(100))
    is_master_user = db.Column(db.Boolean, default=False)
    microsoft_id = db.Column(db.String(100), unique=True, nullable=True)  # Microsoft OID
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    ingredients = db.Column(db.Text)  # JSON string of ingredients with percentages
    nutritional_claims = db.Column(db.Text)  # JSON string of claims
    certifications = db.Column(db.Text)  # JSON string of certifications
    nutritional_info = db.Column(db.Text)  # JSON string of nutritional values
    allergens = db.Column(db.Text)  # JSON string of allergen information
    claims = db.Column(db.Text)  # JSON string of product claims
    storage_conditions = db.Column(db.Text)  # Storage conditions text
    image_url = db.Column(db.String(200))  # Main product image
    nutri_score_image = db.Column(db.String(200))  # URL to Nutri-Score image
    case_study = db.Column(db.Text)
    production_tech = db.Column(db.String(100))
    recipe_number = db.Column(db.String(50))  # Store extracted recipe number from documents
    is_exclusive = db.Column(db.Boolean, default=False)  # Whether this is an exclusive recipe
    product_type = db.Column(db.String(50), default='Development')  # Product or Development
    department = db.Column(db.String(100))  # Department information (e.g., Production, R&D)
    customer = db.Column(db.String(200))  # Customer name or company (mutually exclusive with market)
    market = db.Column(db.String(200))  # Market information (mutually exclusive with customer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ConceptSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(36), unique=True, nullable=False)
    client_name = db.Column(db.String(100))
    client_email = db.Column(db.String(120))
    product_config = db.Column(db.Text)  # JSON string of configuration
    pdf_path = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Trend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # health, sustainability, innovation
    report_type = db.Column(db.String(50), nullable=False, default='produktentwicklung')  # produktentwicklung, marktdaten
    description = db.Column(db.Text)
    market_data = db.Column(db.Text)
    consumer_insights = db.Column(db.Text)
    image_url = db.Column(db.String(200))
    pdf_path = db.Column(db.String(200))  # Path to uploaded PDF document
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ResearchJob(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.String(36), unique=True, nullable=False)  # UUID
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    description = db.Column(db.Text, nullable=False)
    keywords = db.Column(db.Text)  # JSON array of keywords
    categories = db.Column(db.Text)  # JSON array of categories
    research_plan = db.Column(db.Text)  # JSON object with detailed research plan
    plan_approved = db.Column(db.Boolean, default=False)  # Whether user approved the plan
    status = db.Column(db.String(50), default='queued')  # queued, generating_plan, waiting_approval, processing_strategy, scraping_data, synthesizing_report, finalizing_report, generating_pdf, completed, failed, cancelled
    progress = db.Column(db.Integer, default=0)
    status_log = db.Column(db.Text)  # JSON array of status updates
    result_trend_id = db.Column(db.Integer, db.ForeignKey('trend.id'), nullable=True)
    error_message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    user = db.relationship('User', backref='research_jobs')
    result_trend = db.relationship('Trend', backref='research_job')

class ResearchSource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.String(36), db.ForeignKey('research_job.job_id'), nullable=False)
    source_name = db.Column(db.String(100), nullable=False)
    source_url = db.Column(db.String(500))
    status = db.Column(db.String(50), default='pending')  # pending, processing, success, failed
    found_items = db.Column(db.Integer, default=0)
    cleaned_content = db.Column(db.Text)  # Extracted and cleaned data
    error_message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    research_job = db.relationship('ResearchJob', backref='sources')
