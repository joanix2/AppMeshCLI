import json

class JsonDict(dict):
    def __init__(self, filepath):
        super().__init__()
        self.filepath = filepath
        self._load_from_json()

    def _load_from_json(self):
        """Charge les données depuis le fichier JSON."""
        try:
            with open(self.filepath, 'r') as file:
                data = json.load(file)
                self.update(data)
        except FileNotFoundError:
            print(f"Le fichier {self.filepath} n'existe pas. Un nouveau fichier sera créé.")
        except json.JSONDecodeError:
            print(f"Le fichier {self.filepath} n'est pas un JSON valide.")

    def _write_to_json(self):
        """Écrit les données dans le fichier JSON."""
        with open(self.filepath, 'w') as file:
            json.dump(self, file, indent=4, ensure_ascii=False)

    def __setitem__(self, key, value):
        super(JsonDict, self).__setitem__(key, value)
        self._write_to_json()

    def update(self, *args, **kwargs):
        super(JsonDict, self).update(*args, **kwargs)
        self._write_to_json()