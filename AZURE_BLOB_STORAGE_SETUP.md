# Azure Blob Storage Setup Guide

To enable image uploads to Azure Blob Storage, the following environment variables must be configured in your application's environment.

## Required Environment Variables

### 1. `AZURE_STORAGE_CONNECTION_STRING`

This is the connection string that allows the application to securely connect to your Azure Storage Account.

**How to find it:**

1.  Navigate to your Storage Account in the Azure Portal.
2.  In the left-hand menu, under **Security + networking**, select **Access keys**.
3.  You will see two keys (key1 and key2). Click the **Show** button for one of them.
4.  Copy the full **Connection string** value.

### 2. `AZURE_STORAGE_CONTAINER_NAME`

This is the name of the container within your Storage Account where the images will be stored. You should have already created this container.

**Example:** `recipe-images`

## How to Set the Variables

In your Azure App Service or deployment environment, add these two variables to the application settings or configuration.

**Example (for local testing in a bash shell):**

```bash
export AZURE_STORAGE_CONNECTION_STRING="DefaultEndpointsProtocol=https..."
export AZURE_STORAGE_CONTAINER_NAME="your-container-name"
```

After setting these variables, the application will automatically use Azure Blob Storage for all new image uploads.

## Migrating Existing Images

Once the environment variables are set, you can run the provided migration script to move all existing local images to your new Blob Storage container.

Run the following command from your shell:

```bash
python migrate_images_to_blob.py
```

The script will prompt you for confirmation before starting the migration. This only needs to be done once.
