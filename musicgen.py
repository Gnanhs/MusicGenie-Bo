import requests
import time
import uuid

# Fonction pour générer la musique via Hugging Face API
def generate_music(prompt, token):
    API_URL = "https://api-inference.huggingface.co/models/facebook/musicgen-small"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "inputs": prompt,
        "parameters": {
            "do_sample": True,
            "duration": 10  # Durée en secondes (tu peux changer si besoin)
        }
    }

    print("Envoi de la requête à Hugging Face...")
    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        audio_data = response.content
        filename = f"music_{uuid.uuid4().hex}.wav"
        with open(filename, "wb") as f:
            f.write(audio_data)
        print(f"Musique générée avec succès : {filename}")
        return filename
    else:
        print(f"Erreur Hugging Face : {response.status_code} - {response.text}")
        return None
