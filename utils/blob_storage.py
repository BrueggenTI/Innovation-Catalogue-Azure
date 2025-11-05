import os
from azure.storage.blob import BlobServiceClient
import logging

# Konfiguration abrufen
AZURE_STORAGE_CONNECTION_STRING = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
AZURE_STORAGE_CONTAINER_NAME = os.environ.get('AZURE_STORAGE_CONTAINER_NAME')

logging.basicConfig(level=logging.INFO)

def get_blob_service_client():
    """Erstellt und gibt einen BlobServiceClient zurück."""
    logging.info("Versuche, den BlobServiceClient zu erstellen.")
    if not AZURE_STORAGE_CONNECTION_STRING:
        logging.error("AZURE_STORAGE_CONNECTION_STRING ist nicht gesetzt!")
        return None

    if not AZURE_STORAGE_CONTAINER_NAME:
        logging.error("AZURE_STORAGE_CONTAINER_NAME ist nicht gesetzt!")
        return None

    logging.info(f"AZURE_STORAGE_CONTAINER_NAME: {AZURE_STORAGE_CONTAINER_NAME}")
    # Zum Debuggen nur einen Teil des Connection Strings anzeigen, niemals den ganzen!
    logging.info(f"AZURE_STORAGE_CONNECTION_STRING (Teil): AccountName={AZURE_STORAGE_CONNECTION_STRING.split('AccountName=')[1].split(';')[0] if 'AccountName=' in AZURE_STORAGE_CONNECTION_STRING else 'Nicht gefunden'}")

    try:
        blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
        logging.info("BlobServiceClient erfolgreich erstellt.")
        return blob_service_client
    except Exception as e:
        logging.error(f"Fehler beim Erstellen des BlobServiceClient: {e}", exc_info=True)
        return None

def upload_file_to_blob(file_stream, file_name, content_type):
    """Lädt einen Dateistream in den Azure Blob Storage hoch."""
    logging.info(f"Versuche, die Datei {file_name} in den Blob Storage hochzuladen.")
    blob_service_client = get_blob_service_client()
    if not blob_service_client:
        logging.error("Upload abgebrochen, da kein BlobServiceClient verfügbar ist.")
        return None

    try:
        blob_client = blob_service_client.get_blob_client(container=AZURE_STORAGE_CONTAINER_NAME, blob=file_name)

        file_stream.seek(0)
        blob_client.upload_blob(file_stream, blob_type="BlockBlob", overwrite=True, content_settings={'contentType': content_type})

        logging.info(f"Datei {file_name} erfolgreich hochgeladen. URL: {blob_client.url}")
        return blob_client.url
    except Exception as e:
        logging.error(f"Fehler beim Hochladen der Datei {file_name}: {e}", exc_info=True)
        return None
