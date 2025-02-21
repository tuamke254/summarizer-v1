import vertexai
from vertexai.language_models import TextGenerationModel
from google.api_core.client_options import ClientOptions
import json
import os


# Initialize the PALM model
vertexai.init(project=os.environ.get('PROJECT_ID'), location=os.environ.get('REGION'))
palm_model = TextGenerationModel.from_pretrained("text-bison@001")
palm_parameters = {
    "temperature": 0.5,
    "max_output_tokens": 256,
    "top_k": 3,
    "top_p": 0.5
}

class ProcessorController:
    def __init__(self, prompts_file='prompts.json'):
        # Load prompts from a JSON file
        with open(prompts_file, 'r') as file:
            self.prompts = json.load(file)
    
    def index(self):
        return {'message': 'Hello, World!'}
    
    def generate_text(self, prompt):
        summary = palm_model.predict(prompt, **palm_parameters)
        return summary.text
    
    def extract_insights(self, transcript, prompt_key):
        # Retrieve the instruction prompt based on the key
        instructions = self.prompts.get(prompt_key, "")
        if not instructions:
            raise ValueError(f"No prompt found for key: {prompt_key}")
        return self.generate_text(f"{instructions}\n{transcript}")
    
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