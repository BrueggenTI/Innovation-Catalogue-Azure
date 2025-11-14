import os
import re
from azure.storage.blob import BlobServiceClient, ContentSettings
import logging

# Konfiguration abrufen
AZURE_STORAGE_CONNECTION_STRING = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
AZURE_STORAGE_CONTAINER_NAME = os.environ.get('AZURE_STORAGE_CONTAINER_NAME')

logging.basicConfig(level=logging.INFO)

def get_blob_service_client():
    """Erstellt und gibt einen BlobServiceClient zurück."""
    if not AZURE_STORAGE_CONNECTION_STRING or not AZURE_STORAGE_CONTAINER_NAME:
        logging.error("Azure Storage Konfiguration (Connection String oder Container Name) ist nicht gesetzt.")
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
    if not blob_service_client:
        return None

    # ==> DIAGNOSTIC LOGGING START
    logging.info(f"Attempting to upload '{file_name}' with received content_type: '{content_type}'")
    # ==> DIAGNOSTIC LOGGING END

    try:
        blob_client = blob_service_client.get_blob_client(container=AZURE_STORAGE_CONTAINER_NAME, blob=file_name)

        file_stream.seek(0)
        blob_client.upload_blob(file_stream, blob_type="BlockBlob", overwrite=True)

        # Explizit den Content-Type nach dem Upload setzen
        blob_client.set_http_headers(content_settings=ContentSettings(content_type=content_type))

        logging.info(f"Datei {file_name} erfolgreich in Azure Blob Storage hochgeladen.")
        return blob_client.url
    except Exception as e:
        logging.error(f"Fehler beim Hochladen der Datei {file_name} nach Azure Blob Storage: {e}")
        return None

def get_blob_url_if_exists(file_name):
    """Überprüft, ob ein Blob existiert und gibt dessen URL zurück."""
    blob_service_client = get_blob_service_client()
    if not blob_service_client:
        return None

    try:
        blob_client = blob_service_client.get_blob_client(container=AZURE_STORAGE_CONTAINER_NAME, blob=file_name)
        if blob_client.exists():
            logging.info(f"Blob {file_name} existiert und wird verwendet.")
            return blob_client.url
        else:
            logging.info(f"Blob {file_name} existiert nicht.")
            return None
    except Exception as e:
        logging.error(f"Fehler beim Überprüfen des Blobs {file_name}: {e}")
        return None

def find_latest_image_for_recipe(spec_num):
    """
    Finds the most recently updated image for a given recipe specification number.
    Searches for blobs containing the spec_num as a whole word, ending in .png or .jpg.
    """
    blob_service_client = get_blob_service_client()
    if not blob_service_client:
        return None, None

    try:
        container_client = blob_service_client.get_container_client(AZURE_STORAGE_CONTAINER_NAME)
        blobs = container_client.list_blobs()

        candidate_blobs = []
        # Regex to find the spec_num as a whole word, case-insensitive for extensions
        pattern = re.compile(r".*\b" + re.escape(spec_num) + r"\b.*\.(png|jpg)$", re.IGNORECASE)

        for blob in blobs:
            if pattern.match(blob.name):
                candidate_blobs.append(blob)

        if not candidate_blobs:
            logging.info(f"Kein passendes Bild für Rezeptnummer {spec_num} gefunden.")
            return None, None

        # Sort blobs by last_modified timestamp in descending order and pick the newest
        latest_blob = sorted(candidate_blobs, key=lambda b: b.last_modified, reverse=True)[0]

        blob_client = container_client.get_blob_client(latest_blob.name)
        logging.info(f"Neuestes passendes Bild für Rezeptnummer {spec_num} gefunden: {latest_blob.name}")

        return blob_client.url, latest_blob.name

    except Exception as e:
        logging.error(f"Fehler bei der Suche nach dem neuesten Bild für Rezeptnummer {spec_num}: {e}")
        return None, None
