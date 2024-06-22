# AppMeshCLI

AppMeshCLI est un outil de ligne de commande robuste conçu pour accélérer et simplifier le développement d'applications en automatisant la génération de code pour divers frameworks et technologies. Cet outil est idéal pour les développeurs qui cherchent à optimiser la création d'APIs et d'interfaces utilisateur en utilisant des technologies modernes telles que C# .NET, Django pour le backend et Flutter pour le frontend.

## Fonctionnalités

### Génération Automatique de Code
- **Templates de Code :** Génère automatiquement des modèles, des vues, des contrôleurs et des DTOs pour la création d'APIs en C# .NET, Django, et d'autres frameworks.
- **Frontend Automation :** Crée des services pour la connexion aux APIs dans Flutter et génère également les modèles nécessaires.
- **Diagramme de Classes :** Produit un diagramme de classes de l'application au format DMBL avec ChatGPT pour une visualisation et une compréhension améliorées de la structure de l'application.

### Intégration et DevOps
- **Docker :** Automatise la création d'images Docker et de configurations Docker Compose pour faciliter le déploiement et la gestion des environnements.
- **Intégration Continue :** Suivi des avancements via Git, génération de tickets pour Jira directement depuis la CLI, et intégration avec Figma pour l'implémentation des maquettes.

### Documentation et Standards
- **Fichiers Standard :** Génère automatiquement des fichiers essentiels tels que `README.md`, `.gitignore`, et d'autres configurations nécessaires pour un projet prêt à l'emploi.

## Installation
```bash
# Installer AppMeshCLI
npm install -g appmeshcli
```

## Usage
```bash
# Créer un nouveau projet
appmeshcli create-project --name MonProjet --type django-flutter

# Générer des modèles, des vues et des contrôleurs
appmeshcli generate mvc --framework django

# Générer des services Flutter
appmeshcli generate service --framework flutter
```

## Contribuer
AppMeshCLI est ouvert aux contributions ! Si vous souhaitez améliorer l'outil ou suggérer de nouvelles fonctionnalités, n'hésitez pas à ouvrir un issue ou à soumettre une pull request.
