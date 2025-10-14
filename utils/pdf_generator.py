from reportlab.lib.pagesizes import A4, letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate
from reportlab.platypus.frames import Frame
import json
import os
from datetime import datetime
from io import BytesIO
import urllib.request

def generate_concept_pdf(concept_session):
    """Generate a PDF concept summary matching the Live Preview layout exactly - side-by-side cards"""
    
    # Create directory if it doesn't exist
    pdf_dir = 'static/pdfs'
    os.makedirs(pdf_dir, exist_ok=True)
    
    # Generate filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'concept_{concept_session.session_id}_{timestamp}.pdf'
    filepath = os.path.join(pdf_dir, filename)
    
    # Create PDF document
    doc = SimpleDocTemplate(filepath, pagesize=A4, 
                          leftMargin=0.75*inch, rightMargin=0.75*inch, 
                          topMargin=0.75*inch, bottomMargin=0.75*inch)
    styles = getSampleStyleSheet()
    story = []
    
    # Custom styles matching Brüggen branding
    title_style = ParagraphStyle(
        'BruggenTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#661c31'),  # Brüggen burgundy
        alignment=TA_CENTER,
        spaceAfter=10,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'BruggenSubtitle',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#ff4143'),  # Brüggen coral
        alignment=TA_CENTER,
        spaceAfter=20,
        fontName='Helvetica-Bold'
    )
    
    header_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#661c31'),
        spaceBefore=15,
        spaceAfter=10,
        fontName='Helvetica-Bold'
    )
    
    card_header_style = ParagraphStyle(
        'CardHeader',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=colors.HexColor('#661c31'),
        spaceBefore=5,
        spaceAfter=8,
        fontName='Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#212529'),
        spaceAfter=6,
        fontName='Helvetica'
    )
    
    product_title_style = ParagraphStyle(
        'ProductTitle',
        parent=styles['Heading3'],
        fontSize=16,
        textColor=colors.HexColor('#661c31'),
        alignment=TA_CENTER,
        spaceAfter=8,
        fontName='Helvetica-Bold'
    )
    
    # Header with Brüggen branding
    story.append(Paragraph("H. & J. Brüggen KG", title_style))
    story.append(Paragraph("Innovation Concept Summary", subtitle_style))
    story.append(Spacer(1, 20))
    
    # Parse product configuration
    config = {}
    if concept_session.product_config:
        try:
            config = json.loads(concept_session.product_config)
        except json.JSONDecodeError:
            config = {}
    
    # Product Preview Section (matching the Live Preview)
    if config.get('baseProductName'):
        story.append(Paragraph("Live Preview", header_style))
        
        # Try to download and include the product image
        product_image = None
        if config.get('baseProductImage'):
            try:
                # Handle both full URLs and relative paths
                image_url = config['baseProductImage']
                if image_url.startswith('http'):
                    with urllib.request.urlopen(image_url) as response:
                        product_image = Image(BytesIO(response.read()), width=150, height=150)
                else:
                    # Try local path
                    local_path = image_url.lstrip('/')
                    if os.path.exists(local_path):
                        product_image = Image(local_path, width=150, height=150)
            except Exception as e:
                print(f"Could not load product image: {e}")
        
        if product_image:
            product_image.hAlign = 'CENTER'
            story.append(product_image)
            story.append(Spacer(1, 10))
        
        # Product title (matching preview)
        story.append(Paragraph(config['baseProductName'], product_title_style))
        
        # Custom ingredients subtitle (matching preview)
        if config.get('customIngredients'):
            custom_count = len(config['customIngredients'])
            if custom_count > 0:
                subtitle_text = f"+ {custom_count} custom ingredient{'s' if custom_count > 1 else ''}"
                story.append(Paragraph(subtitle_text, normal_style))
        
        story.append(Spacer(1, 20))
    
    # Side-by-side cards layout (matching Live Preview exactly)
    # Create Recipe Details and Current Configuration cards
    
    # Recipe Details Card Content
    recipe_details = []
    recipe_details.append(Paragraph("Recipe Details", card_header_style))
    
    # Base ingredients section with unapproved raw material marking
    if config.get('baseIngredients'):
        recipe_details.append(Paragraph("<b>Base Ingredients:</b>", ParagraphStyle('BoldLabel', parent=normal_style, fontName='Helvetica-Bold')))
        if isinstance(config['baseIngredients'], list):
            for ingredient in config['baseIngredients']:
                # Check if ingredient is a structured object or just a string
                if isinstance(ingredient, dict):
                    ing_name = ingredient.get('display') or ingredient.get('name', str(ingredient))
                    # Check for unapproved raw material status
                    if ingredient.get('status') == 'unapproved_raw_material':
                        # Red color style for unapproved ingredients
                        unapproved_style = ParagraphStyle(
                            'UnapprovedIngredient',
                            parent=normal_style,
                            textColor=colors.HexColor('#dc3545'),  # Bootstrap danger red
                            fontName='Helvetica-Bold'
                        )
                        recipe_details.append(Paragraph(f"• {ing_name} <font color='#dc3545'><b>[UNAPPROVED RAW MATERIAL]</b></font>", unapproved_style))
                    else:
                        recipe_details.append(Paragraph(f"• {ing_name}", normal_style))
                else:
                    # Fallback for string ingredients
                    recipe_details.append(Paragraph(f"• {ingredient}", normal_style))
        else:
            recipe_details.append(Paragraph(str(config['baseIngredients']), normal_style))
        recipe_details.append(Spacer(1, 10))
    
    # Base nutritional claims
    if config.get('baseClaims'):
        recipe_details.append(Paragraph("<b>Nutritional Claims:</b>", ParagraphStyle('BoldLabel', parent=normal_style, fontName='Helvetica-Bold')))
        if isinstance(config['baseClaims'], list):
            for claim in config['baseClaims']:
                recipe_details.append(Paragraph(f"• {claim}", normal_style))
        else:
            recipe_details.append(Paragraph(str(config['baseClaims']), normal_style))
        recipe_details.append(Spacer(1, 10))
    
    # Base certifications
    if config.get('baseCertifications'):
        recipe_details.append(Paragraph("<b>Certifications:</b>", ParagraphStyle('BoldLabel', parent=normal_style, fontName='Helvetica-Bold')))
        if isinstance(config['baseCertifications'], list):
            for cert in config['baseCertifications']:
                recipe_details.append(Paragraph(f"• {cert}", normal_style))
        else:
            recipe_details.append(Paragraph(str(config['baseCertifications']), normal_style))
    
    # Current Configuration Card Content
    current_config = []
    current_config.append(Paragraph("Current Configuration", card_header_style))
    
    # Custom ingredients
    if config.get('customIngredients') and config['customIngredients']:
        current_config.append(Paragraph("<b>Additional Ingredients:</b>", ParagraphStyle('BoldLabel', parent=normal_style, fontName='Helvetica-Bold')))
        for ingredient in config['customIngredients']:
            current_config.append(Paragraph(f"• {ingredient}", normal_style))
        current_config.append(Spacer(1, 10))
    
    # Additional nutritional claims
    if config.get('nutritionalClaims') and config['nutritionalClaims']:
        current_config.append(Paragraph("<b>Additional Claims:</b>", ParagraphStyle('BoldLabel', parent=normal_style, fontName='Helvetica-Bold')))
        for claim in config['nutritionalClaims']:
            current_config.append(Paragraph(f"• {claim}", normal_style))
        current_config.append(Spacer(1, 10))
    
    # Additional certifications
    if config.get('certifications') and config['certifications']:
        current_config.append(Paragraph("<b>Additional Certifications:</b>", ParagraphStyle('BoldLabel', parent=normal_style, fontName='Helvetica-Bold')))
        for cert in config['certifications']:
            current_config.append(Paragraph(f"• {cert}", normal_style))
        current_config.append(Spacer(1, 10))
    
    # Packaging
    if config.get('packaging'):
        current_config.append(Paragraph("<b>Packaging:</b>", ParagraphStyle('BoldLabel', parent=normal_style, fontName='Helvetica-Bold')))
        current_config.append(Paragraph(f"• {config['packaging']}", normal_style))
    
    # Create the side-by-side table layout
    # Convert content to strings for table cells
    def flowables_to_html(flowables):
        """Convert flowables to HTML strings for table cells"""
        html_parts = []
        for flowable in flowables:
            if isinstance(flowable, Paragraph):
                html_parts.append(flowable.text)
            elif isinstance(flowable, Spacer):
                html_parts.append("<br/>")
        return "<br/>".join(html_parts)
    
    # Create table with two columns for side-by-side layout
    recipe_html = flowables_to_html(recipe_details)
    config_html = flowables_to_html(current_config)
    
    # Create styled table cells
    recipe_cell = Paragraph(recipe_html, normal_style)
    config_cell = Paragraph(config_html, normal_style)
    
    # Create the two-column table
    cards_table = Table([[recipe_cell, config_cell]], 
                       colWidths=[3.25*inch, 3.25*inch])
    
    # Style the table to look like cards
    cards_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8f9fa')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.HexColor('#f8f9fa')]),
    ]))
    
    story.append(cards_table)
    story.append(Spacer(1, 20))
    
    # Client Information Section
    if concept_session.client_name:
        story.append(Paragraph("Client Information", header_style))
        
        client_data = [
            ['Client Name:', concept_session.client_name or 'Not provided'],
            ['Email:', concept_session.client_email or 'Not provided'],
            ['Date:', concept_session.created_at.strftime('%B %d, %Y') if concept_session.created_at else datetime.now().strftime('%B %d, %Y')],
            ['Session ID:', concept_session.session_id]
        ]
        
        client_table = Table(client_data, colWidths=[1.5*inch, 4*inch])
        client_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ]))
        story.append(client_table)
        story.append(Spacer(1, 20))
    
    # Special Notes
    if config.get('notes') and config['notes']:
        story.append(Paragraph("Special Notes & Requirements", header_style))
        story.append(Paragraph(config['notes'], normal_style))
        story.append(Spacer(1, 20))
    
    # Next Steps Section
    story.append(Paragraph("Next Steps", header_style))
    next_steps = [
        "• Technical feasibility assessment and recipe optimization",
        "• Comprehensive nutritional analysis and validation",
        "• Cost calculation and competitive pricing strategy",
        "• Prototype development and sensory testing",
        "• Regulatory compliance and certification review",
        "• Market launch planning and production scaling"
    ]
    
    for step in next_steps:
        story.append(Paragraph(step, normal_style))
    
    story.append(Spacer(1, 20))
    
    # Contact Information
    story.append(Paragraph("Contact Information", header_style))
    contact_info = """
    <b>H. & J. Brüggen KG</b><br/>
    Innovation Team<br/>
    Am Hafen 27<br/>
    25421 Pinneberg, Germany<br/><br/>
    Email: innovation@bruggen.com<br/>
    Phone: +49 (0)4101 505-0<br/>
    Web: www.bruggen.com
    """
    story.append(Paragraph(contact_info, normal_style))
    
    # Build PDF
    doc.build(story)
    
    return filepath


