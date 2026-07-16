# AI Agents in Python

## Description

Ce projet est un **générateur automatique de guides d'étude Markdown** pour des sujets de programmation. Il utilise un système multi-agent construit avec **Google ADK**, orchestré en local via **LiteLLM** et **Ollama**.

Le pipeline fonctionne en 3 étapes séquentielles :
1. Un **Explainer Agent** explique le sujet demandé (explication, concepts clés, exemple).
2. Un **Practice Designer Agent** conçoit un exercice pratique à partir de cette explication, et liste les erreurs courantes associées.
3. Un **Reviewer Agent** relit le brouillon complet, identifie ce qui manque ou est ambigu, et donne un résumé final.

Le résultat est ensuite **validé** (vérification de la présence de toutes les sections attendues) puis **sauvegardé** automatiquement en fichier `.md` dans `output/`.

## Requirements

- Python 3.12+
- [Ollama](https://ollama.com/) installé et lancé en local
- Modèles Ollama utilisés :
  - `qwen2.5-coder:7b` — Explainer Agent
  - `qwen3:14b` — Practice Designer Agent et Reviewer Agent
- Les dépendances Python listées dans `requirements.txt`

## Setup

```bash
git clone https://github.com/Hugol4ka/Personal_Ai-s_Agent.git
cd Personal_Ai_StudyAgent

# Environnement virtuel
python -m venv .venv
source .venv/bin/activate      # Windows : .venv\Scripts\activate

# Dépendances
pip install -r requirements.txt

# Modèles Ollama
ollama pull qwen3:14b 
```

## Configuration

Le projet utilise un fichier `.env` (non versionné) pour configurer le modèle utilisé par chaque agent. Copiez le fichier d'exemple avant de lancer le projet :

```bash
cp .env.example .env
```

Variables disponibles dans `.env` :

```bash
# Modèles Ollama utilisés par chaque agent
# Format attendu par LiteLLM : "ollama_chat/"
EXPLAINER_MODEL=ollama_chat/qwen3:14b
PRACTICE_MODEL=ollama_chat/qwen3:14b
REVIEWER_MODEL=ollama_chat/qwen3:14b
```

Chaque agent lit sa variable correspondante via `os.getenv(...)`, avec une valeur par défaut si la variable n'est pas définie — le projet fonctionne donc même sans `.env`, mais permet de changer facilement de modèle sans toucher au code.

Aucune clé API n'est nécessaire pour l'usage par défaut (Ollama en local). Si vous passez à un autre provider (Gemini, OpenAI, Claude...), ajoute la clé correspondante dans `.env` (jamais dans le code).

## How to Run

Assure-vous qu'Ollama tourne en arrière-plan :

```bash
ollama serve
```

Puis lancez le projet avec un sujet en argument :

```bash
python main.py "Python decorators"
```

Le sujet est **obligatoire** — le programme s'arrête avec un message d'erreur clair si l'argument est vide ou manquant.

## Example Input

```bash
python main.py "Websockets"
```

## Example Output
```markdown
## Sujet
websockets

## Explication simple
Les WebSockets sont une technologie qui permet aux navigateurs Web et aux serveurs de maintenir une connexion persistante ouverte, facilitant les échanges en temps réel.

## Concepts clés
- Connexion persistante : Une seule connexion entre le client et le serveur.
- Échange en temps réel : Transfert d'informations instantanées sans besoin de recharger la page.
- Protocole spécifique : Utilise l'hypertexte (HTTP) pour établir la connexion.

## Exemple
Un exemple courant est une chatbox en direct où les messages sont transmis instantanément entre le client et le serveur, sans rafraîchissement de la page.

## Exercice pratique  
**Énoncé** : Créez un serveur WebSocket et un client simple qui permettent d'envoyer des messages en temps réel entre deux navigateurs.  
- **Entrée** : Un client tape un message dans un champ de texte et clique sur "Envoyer".  
- **Sortie attendue** : Le message apparaît immédiatement dans l'interface du même client et dans celle d'un autre navigateur connecté.  
**Indices** :  
- Utilisez le protocole `ws://` pour le serveur (ex: `ws://localhost:8080`).  
- Sur le client, écoutez l'événement `message` pour recevoir les données.  
- Sur le serveur, utilisez `on('message', ...)` pour retransmettre les messages à tous les clients connectés.  

## Erreurs courantes  
- Utiliser une URL HTTP (`http://`) au lieu de WebSocket (`ws://`) pour établir la connexion.  
- Oublier de gérer l'événement `open` sur le client pour initialiser la connexion.  
- Envoyer des données non sérialisées (ex: objets JavaScript non convertis en JSON).  
- Ne pas broadcaster les messages vers tous les clients connectés sur le serveur.

## Commentaires de révision  
- **Manque de précision technique** : L'explication du protocole WebSocket mentionne l'utilisation de HTTP pour établir la connexion, mais ne précise pas le processus d'upgrade (HTTP → WebSocket) ni la négociation de protocole.  
- **Absence de détails sur les bibliothèques** : L'exercice pratique ne précise pas les bibliothèques à utiliser (ex: `ws` pour Node.js, `WebSocket` pour le client JS), ce qui pourrait bloquer les débutants.  
- **Exemple manquant de code** : Aucun exemple concret de code côté client ou serveur (même simplifié) n'est fourni, ce qui rend l'exercice moins guidé.  
- **Explication ambiguë sur les données sérialisées** : L'erreur courante sur la sérialisation ne précise pas pourquoi JSON est recommandé (sérialisation universelle, compatibilité, etc.).  
- **Suggestions d'amélioration** :  
  - Ajouter un diagramme ou une explication du processus de handshake WebSocket.  
  - Inclure un exemple de code minimal (ex: serveur Node.js avec `ws`, client HTML/JS).  
  - Clarifier la différence entre HTTP et WebSocket après l'upgrade.  
  - Ajouter une section sur les cas d'usage avancés (ex: jeux en temps réel, notifications push).  

## Résumé final  
Le guide est clair dans ses bases mais manque de détails techniques et d'exemples concrets. Il mérite une révision pour ajouter des explications sur le handshake WebSocket, des exemples de code et des précisions sur les bibliothèques. Approbation conditionnelle après ces améliorations.
```

## Project Structure

```
Personal_Ai_StudyAgent/
├── agents/
│   ├── explainer_agent.py
│   ├── practice_designer_agent.py
│   └── reviewer_agent.py
├── tools/
│   ├── file_writer.py
│   └── validation.py
├── output/
│   └── (fichiers .md générés)
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
└── main.py
```

## Agents

| Agent | Rôle |
|---|---|
| **explainer_agent** | Reçoit un sujet et génère une explication courte, des concepts clés, et un exemple. Ne s'occupe de rien d'autre. |
| **practice_designer_agent** | Reçoit le sujet et l'explication du premier agent, et conçoit un exercice pratique adapté à un débutant, accompagné d'indices et des erreurs courantes associées. |
| **reviewer_agent** | Reçoit le brouillon complet (explication + exercice) et produit des commentaires de révision constructifs ainsi qu'un résumé final. N'invente pas de nouveau contenu, ne remplace pas les autres agents. |

Chaque agent a une **responsabilité unique** : le workflow reste simple à comprendre et à déboguer, plutôt que d'avoir un seul agent qui tente de tout faire.

## Tools

| Outil | Rôle |
|---|---|
| **save_markdown_file** (`tools/file_writer.py`) | Sauvegarde le guide final en `.md` dans `output/`. Crée le dossier parent si besoin, et gère proprement les erreurs d'écriture (permissions, chemin invalide, disque en lecture seule...) sans faire planter le programme. |
| **validate_required_sections** (`tools/validation.py`) | Vérifie que les 8 sections attendues sont bien présentes dans le Markdown généré. Retourne un dictionnaire indiquant si le contenu est valide et la liste des sections manquantes, le cas échéant. |

Les deux outils sont **indépendants du framework d'agents** (aucun import ADK dedans) et ont été testés séparément avant d'être connectés au pipeline.

## Self-Validation Checklist

**Setup**
- [x] I created the required project directories.
- [x] I created README.md.
- [x] I created requirements.txt.
- [x] I created .env.example.
- [x] I created .gitignore.
- [x] I created main.py.
- [x] My project structure is easy to understand.
- [x] I created and activated a Python virtual environment.
- [x] I installed the required Python dependencies.
- [x] I installed Ollama.
- [x] I pulled a small local model.
- [x] I confirmed that the model responds locally.
- [x] I documented the setup process in README.md.
- [x] I documented the model I used.
- [x] I did not commit secrets or local environment files.

**Explainer Agent**
- [x] I created agents/explainer_agent.py.
- [x] My agent has a clear role.
- [x] My agent has specific instructions.
- [x] My agent receives a topic as input.
- [x] My agent returns a structured explanation.
- [x] I tested the agent with at least two topics.
- [x] I saved one example output in README.md.

**File Writer Tool**
- [x] I created tools/file_writer.py.
- [x] I implemented save_markdown_file().
- [x] The function receives a path and Markdown content.
- [x] The function writes a Markdown file to disk.
- [x] I tested the function without using the agent.
- [x] I used the function to save agent output.

**Validation Tool**
- [x] I created tools/validation.py.
- [x] I implemented validate_required_sections().
- [x] The function checks for all required sections.
- [x] The function reports missing sections.
- [x] I tested the function with valid Markdown.
- [x] I tested the function with incomplete Markdown.
- [x] I used the validator in the project workflow.

**Practice Designer Agent**
- [x] I created agents/practice_designer_agent.py.
- [x] The agent has a clear and separate responsibility.
- [x] The agent receives the topic.
- [x] The agent receives the previous explanation.
- [x] The agent generates a practice exercise.
- [x] The exercise includes hints.

**Reviewer Agent**
- [x] I created agents/reviewer_agent.py.
- [x] The agent reviews an existing draft.
- [x] The agent identifies missing or unclear parts.
- [x] The agent provides suggestions for improvement.
- [x] The agent does not replace the other agents.

**Full Workflow**
- [x] main.py runs the full workflow.
- [x] The Explainer Agent runs first.
- [x] The Practice Designer Agent uses the previous output.
- [x] The Reviewer Agent reviews the draft.
- [x] The final Markdown file includes all required sections.
- [x] The validation tool runs before or after saving.
- [x] Missing sections are reported clearly.
- [x] The final file is saved in output/study_guide.md.

**Error Handling & Config**
- [x] The project checks for empty topic input.
- [x] The project handles file-writing errors.
- [x] The project reports validation failures clearly.
- [x] The README includes troubleshooting notes.
- [x] The README explains how to configure the model provider.
- [x] The project does not expose secrets.
- [x] The review comments are included in the final Markdown file.
- [x] The exercise is appropriate for the topic.
- [x] The generated file appears in the output directory.
## Reflection

**1. Quelle est la différence entre un appel LLM direct et un agent IA ?**

Un appel LLM direct (comme `litellm.completion()`) est une simple requête-réponse isolée : on envoie un texte, on reçoit une réponse, sans structure imposée ni mémoire. Si on veut un comportement cohérent d'un appel à l'autre, il faut répéter le prompt complet à chaque fois.

Un agent (via `LlmAgent` d'ADK) encapsule un **rôle fixe** et des **instructions strictes** (le paramètre `instruction`), qui s'appliquent automatiquement à chaque appel — on n'a plus qu'à envoyer le sujet, pas de réécrire tout le prompt. L'agent s'intègre aussi dans un framework plus large (`Runner`, `Session`, flux d'événements) qui gère l'exécution de façon standardisée, et qui permettrait, si besoin, de gérer une mémoire de conversation multi-tours ou l'appel d'outils — même si dans ce projet, chaque agent n'est appelé qu'une seule fois par exécution, donc cette capacité de mémoire n'est pas pleinement exploitée.

**2. Quel rôle joue chaque agent dans mon système ?**

Voir la section [Agents](#agents) ci-dessus. En résumé : l'Explainer explique, le Practice Designer conçoit un exercice à partir de cette explication, et le Reviewer relit et commente l'ensemble — chacun avec une responsabilité unique, sans empiéter sur celle des autres. La communication entre eux n'est pas gérée automatiquement par ADK : c'est du code Python simple (concaténation de strings) qui transmet le texte généré par un agent en entrée du suivant, dans `run_multi_agent_pipeline()`.

**3. Quel rôle joue chaque outil dans mon système ?**

Voir la section [Tools](#tools) ci-dessus. `save_markdown_file` gère la persistance sur disque de façon déterministe (contrairement à la génération de texte, l'écriture d'un fichier doit toujours se comporter de la même façon). `validate_required_sections` fait un contrôle structurel simple et fiable — le but n'est pas de juger la qualité du contenu généré par les agents, mais de garantir que rien d'essentiel ne manque.

**4. Quelle a été la partie la plus difficile du projet ?**

La partie la plus difficile a été de comprendre le flux `Runner` / `Session` / événements d'ADK. Contrairement à un simple appel `completion()` qui retourne directement une réponse, `runner.run_async()` retourne un flux d'événements asynchrone qu'il faut parcourir avec `async for`, en filtrant l'événement final avec `event.is_final_response()`. Il a aussi fallu comprendre pourquoi une `Session` est nécessaire avant même de pouvoir lancer un agent, alors qu'elle n'est pas vraiment exploitée dans ce projet (chaque agent n'étant appelé qu'une fois, sans échange multi-tours).

**5. Quelle limitation ai-je observée avec le modèle sélectionné ?**

Avec `qwen3:14b`, un caractère chinois (`糖`, résidu du terme anglais *"syntactic sugar"*) s'est glissé au milieu d'une phrase en français lors d'une génération, sans raison apparente. Cela illustre une limitation connue des modèles locaux de taille modeste : un formatage et un vocabulaire parfois inconsistants, même avec des instructions strictes sur la langue et la structure attendues.

## Known Limitations

- **Formatage inconsistant** : le modèle local (14B) suit les instructions de structure de façon relativement fiable, mais pas garantie à 100 % — un mélange de langue a été observé (voir Reflection, point 5).
- **Logs verbeux d'ADK** : même lorsqu'une erreur est correctement interceptée par le `try/except` (par exemple `APIConnectionError` quand Ollama est arrêté), ADK affiche en interne une traceback complète dans la console avant que le message d'erreur personnalisé n'apparaisse. Ce n'est pas un bug du projet, mais un choix de logging interne de la librairie.
- **Validation structurelle uniquement** : `validate_required_sections` vérifie la présence des titres attendus, pas la pertinence ou la qualité du contenu — un guide peut être "valide" structurellement tout en étant peu utile sur le fond.
- **Pas de gestion de mémoire multi-tours** : chaque agent est appelé une seule fois par exécution ; le projet n'exploite pas la capacité de `Session` à conserver un historique de conversation.
- **Dépendance au matériel local** : *MacBook Pro puce M5, 24 Go RAM*.⎵⎵
  Le pipeline complet (3 appels LLM séquentiels) prend environ 2 minutes 30 sur ma machine. La quasi-totalité de ce temps est passée à attendre les réponses d'Ollama plutôt qu'à exécuter du code Python (moins de 1% de CPU côté script).
- **Nommage du fichier de sortie** : le fichier est actuellement sauvegardé sous `output/{sujet}.md` (nom dynamique basé sur le sujet), et non `output/study_guide.md` comme un nom fixe pourrait le suggérer.
