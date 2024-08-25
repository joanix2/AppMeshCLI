import os
import json
from dotenv import load_dotenv
from openai import OpenAI

def load_tools_from_directory(directory_path):
    """
    Charge tous les fichiers JSON dans le répertoire spécifié et les retourne sous forme de liste d'objets Python.

    :param directory_path: Le chemin du répertoire contenant les fichiers JSON.
    :return: Une liste d'objets Python représentant les outils chargés.
    """
    tools = []

    # Parcourir tous les fichiers dans le répertoire
    for filename in os.listdir(directory_path):
        if filename.endswith('.json'):
            file_path = os.path.join(directory_path, filename)
            with open(file_path, 'r') as json_file:
                try:
                    # Charger le fichier JSON
                    tool = json.load(json_file)
                    tools.append(tool)
                except json.JSONDecodeError:
                    print(f"Erreur lors du chargement du fichier {filename}. Ce fichier n'est pas un JSON valide.")
    
    return tools

def get_completion(client, messages, tools, function_name=None, model="gpt-4o"):
    # Si function_name est fourni, filtrer la liste des outils
    if function_name is not None:
        # Filtrer les outils dont le nom correspond à function_name
        filtered_tools = [
            tool for tool in tools
            if tool.get("function", {}).get("name") == function_name
        ]
        
        # Si aucun outil ne correspond, lever une erreur
        if not filtered_tools:
            raise ValueError(
                f"Le nom de la fonction '{function_name}' n'est pas présent dans la liste des outils."
            )
        
        # Mettre à jour la liste des outils pour ne contenir que l'outil filtré
        tools = filtered_tools
    
    # Créer la complétion en utilisant les outils filtrés ou la liste complète
    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools,
        tool_choice={
            "type": "function",
            "function": {"name": function_name} if function_name else None
        },
    )
    
    return completion

# # Check if the conversation was too long for the context window
# if response['choices'][0]['message']['finish_reason'] == "length":
#     print("Error: The conversation was too long for the context window.")
#     # Handle the error as needed, e.g., by truncating the conversation or asking for clarification
#     handle_length_error(response)
    
# # Check if the model's output included copyright material (or similar)
# if response['choices'][0]['message']['finish_reason'] == "content_filter":
#     print("Error: The content was filtered due to policy violations.")
#     # Handle the error as needed, e.g., by modifying the request or notifying the user
#     handle_content_filter_error(response)
    
# # Check if the model has made a tool_call. This is the case either if the "finish_reason" is "tool_calls" or if the "finish_reason" is "stop" and our API request had forced a function call
# if (response['choices'][0]['message']['finish_reason'] == "tool_calls" or 
#     # This handles the edge case where if we forced the model to call one of our functions, the finish_reason will actually be "stop" instead of "tool_calls"
#     (our_api_request_forced_a_tool_call and response['choices'][0]['message']['finish_reason'] == "stop")):
#     # Handle tool call
#     print("Model made a tool call.")
#     # Your code to handle tool calls
#     handle_tool_call(response)
    
# # Else finish_reason is "stop", in which case the model was just responding directly to the user
# elif response['choices'][0]['message']['finish_reason'] == "stop":
#     # Handle the normal stop case
#     print("Model responded directly to the user.")
#     # Your code to handle normal responses
#     handle_normal_response(response)
    
# # Catch any other case, this is unexpected
# else:
#     print("Unexpected finish_reason:", response['choices'][0]['message']['finish_reason'])
#     # Handle unexpected cases as needed
#     handle_unexpected_case(response)

def main():

    # Load environment variables from the .env file
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    client = OpenAI(api_key=api_key)

    #Load tools
    directory_path = './function'
    messages = [{"role": "user", "content": "This is a CLI project with LLMs"}]
    tools = load_tools_from_directory(directory_path)
    readme = get_completion(client, messages, tools, "get_readme")
    print(readme)

if __name__ == '__main__':
    main()