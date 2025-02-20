from flask import Blueprint, make_response, jsonify, request
from .controller import MainController
import os
import json


main_bp = Blueprint('main', __name__)
main_controller = MainController()
@main_bp.route('/', methods=['GET'])
def index():
    """ Example endpoint with simple greeting.
    ---
    tags:
      - Example API
    responses:
      200:
        description: A simple greeting
        schema:
          type: object
          properties:
            data:
              type: object
              properties:
                message:
                  type: string
                  example: "Hello World!"
    """
    result=main_controller.index()
    return make_response(jsonify(data=result))

@main_bp.route('/files', methods=['GET'])
def list_files():
    """List files in a Google Drive folder.
    ---
    tags:
      - Google Drive API
    parameters:
      - in: query
        name: folder_id
        type: string
        required: true
        description: The ID of the Google Drive folder.
    responses:
      200:
        description: A list of files in the specified folder.
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: string
                description: The ID of the file.
              name:
                type: string
                description: The name of the file.
      401:
        description: Unauthorized.  Missing or invalid credentials.
      500:
        description: Internal Server Error.  An error occurred while processing the request.

    """
    folder_id = os.environ.get('FOLDER_ID')
    if not folder_id:
        return make_response(jsonify({'error': 'folder_id is required'}), 400)

    credentials = main_controller.auth(request)
    if not credentials:
        return make_response(jsonify({'error': 'Authentication failed'}), 401)

    service = main_controller.build_drive_service(credentials)
    if not service:
        return make_response(jsonify({'error': 'Error building Drive service'}), 500)

    files = main_controller.list_files(request, service, folder_id)
    if not files:
        return make_response(jsonify({'error': 'Error listing files'}), 500)
    
    # return make_response(main_controller.insert_record(files))
    main_controller.insert_record(files)

    json_data = make_response(jsonify({'files': files}))
   
    return json_data


@main_bp.route('/records', methods=['GET'])
def get_record():
    """Get records from the database.
    ---
    tags:
      - Database
    responses:
      200:
        description: A list of records from the database.
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                description: The ID of the record.
              name:
                type: string
                description: The name of the record.
    """
    records = main_controller.get_record('1_HDiirwRmVoSWsj1VIGVQMhhK4HJzUOV')
    return make_response(records)
    # return make_response(jsonify(records))

