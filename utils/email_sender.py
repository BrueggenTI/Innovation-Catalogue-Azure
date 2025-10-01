from flask_mail import Message
from app import mail
import logging
import os

def send_concept_email(concept_session):
    """Send concept PDF via email to client"""
    
    try:
        msg = Message(
            subject="Your Brüggen Innovation Concept Summary",
            recipients=[concept_session.client_email],
            sender=os.environ.get('MAIL_DEFAULT_SENDER', 'innovation@bruggen.com')
        )
        
        # Email body
        msg.body = f"""
Dear {concept_session.client_name or 'Valued Partner'},

Thank you for your interest in collaborating with H. & J. Brüggen KG on innovative breakfast solutions.

Please find attached your personalized concept summary from our co-creation session. This document outlines the product specifications we discussed and the next steps in bringing your vision to life.

Our innovation team is excited about the potential of this concept and looks forward to working with you to develop a market-leading product that meets your specific requirements.

Next Steps:
- Our technical team will conduct a feasibility assessment
- We'll provide detailed nutritional analysis and cost calculations
- Prototype development will begin upon approval
- Regulatory compliance review will be completed

We will be in touch within 2-3 business days with additional details and timeline estimates.

Thank you for choosing Brüggen as your innovation partner.

Best regards,
The Brüggen Innovation Team

---
H. & J. Brüggen KG
Innovation Department
Email: innovation@bruggen.com
Phone: +49 (0)4321 505-0
Website: www.bruggen.com
        """
        
        msg.html = f"""
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <div style="text-align: center; margin-bottom: 30px;">
            <h1 style="color: #2c5234; margin-bottom: 10px;">H. & J. Brüggen KG</h1>
            <h2 style="color: #666; font-weight: normal;">Innovation Concept Summary</h2>
        </div>
        
        <p>Dear {concept_session.client_name or 'Valued Partner'},</p>
        
        <p>Thank you for your interest in collaborating with H. & J. Brüggen KG on innovative breakfast solutions.</p>
        
        <p>Please find attached your personalized concept summary from our co-creation session. This document outlines the product specifications we discussed and the next steps in bringing your vision to life.</p>
        
        <p>Our innovation team is excited about the potential of this concept and looks forward to working with you to develop a market-leading product that meets your specific requirements.</p>
        
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
            <h3 style="color: #2c5234; margin-top: 0;">Next Steps:</h3>
            <ul style="margin-bottom: 0;">
                <li>Our technical team will conduct a feasibility assessment</li>
                <li>We'll provide detailed nutritional analysis and cost calculations</li>
                <li>Prototype development will begin upon approval</li>
                <li>Regulatory compliance review will be completed</li>
            </ul>
        </div>
        
        <p>We will be in touch within <strong>2-3 business days</strong> with additional details and timeline estimates.</p>
        
        <p>Thank you for choosing Brüggen as your innovation partner.</p>
        
        <p>Best regards,<br>
        <strong>The Brüggen Innovation Team</strong></p>
        
        <hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">
        
        <div style="color: #666; font-size: 14px;">
            <strong>H. & J. Brüggen KG</strong><br>
            Innovation Department<br>
            Email: <a href="mailto:innovation@bruggen.com">innovation@bruggen.com</a><br>
            Phone: +49 (0)4321 505-0<br>
            Website: <a href="http://www.bruggen.com">www.bruggen.com</a>
        </div>
    </div>
</body>
</html>
        """
        
        # Attach PDF if it exists
        if concept_session.pdf_path and os.path.exists(concept_session.pdf_path):
            with open(concept_session.pdf_path, 'rb') as fp:
                msg.attach(
                    filename=f"bruggen_concept_{concept_session.client_name or 'summary'}.pdf",
                    content_type="application/pdf",
                    data=fp.read()
                )
        
        mail.send(msg)
        logging.info(f"Email sent successfully to {concept_session.client_email}")
        return True
        
    except Exception as e:
        logging.error(f"Failed to send email: {str(e)}")
        return False
