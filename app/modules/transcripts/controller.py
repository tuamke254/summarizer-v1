import logging
from app.db.db import db
from app.db.models import Transactions


class TranscriptsController:
    def index(self):
        return {'message':'Hello, World!'}
    
    def get_new_transcript(self, request, service, folder_id):
        """
        List new transcripts in a Google Drive folder and compare against transaction records.

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
        
    def insert_new_transcript(self, files):
        """
        Inserts new transcript records into the database.

        Args:
            files (list): A list of dictionaries, where each dictionary contains
                          the keys 'id', 'name', and 'createdTime' representing
                          the file's ID, name, and creation timestamp respectively.

        Returns:
            bool: True if the records were inserted successfully, False otherwise.

        Raises:
            Exception: Logs any exception that occurs during the database transaction
                       and rolls back the session.
        """
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
        
    def get_pending_transcript(self):
        """
        Retrieves the first pending transcript record from the Transactions table.

        This method queries the Transactions table for the first record with a 
        'Pending' file_status. If such a record is found, it returns a dictionary 
        containing the file_id, file_name, file_timestamp, and file_status of the 
        record. If no pending records are found, it logs an informational message 
        and returns None. In case of an exception during the query, it logs an 
        error message and returns None.

        Returns:
            dict: A dictionary containing the file_id, file_name, file_timestamp, 
                  and file_status of the pending record if found.
            None: If no pending records are found or an error occurs during the query.
        """
        try:
            record = Transactions.query.filter_by(file_status='Pending').first()
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

    def get_content_transcript(self, service):
        """
        Retrieve content transcripts from a service for transactions with a 'Pending' file status.

        This method queries the Transactions table for records with a 'Pending' file status.
        For each pending transaction, it retrieves the corresponding file content from the provided service
        and compiles a list of transcripts.

        Args:
            service: An authenticated service object that provides access to the file content.

        Returns:
            list: A list of transcripts if there are pending transactions, otherwise None.

        Raises:
            Exception: If there is an error retrieving the transcripts, it logs the error and returns None.
        """
        try:
            record = Transactions.query.filter_by(file_status='Pending').first()
            if record:
                transcripts = []
                for record in Transactions.query.filter_by(file_status='Pending').all():
                    file_id = record.file_id
                    request = service.files().get_media(fileId=file_id)
                    transcript = request.execute()
                    transcripts.append(transcript)
                return transcripts
            else:
                logging.info("No pending transcripts found.")
                return None
        except Exception as e:
            logging.error(f"Error retrieving transcripts: {e}")
            return None    