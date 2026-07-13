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