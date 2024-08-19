import json
from jinja2 import Environment, FileSystemLoader

# Dictionnaire pour traduire les types JSON vers les types Flutter
TYPE_TRANSLATION = {
    'string': 'String',
    'integer': 'int',
    'boolean': 'bool',
    # Ajoutez d'autres types si nécessaire
}

# Dictionnaire pour déterminer les valeurs par défaut en Flutter
DEFAULT_VALUES = {
    'string': "''",
    'integer': '0',
    'boolean': 'false',
    # Ajoutez d'autres types si nécessaire
}

# Fonction pour déterminer le type de variable en Flutter en utilisant un dictionnaire
def get_flutter_variable_type(field_type):
    return TYPE_TRANSLATION.get(field_type, 'dynamic')

# Fonction pour déterminer la valeur par défaut en Flutter en utilisant un dictionnaire
def get_default_value(field_type):
    return DEFAULT_VALUES.get(field_type, 'null')


# Fonction pour générer le code Flutter d'un formulaire à partir du schéma JSON en utilisant un template Jinja2
def generate_flutter_form_with_template(json_schema):
    title = json_schema.get('title', 'Form')
    properties = json_schema.get('properties', {})
    required = json_schema.get('required', [])

    fields = {field: get_flutter_variable_type(specs['type']) for field, specs in properties.items()}
    default_values = {field: get_default_value(specs['type']) for field, specs in properties.items()}

    # Configurer l'environnement Jinja2 pour charger le template
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('flutter_form.jinja2')

    # Générer le code en utilisant le template et les données du schéma
    flutter_code = template.render(
        class_name=title,
        fields=fields,
        required=required,
        default_values=default_values
    )

    return flutter_code

def main():
    # Exemple de JSON Schema
    json_schema = {
        "title": "Person",
        "type": "object",
        "properties": {
            "firstName": {"type": "string"},
            "lastName": {"type": "string"},
            "age": {"type": "integer", "minimum": 0},
            "email": {"type": "string", "format": "email"},
            "isEmployed": {"type": "boolean"}
        },
        "required": ["firstName", "lastName"]
    }

    # Exécution de la génération de code
    flutter_code = generate_flutter_form_with_template(json_schema)
    print(flutter_code)

if __name__ == '__main__':
    main()
