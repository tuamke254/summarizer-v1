import os
import json
from google import genai
from google.genai import types

PROMPTS = os.environ.get("PROMPTS_FILE")
PROJECT = os.environ.get("PROJECT_NAME")
LOCATION = os.environ.get("LOCATION")


class ProcessorController:
    def __init__(self, prompts_file=PROMPTS, project=PROMPTS, location=LOCATION):
        # Load prompts from a JSON file
        with open(prompts_file, 'r') as file:
            self.prompts = json.load(file)
        
        # Initialize the genai client
        self.client = genai.Client(
            vertexai=True,
            project=project,
            location=location,
        )
        
        # Define the model and configuration
        self.model = "gemini-2.0-flash-001"
        self.generate_content_config = types.GenerateContentConfig(
            temperature=0.5,
            top_p=0.5,
            max_output_tokens=256,
            response_modalities=["TEXT"],
            safety_settings=[
                types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="OFF"),
                types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="OFF"),
                types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="OFF"),
                types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="OFF"),
            ],
        )

    # Test Method
    def index(self):
        return {'message': 'Hello, World!'}
    
    def generate_text(self, prompt):
        # Prepare the content for the genai model
        contents = [
            types.Content(
                role="user",
                parts=[types.Part(text=prompt)]
            )
        ]
        
        # Generate content using the genai model
        response = ""
        for chunk in self.client.models.generate_content_stream(
            model=self.model,
            contents=contents,
            config=self.generate_content_config,
        ):
            response += chunk.text
        
        return response
    
    def extract_insights(self, transcript, prompt_key):
        # Retrieve the instruction prompt based on the key
        instructions = self.prompts.get(prompt_key, "")
        if not instructions:
            raise ValueError(f"No prompt found for key: {prompt_key}")
        
        # Combine the instructions and transcript
        prompt = f"{instructions}\n{transcript}"
        return self.generate_text(prompt)
    
    def meeting_minutes(self, transcript):
        # Define the keys for the prompts and corresponding output fields
        tasks = {
            'abstract_summary': 'abstract_summary_extraction',
            'key_points': 'key_points_extraction',
            'keywords': 'keywords_extraction',
            'action_items': 'action_item_extraction',
            'sentiment': 'sentiment_analysis'
        }
        
        # Iterate through the tasks and extract insights
        minutes = {}
        for field, prompt_key in tasks.items():
            minutes[field] = self.extract_insights(transcript, prompt_key)
        
        return minutes
