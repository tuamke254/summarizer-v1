from google.cloud import secretmanager
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import logging
import os

logging.basicConfig(level=logging.ERROR)

class AuthController:
    def index(self):
        return {'message':'Hello, World!'}
    
    def auth(self, request):
        """
        Authenticates the request using Google Cloud Platform (GCP) service account credentials.

        This method retrieves the GCP service account key from Google Secret Manager, decodes it,
        and generates credentials from the service account information.

        Args:
            request: The incoming request object.

        Returns:
            google.auth.credentials.Credentials: The GCP service account credentials if authentication is successful.
            None: If authentication fails.

        Raises:
            Exception: If there is an error during the authentication process.
        """
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
        """
        Builds and returns a Google Drive service instance using the provided credentials.

        Args:
            credentials (google.auth.credentials.Credentials): The OAuth 2.0 credentials to authorize the API requests.

        Returns:
            googleapiclient.discovery.Resource: A resource object with methods for interacting with the service.
            None: If an error occurs while building the service.

        Raises:
            Exception: If an error occurs during the service creation, it is logged and None is returned.
        """
        try:
            service = build('drive', 'v3', credentials=credentials)
            return service
        except Exception as e:
            logging.error(f"Error building Drive service: {e}")
            return None
