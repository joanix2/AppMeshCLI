import subprocess

def run_command(command:str):
    """Exécute une commande shell et affiche la sortie en temps réel."""
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Afficher la sortie en temps réel
    for line in process.stdout:
        print(line, end='')

    # Capturer la sortie d'erreur, s'il y en a
    for line in process.stderr:
        print(line, end='')

    process.wait()

    if process.returncode != 0:
        raise subprocess.CalledProcessError(process.returncode, command)