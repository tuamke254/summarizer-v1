from flask import Blueprint, make_response, jsonify, request
from .controller import TranscriptsController
from app.modules.auth.controller import AuthController
import os


transcripts_bp = Blueprint('transcripts', __name__)
transcripts_controller = TranscriptsController()
auth_controller = AuthController()
@transcripts_bp.route('/', methods=['GET'])
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
    result=transcripts_controller.index()
    return make_response(jsonify(data=result))

@transcripts_bp.route('/new', methods=['GET'])
def get_new_transcript():
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

    credentials = auth_controller.auth()
    if not credentials:
        return make_response(jsonify({'error': 'Authentication failed'}), 401)

    service = auth_controller.build_drive_service(credentials)
    if not service:
        return make_response(jsonify({'error': 'Error building Drive service'}), 500)

    files = transcripts_controller.get_new_transcript(request, service, folder_id)
    if not files:
        return make_response(jsonify({'error': 'Error listing files'}), 500)
    
    transcripts_controller.insert_new_transcript(files)
    return make_response(jsonify(data=files))

@transcripts_bp.route('/pending', methods=['GET'])
def get_pending_transcripts():
    """List pending transcripts.
    ---
    tags:
      - Transcripts
    responses:
      200:
        description: A list of pending transcripts.
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                description: The ID of the transcript.
              file_id:
                type: string
                description: The ID of the file.
              file_name:
                type: string
                description: The name of the file.
              file_timestamp:
                type: string
                description: The timestamp when the file was created.
              file_status:
                type: string
                description: The status of the file.
      500:
        description: Internal Server Error.  An error occurred while processing the request.

    """
    transcripts = transcripts_controller.get_pending_transcript()
    if not transcripts:
        return make_response(jsonify({'error': 'Error listing transcripts'}), 500)
    
    return make_response(jsonify(data=transcripts))
