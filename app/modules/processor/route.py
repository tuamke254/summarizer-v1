from flask import Blueprint, make_response, jsonify, request
from .controller import ProcessorController
from auth.controller import AuthController
from transcripts.controller import TranscriptsController


processor_bp = Blueprint('processor', __name__)
processor_controller = ProcessorController()
auth_controller = AuthController()
transcripts_controller = TranscriptsController()

@processor_bp.route('/', methods=['GET'])
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
    result=processor_controller.index()
    return make_response(jsonify(data=result))

@processor_bp.route('/summary', methods=['POST'])
def summary():
    credentials = auth_controller.auth()
    if not credentials:
        return make_response(jsonify(data='Unauthorized'), 401)
    
    service = auth_controller.build_drive_service(credentials)
    if not service:
        return make_response(jsonify(data='Unauthorized'), 401)
    
    transcripts = transcripts_controller.get_content(service)
    if not transcripts:
        return make_response(jsonify(data='No new transcripts'), 200)
    response = {}
    for transcript in transcripts:
       response = processor_controller.meeting_minutes(transcript)
       response.append(response)
    return make_response(jsonify(response))
