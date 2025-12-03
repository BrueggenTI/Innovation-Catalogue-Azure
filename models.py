from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'user'
    __table_args__ = (
        db.Index('idx_user_email', 'email'),
        db.Index('idx_user_microsoft_id', 'microsoft_id'),
    )
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100))
    position = db.Column(db.String(100))
    department = db.Column(db.String(100))
    is_master_user = db.Column(db.Boolean, default=False)
    microsoft_id = db.Column(db.String(100), unique=True, nullable=True)  # Microsoft OID
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class UserGroup(db.Model):
    __tablename__ = 'user_group'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    creator = db.relationship('User', backref='created_groups')

class GroupMember(db.Model):
    __tablename__ = 'group_member'
    __table_args__ = (
        db.UniqueConstraint('group_id', 'user_id', name='unique_group_member'),
    )

    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('user_group.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    role = db.Column(db.String(20), default='member')  # owner, admin, member
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)

    group = db.relationship('UserGroup', backref=db.backref('members', cascade='all, delete-orphan'))
    user = db.relationship('User', backref='group_memberships')

class ContentShare(db.Model):
    __tablename__ = 'content_share'

    id = db.Column(db.Integer, primary_key=True)
    content_type = db.Column(db.String(50), nullable=False)  # custom_page, cocreation_draft
    content_id = db.Column(db.Integer, nullable=False)
    shared_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    shared_with_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    shared_with_group_id = db.Column(db.Integer, db.ForeignKey('user_group.id', ondelete='CASCADE'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    sharer = db.relationship('User', foreign_keys=[shared_by], backref='shared_content_by_me')
    recipient_user = db.relationship('User', foreign_keys=[shared_with_user_id], backref='shared_content_with_me')
    recipient_group = db.relationship('UserGroup', backref='shared_content')

class Notification(db.Model):
    __tablename__ = 'notification'

    id = db.Column(db.Integer, primary_key=True)
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # group_invite, content_share, role_change
    message = db.Column(db.Text, nullable=False)
    link = db.Column(db.String(200))
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    recipient = db.relationship('User', backref='notifications')

class Product(db.Model):
    __tablename__ = 'product'
    __table_args__ = (
        db.Index('idx_product_category', 'category'),
        db.Index('idx_product_name', 'name'),
        db.Index('idx_product_recipe_number', 'recipe_number'),
        db.Index('idx_product_created_at', 'created_at'),
        db.Index('idx_product_is_exclusive', 'is_exclusive'),
        db.Index('idx_product_product_type', 'product_type'),
        db.Index('idx_product_category_created', 'category', 'created_at'),
    )
    
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
    shelf_life = db.Column(db.String(100))  # Shelf life information (e.g., "12 months (365 days)")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ConceptSession(db.Model):
    __tablename__ = 'concept_session'
    __table_args__ = (
        db.Index('idx_concept_session_id', 'session_id'),
        db.Index('idx_concept_created_at', 'created_at'),
    )
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(36), unique=True, nullable=False)
    client_name = db.Column(db.String(100))
    client_email = db.Column(db.String(120))
    product_config = db.Column(db.Text)  # JSON string of configuration
    pdf_path = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Trend(db.Model):
    __tablename__ = 'trend'
    __table_args__ = (
        db.Index('idx_trend_category', 'category'),
        db.Index('idx_trend_report_type', 'report_type'),
        db.Index('idx_trend_created_at', 'created_at'),
        db.Index('idx_trend_category_report', 'category', 'report_type'),
    )
    
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
    __tablename__ = 'research_job'
    __table_args__ = (
        db.Index('idx_research_job_id', 'job_id'),
        db.Index('idx_research_user_id', 'user_id'),
        db.Index('idx_research_status', 'status'),
        db.Index('idx_research_created_at', 'created_at'),
    )
    
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

class CustomRecipePage(db.Model):
    __tablename__ = 'custom_recipe_page'
    __table_args__ = (
        db.Index('idx_custom_page_user_id', 'user_id'),
        db.Index('idx_custom_page_created_at', 'created_at'),
    )
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)  # Optional description for the custom page
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_ids = db.Column(db.Text, nullable=False)  # JSON array of product IDs
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = db.relationship('User', backref='custom_recipe_pages')

class CoCreationDraft(db.Model):
    __tablename__ = 'co_creation_draft'
    __table_args__ = (
        db.Index('idx_draft_user_id', 'user_id'),
        db.Index('idx_draft_created_at', 'created_at'),
    )
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    draft_name = db.Column(db.String(200), nullable=False)
    
    # Base product information
    base_product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=True)
    base_product_name = db.Column(db.String(200), nullable=True)
    
    # Custom ingredients and ratios
    custom_ingredients = db.Column(db.Text, nullable=True)  # JSON array of ingredient names
    ingredient_ratios = db.Column(db.Text, nullable=True)  # JSON object with ingredient percentages/grams
    
    # Claims and certifications
    nutritional_claims = db.Column(db.Text, nullable=True)  # JSON array of selected claims
    certifications = db.Column(db.Text, nullable=True)  # JSON array of selected certifications
    
    # Client information
    client_name = db.Column(db.String(200), nullable=True)
    client_email = db.Column(db.String(200), nullable=True)
    notes = db.Column(db.Text, nullable=True)  # Special notes/requirements
    
    # Full configuration as JSON (for backwards compatibility and future flexibility)
    product_config = db.Column(db.Text, nullable=False)  # JSON string of Co-Creation configuration
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = db.relationship('User', backref='cocreation_drafts')
    base_product = db.relationship('Product', backref='cocreation_drafts')
