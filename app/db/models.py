from sqlalchemy import Column, Integer, String
from app.db.db import db
    
class Transactions(db.Model):
    """
    Represents a transaction record in the database.

    Attributes:
        id (int): The primary key of the transaction.
        file_id (str): The unique identifier of the file.
        file_name (str): The name of the file.
        file_timestamp (str): The timestamp when the file was created or modified.
        file_status (str): The status of the file.
    """
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    file_id = Column(String(50))
    file_name = Column(String(50))
    file_timestamp = Column(String(50))
    file_status = Column(String(50))

# Add more models as needed