# from function_calling.complet import get_completion, load_tools_from_directory
# from function_calling.schema2template import complete_template_from_json


# def create_readme(client, directory_path = ""):
#     tools = load_tools_from_directory(directory_path)
#     readme = get_completion(client, messages, tools, "get_readme")
#     # Exemple d'utilisation
#     complete_template_from_json(
#         schema_json_path='schema.json',
#         template_path='README_template.jinja2',
#         output_path='README.md'
#     )

import argparse
from datetime import datetime
import json
import os
from bson import ObjectId
from dotenv import load_dotenv
from openai import OpenAI
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import DuplicateKeyError
from jinja2 import Template
from complet import get_completion
import hashlib

def convert_to_serializable(obj):
    if isinstance(obj, ObjectId):
        return f"ObjectId({str(obj)})"
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

def remove_object_ids(data):
    if isinstance(data, dict):
        # Crée une nouvelle dictée en filtrant les clés '_id'
        return {key: remove_object_ids(value) for key, value in data.items() if not isinstance(value, ObjectId)}
    elif isinstance(data, list):
        # Applique récursivement la fonction sur chaque élément de la liste
        return [remove_object_ids(item) for item in data]
    else:
        # Retourne les valeurs de base telles quelles
        return data
    
def format_response(response):
    tool_call = response.choices[0].message.tool_calls[0]
    message = response.choices[0].message.content
    result = {
        "id": tool_call.id,
    }
    if message : result["message"] = message
    if tool_call.function : result["function"] = {
        "arguments": json.loads(tool_call.function.arguments),
        "name": tool_call.function.name
    }
        
    return result

def init_mongo(uri, server_api_index='1'):
    # Crée un nouveau client et se connecte au serveur
    client = MongoClient(uri, server_api=ServerApi(server_api_index))

    # Vérifie la connexion en envoyant une commande 'ping'
    try:
        client.admin.command('ping')
        print("You successfully connected to MongoDB!")
        return client
    except Exception as e:
        print(e)
        exit(1)  # Quitte le programme en cas d'erreur

# interpéréter le text de la CLI
def parse_arguments():
    parser = argparse.ArgumentParser(description="A CLI tool for executing commands with options.")
    
    # Argument pour la commande
    parser.add_argument('command', type=str, help="The command to execute.")
    
    # Capture tous les autres arguments après la commande
    parser.add_argument('options', nargs=argparse.REMAINDER, help="Options in the form -option value or --option value.")

    args = parser.parse_args()

    # Créer un dictionnaire pour stocker les options
    options = {}
    current_option = None

    # Parcourir la liste des options
    for item in args.options:
        if item.startswith('-'):  # Détection des options
            current_option = item.lstrip('-')  # Enlever les tirets
            options[current_option] = None  # Placeholder pour la valeur
        elif current_option:
            options[current_option] = item  # Assigner la valeur à l'option
            current_option = None

    return args.command, options

def show_command(command, options):
    print(f"Executing command: {command}")
    print("With options:")
    for key, value in options.items():
        print(f"  - {key}: {value}")

# Fonction pour vérifier si une commande existe dans la collection 'tasks'
def find_task_by_command(db, command_name):
    tasks_collection = db['tasks']  # Collection 'tasks'

    # Recherche du document dans la collection 'tasks'
    task = tasks_collection.find_one({"command_name_text": command_name})

    if task:
        print(f"Task found! ID : {task.get('_id')}")
        return task
    else:
        print(f"No task found with command name '{command_name}'")
        return None
    
def reconstitute_message(db, message_document):
    prompts_collection = db['prompts']  # Collection 'prompts'

    # Liste pour stocker le contenu des prompts
    reconstituted_message = []

    # Parcours des prompt_id dans le document message
    for prompt in message_document.get('prompts', []):
        prompt_id = prompt.get('prompt_id')
        
        # Recherche du prompt par son ID
        prompt_data = prompts_collection.find_one({"_id": prompt_id})
        
        if prompt_data:
            # Ajout du contenu du prompt à la liste
            reconstituted_message.append(prompt_data)
        else:
            print(f"Prompt with ID {prompt_id} not found.")

    # Assemblage du message final
    message_document['prompts'] = reconstituted_message

    return message_document

# Fonction pour récupérer les données de la tâche
def get_task_data(db, task):
    # Récupération des ids à partir du document task
    tool_id = task.get("tool_id")
    message_id = task.get("message_id")
    template_id = task.get("template_id")

    tool_data = db['tools'].find_one({"_id": tool_id})
    message_data = db['messages'].find_one({"_id": message_id})
    template_data = db['templates'].find_one({"_id": template_id})

    # Extraction des informations spécifiques des documents
    message_content = reconstitute_message(db, message_data)
    output_name = task.get("output_file_name")

    return {
        "tool": tool_data,
        "message": message_content,
        "template": template_data,
        "output_name": output_name
    }

# compléter le template jinja
def render_template_to_file(template_content, arguments, output_file_name):
    """
    Remplit un template Jinja avec les arguments fournis et enregistre le résultat dans un fichier.

    :param template_content: Le contenu du template Jinja sous forme de chaîne de caractères.
    :param arguments: Un dictionnaire contenant les arguments pour compléter le template.
    :param output_file_name: Le nom du fichier dans lequel enregistrer le rendu final.
    """
    # Crée un template Jinja à partir du contenu fourni
    template = Template(template_content)
    
    # Rendu du template avec les arguments
    rendered_content = template.render(arguments)
    
    # Écriture du rendu dans le fichier de sortie
    with open(output_file_name, 'w') as output_file:
        output_file.write(rendered_content)
    
    print(f"Template successfully rendered and saved to {output_file_name}")

def hash_data(data):
    """
    Hache les données en utilisant SHA-256.

    :param data: Les données à hacher (sous forme de dict).
    :return: Le haché SHA-256 sous forme de chaîne hexadécimale.
    """
    # Convertir le dictionnaire en chaîne JSON
    data_string = json.dumps(data, sort_keys=True)
    return hashlib.sha256(data_string.encode('utf-8')).hexdigest()

def save_call(collection, filtered_data, result):
    """
    Enregistre les données filtrées, leur haché comme _id, et le résultat dans MongoDB.

    :param collection: La collection MongoDB dans laquelle enregistrer les données.
    :param filtered_data: Les données filtrées (sous forme de dict).
    :param result: Le résultat à enregistrer avec les données.
    """
    hash_value = hash_data(filtered_data)

    document = {
        "_id": hash_value,  # Utilisation du hash comme ID du document
        "filtered_data": filtered_data,
        "result": result,
        "date": datetime.now()  # Utilisation de datetime.now() pour obtenir la date actuelle
    }

    try:
        collection.insert_one(document)
        print("Document successfully saved to MongoDB with _id:", hash_value)
    except DuplicateKeyError:
        print("Document with this _id already exists in MongoDB.")

def get_call(db, filtered_data, openai_client, model="gpt-3.5-turbo-0125"):
    calls_collection = db["gpt_calls"]
    hash = hash_data(filtered_data)

    # Recherche du document dans la collection 'tasks'
    call = calls_collection.find_one({"_id": hash})

    if call:
        result = call.get("result")
    else :
        #  faire un call api à chatGPT
        function_name = filtered_data.get("tool").get("function").get("name")
        response = get_completion(client = openai_client, 
                    messages = filtered_data.get("message").get("prompts"), 
                    tools = [filtered_data.get("tool")], 
                    function_name = function_name, 
                    model=model
                    )
        
        result = format_response(response)

        # Sauvegarde du call api
        save_call(calls_collection, filtered_data, result)

    return result

def main():
    # Charger les variables d'environnement à partir du fichier .env
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    uri = os.getenv('MONGO_URI')

    if not api_key or not uri:
        raise ValueError("API key or Mongo URI not found in environment variables.")

    # Initialisation du client de l'API ChatGPT
    openai_client = OpenAI(api_key=api_key)

    # Initialisation de la connexion à la base de données MongoDB
    mongo_client = init_mongo(uri)
    db = mongo_client['template_completion']

    # Parser la commande
    command, options = parse_arguments()

    # Trouver la tâche correspondant à la commande
    task = find_task_by_command(db, command)
    if not task:
        raise ValueError(f"No task found for command: {command}")

    # Récupération des données de la tâche
    data = get_task_data(db, task)
    filtered_data = remove_object_ids(data)
    # print("Command data\n", json.dumps(filtered_data, indent=4))

    # Appel à l'API ChatGPT
    result = get_call(db, filtered_data, openai_client)

    # Création du fichier basé sur le template
    render_template_to_file(
        template_content=filtered_data.get("template", {}).get("content"),
        arguments=result.get("function", {}).get("arguments", {}),
        output_file_name=filtered_data.get("output_name")
    )

if __name__ == "__main__":
    main()

