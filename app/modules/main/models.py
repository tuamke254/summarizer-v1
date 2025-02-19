from sqlalchemy import Column, Integer, String
from app.db.db import db

class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(50))

# Add more models as needed