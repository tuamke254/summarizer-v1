import os
import json
from google import genai
from google.genai import types

# set the environment variables
PROMPTS = os.environ.get("PROMPTS_FILE")
PROJECT = os.environ.get("PROJECT_NAME")
LOCATION = os.environ.get("LOCATION")


class ProcessorController:
    def __init__(self, prompts_file=PROMPTS, project=PROJECT, location=LOCATION):
        """
        Initializes the ProcessorController with the specified configuration.
        Args:
            prompts_file (str): Path to the JSON file containing prompts. Defaults to PROMPTS.
            project (str): The project identifier. Defaults to PROJECT.
            location (str): The location identifier. Defaults to LOCATION.
        Attributes:
            prompts (dict): Loaded prompts from the JSON file.
            client (genai.Client): Initialized genai client.
            model (str): The model identifier.
            generate_content_config (types.GenerateContentConfig): Configuration for content generation.
        """
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

    # API Endpoint Test Method
    def index(self):
        return {'message': 'Hello, World!'}
    
    def generate_text(self, prompt):
        """
        Generates text based on the provided prompt using a generative AI model.
        Args:
            prompt (str): The input text prompt to generate content from.
        Returns:
            str: The generated text response from the AI model.
        """
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
        """
        Extracts insights from a given transcript using a specified prompt key.
        This method retrieves the instructions associated with the provided prompt key,
        combines them with the transcript, and generates text based on the combined prompt.
        Args:
            transcript (str): The transcript from which insights are to be extracted.
            prompt_key (str): The key used to retrieve the corresponding instructions.
        Returns:
            str: The generated text based on the combined instructions and transcript.
        Raises:
            ValueError: If no instructions are found for the given prompt key.
        """      
        instructions = self.prompts.get(prompt_key, "")
        if not instructions:
            raise ValueError(f"No prompt found for key: {prompt_key}")
        
        # Combine the instructions and transcript
        prompt = f"{instructions}\n{transcript}"
        return self.generate_text(prompt)
    
    def meeting_minutes(self, transcript):
        """
        Generate meeting minutes from a given transcript.
        This method processes a transcript to extract various insights such as 
        abstract summary, key points, keywords, action items, and sentiment analysis.
        Args:
            transcript (str): The transcript of the meeting to be processed.
        Returns:
            dict: A dictionary containing the extracted insights with the following keys:
                - 'abstract_summary': Summary of the meeting.
                - 'key_points': Key points discussed in the meeting.
                - 'keywords': Important keywords from the meeting.
                - 'action_items': Action items identified during the meeting.
                - 'sentiment': Sentiment analysis of the meeting.
        """
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
