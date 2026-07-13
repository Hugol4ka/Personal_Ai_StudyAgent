# Personal AI Study Agent 🤖📚

Ce projet est un générateur de guides d'étude automatisé, construit avec Python. Il utilise une architecture d'agents autonomes pour expliquer des concepts techniques et générer des quiz.

## 🛠️ Stack Technique

* **Langage :** Python 3
* **Orchestration LLM :** LiteLLM
* **Modèle local :** Ollama
* **Modèle utilisé :** `qwen2.5-coder:7b` (Spécialisé dans le code et les explications techniques)

## 🚀 Comment lancer le projet

1. Créez un environnement virtuel et installez les dépendances Python :
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt

2. Assurez-vous d'avoir installé [Ollama](https://ollama.com/) et téléchargé le modèle :
   ```bash
   ollama pull qwen2.5-coder:7b

## Exemple Output/utilisation

1. Sans argument, Avec la possibilité de modifié directement dans le main.py
   ```bash
   def main():
    topic = sys.argv[1] if len(sys.argv) > 1 else "Python decorators" 
    print(f"--- Génération de l'explication pour : {topic} ---\n")

    result = asyncio.run(run_explainer(topic))
    print(result)
<img width="1077" height="845" alt="Capture d’écran 2026-07-13 à 13 52 38" src="https://github.com/user-attachments/assets/1a43bb14-436f-45b2-b6ea-babf15a708dd" />

3. Avec argument:
   ```bash
   python main.py  "Websockets"
<img width="1075" height="724" alt="Capture d’écran 2026-07-13 à 13 54 36" src="https://github.com/user-attachments/assets/b7c48307-7e3f-4688-97ae-17121e528518" />
