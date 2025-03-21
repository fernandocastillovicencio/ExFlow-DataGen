import os

def create_directory(path):
    """Cria um diretório se ele não existir."""
    os.makedirs(path, exist_ok=True)
