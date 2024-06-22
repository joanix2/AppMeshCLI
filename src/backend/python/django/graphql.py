def add_graphql_settings(project_path, project_name, app_name):
    # Chemin du fichier settings.py
    settings_path = os.path.join(project_path, project_name, project_name, 'settings.py')

    # Lire le contenu actuel de settings.py
    with open(settings_path, 'r') as file:
        settings_contents = file.readlines()

    # Ajout de 'graphene_django' aux applications installées
    added_graphene = False
    for i, line in enumerate(settings_contents):
        if 'INSTALLED_APPS' in line:
            while ']' not in settings_contents[i]:
                i += 1
            settings_contents.insert(i, "    'graphene_django',\n")
            added_graphene = True
            break

    # Ajout de la configuration GRAPHENE
    graphene_settings = "\nGRAPHENE = {\n    'SCHEMA': '" + app_name + ".schema.schema'\n}\n"
    if added_graphene:
        settings_contents.append(graphene_settings)
    else:
        raise Exception("INSTALLED_APPS not found in settings.py")

    # Réécrire settings.py avec les modifications
    with open(settings_path, 'w') as file:
        file.writelines(settings_contents)

    print(f"Graphene settings added to {settings_path}")


def create_graphql_schema(app_path, models_tree):
    # Chemin vers le fichier schema.py
    schema_file_path = os.path.join(app_path, "schema.py")
    models_names = [node.name for node in ast.walk(models_tree) if isinstance(node, ast.ClassDef)]
    
    schema_template = env.get_template('schema_template.j2')

    with open(schema_file_path, 'w') as f:
        # Génération du schéma complet
        f.write(schema_template.render(classes=models_names))

def add_graphql_url(urls_path, app_name):
    with open(urls_path, 'r+') as f:
        content = f.read()
        content = content.replace("from django.urls import path", f"from django.urls import path\nfrom graphene_django.views import GraphQLView\nfrom {app_name}.schema import schema")
        content = content.replace("urlpatterns = [", "urlpatterns = [\n    path('graphql/', GraphQLView.as_view(graphiql=True, schema=schema)),")
        f.seek(0)
        f.write(content)
        f.truncate()
