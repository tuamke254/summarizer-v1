from flask import current_app as app
from app.modules.main.lib import create_and_populate_table

class MainController:
    def index(self):
        return {'message': 'Hello, World!'}

    def create_table(self):
        create_and_populate_table()
        return {'message': 'Table created and populated with random data'}