import openai
import json
from enum import Enum

# Remplacez 'your-api-key' par votre clé API OpenAI
openai.api_key = 'your-api-key'



class ResponseFormat(Enum):
    JSON_OBJECT = "json_object"
    TEXT = "text"
    HTML = "html"
    MARKDOWN = "markdown"

class GPTCompletion:
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = self.api_key

    def get_completion(self, prompt, format: ResponseFormat):
        # Prépare le format de la réponse
        response_format = format.value

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            # Le format de la réponse est inclus dans les paramètres de l'API
            response_format=response_format
        )

        # Supposons que le modèle renvoie une réponse en fonction du format spécifié
        completion = response.choices[0].message['content']
        
        # Si le format est JSON, essayez de le charger en tant qu'objet Python
        if format == ResponseFormat.JSON_OBJECT:
            try:
                params = json.loads(completion)
                return params
            except json.JSONDecodeError:
                print("Erreur : La réponse n'est pas un JSON valide.")
                return None
        else:
            return completion

# Exemple d'utilisation de l'objet et de l'énumération

gpt = GPTCompletion(api_key="your-api-key")

# Pour obtenir un JSON en réponse
prompt = "Please provide a JSON object with user details."
params = gpt.get_completion(prompt, format=ResponseFormat.JSON_OBJECT)
print(params)

# Pour obtenir une réponse en texte brut
text_response = gpt.get_completion("What is the capital of France?", format=ResponseFormat.TEXT)
print(text_response)
