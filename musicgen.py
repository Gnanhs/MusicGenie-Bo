import requests

def generate_music(prompt: str, token: str) -> str:
    API_URL = "https://api-inference.huggingface.co/models/facebook/musicgen-small"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"inputs": prompt}

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        # L'API retourne un lien de téléchargement temporaire
        with open("output.wav", "wb") as f:
            f.write(response.content)
        return "output.wav"
    else:
        print("Erreur de génération :", response.status_code, response.text)
        return None
