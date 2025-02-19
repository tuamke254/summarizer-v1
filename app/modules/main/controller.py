from flask import current_app as app
from google.cloud import secretmanager
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
import json
import logging

logging.basicConfig(level=logging.ERROR)

class MainController:
    def index(self):
        return {'message': 'Hello, World!'}
    
    def auth(self, request):
        try:
            # Retrieve the GCP service account key from Google Secret Manager
            client = secretmanager.SecretManagerServiceClient()
            name = f"projects/{os.environ.get('PROJECT_ID')}/secrets/{os.environ.get('SECRET_NAME')}/versions/latest"
            response = client.access_secret_version(name=name)
            payload = response.payload.data.decode('UTF-8')
            credentials = service_account.Credentials.from_service_account_info(json.loads(payload))

            return credentials

        except Exception as e:
            logging.error(f"Authentication failed: {e}")
            return None

   
    def build_drive_service(self, credentials):
        try:
            service = build('drive', 'v3', credentials=credentials)
            return service
        except Exception as e:
            logging.error(f"Error building Drive service: {e}")
            return None
    
    def list_files(self, request, service, folder_id):
        """
        List files in a specified Google Drive folder.

        Args:
            service: Authorized Google Drive service instance.
            folder_id: ID of the folder to list files from.

        Returns:
            List of files in the specified folder.
        """
        try:
            query = f"'{folder_id}' in parents"
            results = service.files().list(
                q=query, pageSize=10, fields="nextPageToken, files(id, name, mimeType, createdTime)").execute()
            items = results.get('files', [])
            return items
        except Exception as e:
            print(f"Error listing files: {e}")
            return None
        except Exception as e:
            logging.error(f"Error listing files: {e}")
            return None
    