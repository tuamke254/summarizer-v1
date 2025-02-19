from flask import current_app as app
from app.db.db import db
from app.modules.main.models import User
from faker import Faker
from google.cloud import secretmanager
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
import json


fake = Faker()

class DBFunctions:
    def create_and_populate_table():
        with app.app_context():
            db.create_all()
            
            for _ in range(10):  # Generate 10 random users
                user = User(name=fake.name(), email=fake.email())
                db.session.add(user)
            
            db.session.commit()


class Authentication:
    def authenticate(self, request):
        try:
            # Retrieve the GCP service account key from Google Secret Manager
            client = secretmanager.SecretManagerServiceClient()
            name = f"projects/{os.environ.get('PROJECT_ID')}/secrets/{os.environ.get('SECRET_NAME')}/versions/latest"
            response = client.access_secret_version(name=name)
            payload = response.payload.data.decode('UTF-8')
            credentials = service_account.Credentials.from_service_account_info(json.loads(payload))

            return credentials

        except Exception as e:
            print(f"Authentication failed: {e}")
            return None
