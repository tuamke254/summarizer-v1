import vertexai
from vertexai.language_models import TextGenerationModel
from google.api_core.client_options import ClientOptions

vertexai.init(project="PROJECT_ID", location="REGION")
palm_model = TextGenerationModel.from_pretrained("text-bison@001")
palm_parameters = {
    "temperature": 0.5,
    "max_output_tokens": 256,
    "top_k": 3,
    "top_p": 0.5
}

class ProcessorController:
    def index(self):
        return {'message':'Hello, World!'}
    
    def generate_text(self, prompt):
        summary = palm_model.predict(prompt, **palm_parameters)
        return summary.text
    
    def abstract_summary_extraction(self, transcript):
        instructions = "You are a highly skilled AI trained in language comprehension and summarization. I would like you to read the following text and summarize it into a concise abstract paragraph. Aim to retain the most important points, providing a coherent and readable summary that could help a person understand the main points of the discussion without needing to read the entire text. Please avoid unnecessary details or tangential points."
        return self.generate_text(f"{instructions}\n{transcript}")
    
    def key_points_extraction(self, transcript):
        instructions = "You are a proficient AI with a specialty in distilling information into key points. Based on the following text, identify and list the main points that were discussed or brought up. These should be the most important ideas, findings, or topics that are crucial to the essence of the discussion. Your goal is to provide a list that someone could read to quickly understand what was talked about."
        return self.generate_text(f"{instructions}\n{transcript}")
    
    def keywords_extraction(self, transcript):
        instructions = "You are an AI expert in analyzing conversations and extracting keywords. You will be provided with a block of text, and your task is to extract a list of most important keywords from it. Please list the top 10 keywords and use a comma to separate the keywords in the output. "
        return self.generate_text(f"{instructions}\n{transcript}")
    
    def action_item_extraction(self, transcript):
        instructions = "You are an AI expert in analyzing conversations and extracting action items. Please review the text and identify any tasks, assignments, or actions that were agreed upon or mentioned as needing to be done. These could be tasks assigned to specific individuals, or general actions that the group has decided to take. Please list these action items clearly and concisely."
        return self.generate_text(f"{instructions}\n{transcript}")
    
    def sentiment_analysis(self, transcript):
        instructions = "As an AI with expertise in language and emotion analysis, your task is to analyze the sentiment of the following text. Please consider the overall tone of the discussion, the emotion conveyed by the language used, and the context in which words and phrases are used. Indicate whether the sentiment is generally positive, neutral, or negative, and provide brief explanations for your analysis where possible."
        return self.generate_text(f"{instructions}\n{transcript}")
    
    def meeting_minutes(self, transcript):
        abstract_summary = self.abstract_summary_extraction(transcript)
        key_points = self.key_points_extraction(transcript)
        action_items = self.action_item_extraction(transcript)
        keywords = self.keywords_extraction(transcript)
        sentiment = self.sentiment_analysis(transcript)
        return {
            'abstract_summary': abstract_summary,
            'key_points': key_points,
            'keywords': keywords,
            'action_items': action_items,
            'sentiment': sentiment
        }
