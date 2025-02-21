from flask import Blueprint, make_response, jsonify, request
from .controller import ProcessorController
from auth.controller import AuthController
from transcripts.controller import TranscriptsController

# Initialize the controllers
processor_controller = ProcessorController()
auth_controller = AuthController()
transcripts_controller = TranscriptsController()

# Initialize the Blueprint for the processor module
processor_bp = Blueprint('processor', __name__)

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
def generate_summary():
  """ Generate a summary of the transcripts.
  ---
  tags:
    - Summary API
  requestBody:
    description: Request to generate summary
    required: true
    content:
    application/json:
      schema:
      type: object
      properties:
        auth_token:
        type: string
        description: Authentication token
        example: "your_auth_token"
  responses:
    200:
    description: Summary generated successfully
    content:
      application/json:
      schema:
        type: object
        properties:
        summary:
          type: array
          items:
          type: object
          properties:
            meeting_minutes:
            type: string
            example: "Meeting minutes summary"
    401:
    description: Unauthorized access
    content:
      application/json:
      schema:
        type: object
        properties:
        data:
          type: string
          example: "Unauthorized"
    200:
    description: No new transcripts
    content:
      application/json:
      schema:
        type: object
        properties:
        data:
          type: string
          example: "No new transcripts"
  """
  credentials = auth_controller.auth()
  if not credentials:
    return make_response(jsonify(data='Unauthorized'), 401)
  
  service = auth_controller.build_drive_service(credentials)
  if not service:
    return make_response(jsonify(data='Unauthorized'), 401)
  
  transcripts = transcripts_controller.get_content_transcript(service)
  if not transcripts:
    return make_response(jsonify(data='No new transcripts'), 200)
  
  response = []
  for transcript in transcripts:
    summary = processor_controller.meeting_minutes(transcript)
    response.append(summary)
  
  return make_response(jsonify(summary=response))
