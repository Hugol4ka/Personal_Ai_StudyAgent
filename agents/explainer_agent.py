import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

load_dotenv()

MODEL_NAME = os.getenv("EXPLAINER_MODEL", "ollama_chat/qwen2.5-coder:7b")

explainer_agent = LlmAgent(
    name="explainer_agent",
    model=LiteLlm(model=MODEL_NAME),
instruction="""Vous êtes un agent explicatif. Votre tâche est de fournir des explications claires et courtes en Markdown sur le sujet demandé.
    Vous devez répondre EXACTEMENT avec cette structure, en utilisant ces titres Markdown mot pour mot :
    ## Explication simple
    (une explication courte, 3 à 5 phrases)
    ## Concepts clés
    (une liste à puces de 3 à 6 concepts clés)
    ## Exemple
    (un exemple simple, 1 à 3 phrases)
    Ne rajoutez aucune autre section, ni introduction, ni conclusion."""
)
