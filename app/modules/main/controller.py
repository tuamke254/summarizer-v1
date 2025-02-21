from flask import current_app as app
from google.cloud import secretmanager
from google.oauth2 import service_account
from googleapiclient.discovery import build
from app.modules.main.models import Transactions
from app.db.db import db
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
        List files in a specified Google Drive folder and compare against transaction records.

        Args:
            service: Authorized Google Drive service instance.
            folder_id: ID of the folder to list files from.

        Returns:
            List of new files in the specified folder.
        """
        try:
            query = f"'{folder_id}' in parents"
            results = service.files().list(
                q=query, pageSize=10, fields="nextPageToken, files(id, name, createdTime)").execute()
            items = results.get('files', [])
            
            new_files = []
            for item in items:
                if not Transactions.query.filter_by(file_id=item['id']).first():
                    new_files.append(item)
            
            if not new_files:
                logging.info("No new files in the drive")
                return None
            
            return new_files
        except Exception as e:
            logging.error(f"Error listing files: {e}")
            return None
    
    def insert_record(self, files):
        try:
            for file in files:
                transaction = Transactions(
                    file_id=file.get('id'),
                    file_name=file.get('name'),
                    file_timestamp=file.get('createdTime'),
                    file_status='Pending'
                )
                db.session.add(transaction)
            db.session.commit()
            logging.info("Record inserted successfully")
            return True
        except Exception as e:
            logging.error(f"Error inserting record: {e}")
            db.session.rollback()
            return False
        
    def get_record(self, file_id):
        try:
            record = Transactions.query.filter_by(file_id=file_id, file_status='Pending').first()
            if record:
                return {
                    'file_id': record.file_id,
                    'file_name': record.file_name,
                    'file_timestamp': record.file_timestamp,
                    'file_status': record.file_status
                }
            else:
                logging.info("No unprocessed files found")
                return None
        except Exception as e:
            logging.error(f"Error retrieving record: {e}")
            return None

