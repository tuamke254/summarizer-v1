from sqlalchemy import Column, Integer, String
from app.db.db import db
    
class Transactions(db.Model):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    file_id = Column(String(50))
    file_name = Column(String(50))
    file_timestamp = Column(String(50))
    file_status = Column(String(50))
    
# Add more models as needed