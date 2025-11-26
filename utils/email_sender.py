
from flask_mail import Message
import logging

def send_concept_email(mail, concept):
    """Send concept email with PDF attachment"""
    try:
        msg = Message(
            subject=f"Your Co-Creation Concept: {concept.client_name}",
            recipients=[concept.client_email],
            body="Thank you for creating a concept with us! Please find your customized product concept attached.",
            sender="innovation@brueggen.com"
        )

        if concept.pdf_path:
            with open(concept.pdf_path, 'rb') as f:
                msg.attach(
                    f'bruggen_concept_{concept.client_name or "draft"}.pdf',
                    'application/pdf',
                    f.read()
                )
        
        mail.send(msg)
        logging.info(f"Email sent successfully to {concept.client_email}")
        return True

    except Exception as e:
        logging.error(f"Error sending email: {str(e)}")
        return False
