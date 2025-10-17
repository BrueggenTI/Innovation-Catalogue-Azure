# Brüggen Innovation Catalogue

## Overview
The Brüggen Innovation Catalogue is a B2B digital tool designed for H. & J. Brüggen KG's sales team. This tablet-optimized web application facilitates collaborative discussions with retail clients, showcasing product capabilities, market trends, and enabling real-time product co-creation. It authentically represents Brüggen's brand identity as "The World of Cereals," focusing on muesli, oats, and grain products, and aims to be a comprehensive innovation platform.

## User Preferences
Preferred communication style: Simple, everyday language.
Recipe creation workflow: Form must be immediately editable after AI analysis without additional clicks.

## System Architecture
The application uses a Flask-based web architecture with server-side rendering and progressive enhancement via JavaScript. It follows a modular design with three core functional areas: competence showcase, trend insights, and interactive co-creation.

### Technology Stack
- **Backend**: Python Flask with SQLAlchemy ORM
- **Frontend**: HTML templates with Bootstrap 5, vanilla JavaScript, custom CSS
- **Database**: SQLite (development) with PostgreSQL support
- **Authentication**: Microsoft Azure AD Single Sign-On (MSAL Python, Flask-Session)
- **Email**: Flask-Mail for PDF delivery
- **PDF Generation**: ReportLab
- **Styling**: Bootstrap framework, custom CSS, Montserrat font, 8px-based spacing grid

### Core Modules and Features
- **Innovation Catalog Module (`/catalog`)**: Showcases existing product formulations and manufacturing capabilities through a filterable product database with detailed views, high-quality imagery, and specifications.
- **Trends & Insights Module (`/trends`)**: Presents market trends and consumer insights (health, sustainability, innovation) with market data and a visual exploration interface.
- **Co-Creation Lab Module (`/cocreation`)**: Provides a multi-step, interactive product building workflow for real-time ingredient selection and customization. It generates and emails PDF concept summaries and stores configurations session-based.
- **Recipe Creation Module (`/add-recipe`)**: Offers AI-powered document analysis (PDF, DOC, DOCX, TXT, PPT, PPTX) for product creation. Includes image upload, interactive recipe editing and validation, and direct integration with the Innovation Catalog. AI analysis includes automatic German-to-English translation and detailed extraction of ingredients, percentages, and nutritional data, which is immediately editable. All ingredient percentages and nutritional values are automatically rounded to one decimal place for consistency across both single and batch upload workflows.

### Design and UI/UX
- Authentic Brüggen branding: Burgundy (#661c31) and coral (#ff4143) color scheme.
- Montserrat font family and 8px-based spacing grid system.
- Responsive design adhering to a max content width of 1280px.
- Card-based layouts, dynamic breadcrumb navigation, and contextual back buttons for improved usability.

### Technical Implementation
- **Data Flow**: Structured flows for product exploration, trend discovery, and multi-step co-creation.
- **Data Models**: Comprehensive schemas for `Product`, `Trend`, and `ConceptSession` including flexible JSON-stored attributes for ingredients, claims, nutritional info, and session configurations.
- **Deployment**: Environment configuration for development (SQLite) and production (PostgreSQL), secure session management, and local file system storage for static assets and generated PDFs.
- **Security**: CSRF protection, file upload validation, size restrictions, environment-based credential configuration, ProxyFix middleware, and Microsoft Azure AD authentication.
- **Authentication**: Optional Microsoft SSO with tenant-specific Azure AD integration. Features include:
  - Secure OAuth 2.0 flow with MSAL for Python
  - CSRF protection via state token validation
  - Session-based user authentication tracking
  - Integration with Microsoft Graph API for user profile data
  - Automatic Azure AD logout for complete session termination
  - Route protection decorator (`@login_required`) for sensitive endpoints
  - Visual authentication status indicators in UI

## External Dependencies

- **Email Integration**: SMTP-based email delivery (Gmail default) for automated concept PDF delivery.
- **Image Assets**: Unsplash CDN for product and trend imagery.
- **Frontend Libraries**: Bootstrap 5 for UI framework, Font Awesome for icons.
- **AI/Document Processing**: OpenAI GPT-4 API for document analysis, PyPDF2, python-docx, python-pptx for authentic document parsing.
- **Microsoft Azure AD**: Enterprise authentication via Azure Active Directory. Requires Azure AD tenant configuration and environment variables (CLIENT_ID, CLIENT_SECRET, TENANT_ID, AUTHORITY, REDIRECT_URI). See `AZURE_SSO_SETUP.md` for detailed setup instructions.