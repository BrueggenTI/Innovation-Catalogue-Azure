import os
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import logging

# Konfiguration abrufen
AZURE_STORAGE_CONNECTION_STRING = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
AZURE_STORAGE_CONTAINER_NAME = os.environ.get('AZURE_STORAGE_CONTAINER_NAME')

def get_blob_service_client():
    """Erstellt und gibt einen BlobServiceClient zurück."""
    if not AZURE_STORAGE_CONNECTION_STRING:
        logging.error("Azure Storage Connection String ist nicht konfiguriert.")
        return None
    try:
        blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
        return blob_service_client
    except Exception as e:
        logging.error(f"Fehler beim Erstellen des BlobServiceClient: {e}")
        return None

def upload_file_to_blob(file_stream, file_name, content_type):
    """Lädt einen Dateistream in den Azure Blob Storage hoch."""
    blob_service_client = get_blob_service_client()
    if not blob_service_client or not AZURE_STORAGE_CONTAINER_NAME:
        return None

    try:
        blob_client = blob_service_client.get_blob_client(container=AZURE_STORAGE_CONTAINER_NAME, blob=file_name)

        file_stream.seek(0) # Zurück zum Anfang des Streams
        blob_client.upload_blob(file_stream, blob_type="BlockBlob", overwrite=True, content_settings={'contentType': content_type})

        logging.info(f"Datei {file_name} erfolgreich in den Container {AZURE_STORAGE_CONTAINER_NAME} hochgeladen.")
        return blob_client.url
    except Exception as e:
        logging.error(f"Fehler beim Hochladen der Datei {file_name} in den Blob Storage: {e}")
        return None
