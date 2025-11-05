import os
import logging
from app import app, db
from models import Product
from utils.blob_storage import upload_file_to_blob
from sqlalchemy import or_

logging.basicConfig(level=logging.INFO)

def migrate_images():
    """
    Migriert lokale Bilder aus static/images/recipes und static/uploads/products
    in den Azure Blob Storage und aktualisiert die Datenbank.
    """
    with app.app_context():
        # Produkte finden, die lokale Bild-URLs haben
        products_to_migrate = Product.query.filter(
            or_(
                Product.image_url.like('/static/images/recipes/%'),
                Product.image_url.like('/static/uploads/products/%')
            )
        ).all()

        logging.info(f"{len(products_to_migrate)} Produkte mit lokalen Bildern gefunden, die migriert werden müssen.")

        for product in products_to_migrate:
            local_path = product.image_url.lstrip('/')

            if not os.path.exists(local_path):
                logging.warning(f"Bild für Produkt {product.id} unter {local_path} nicht gefunden. Wird übersprungen.")
                continue

            file_name = os.path.basename(local_path)

            try:
                with open(local_path, 'rb') as file_stream:
                    # Bestimmen des Content-Typs basierend auf der Dateiendung
                    content_type = 'image/jpeg'
                    if file_name.lower().endswith('.png'):
                        content_type = 'image/png'
                    elif file_name.lower().endswith('.gif'):
                        content_type = 'image/gif'
                    elif file_name.lower().endswith('.webp'):
                        content_type = 'image/webp'

                    # Hochladen in den Blob Storage
                    blob_url = upload_file_to_blob(file_stream, file_name, content_type)

                    if blob_url:
                        logging.info(f"Bild {file_name} für Produkt {product.id} erfolgreich hochgeladen nach {blob_url}")
                        product.image_url = blob_url
                        db.session.commit()
                    else:
                        logging.error(f"Fehler beim Hochladen von {file_name} für Produkt {product.id}.")
            except Exception as e:
                logging.error(f"Ein Fehler ist beim Verarbeiten von {local_path} für Produkt {product.id} aufgetreten: {e}")
                db.session.rollback()

        logging.info("Migration der Bilder abgeschlossen.")

if __name__ == '__main__':
    # Bevor das Skript ausgeführt wird, stellen Sie sicher, dass die Umgebungsvariablen
    # AZURE_STORAGE_CONNECTION_STRING und AZURE_STORAGE_CONTAINER_NAME gesetzt sind.

    confirmation = input("Möchten Sie wirklich alle lokalen Bilder in den Azure Blob Storage migrieren? (ja/nein): ")
    if confirmation.lower() == 'ja':
        migrate_images()
    else:
        print("Migration abgebrochen.")
