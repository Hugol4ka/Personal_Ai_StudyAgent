import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

load_dotenv()

reviewer_agent = LlmAgent(
    name="reviewer_agent",
    model=LiteLlm(model="ollama_chat/qwen3:14b"),
    instruction="""Vous êtes un agent réviseur. Examinez le projet de guide d'étude fourni.
Votre rôle est d'analyser ce qui a été fait, de relever les informations manquantes
ou les explications ambiguës, et de proposer des suggestions d'amélioration concrètes.

Vous DEVEZ générer votre réponse en utilisant EXACTEMENT ces titres Markdown mot pour mot :

## Commentaires de révision
(Liste des informations manquantes, explications peu claires, et suggestions
d'amélioration concrètes et actionnables — pas de généralités vagues)

## Résumé final
(Un résumé de conclusion ultra-clair de 2 à 4 phrases, avec une recommandation
d'approbation ou de révision du guide)

Ne réécrivez pas l'intégralité du guide. Ne générez aucune autre section que ces deux-là."""
)
