import os
import requests

def download_file(url, destination):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        os.makedirs(os.path.dirname(destination), exist_ok=True)

        with open(destination, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        print(f"Arquivo baixado com sucesso: {destination}")
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Erro ao baixar o arquivo: {e}")