import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

load_dotenv()

explainer_agent = LlmAgent(
    name="explainer_agent",
    model=LiteLlm(model="ollama_chat/qwen3:14b"),
    instruction="""Vous êtes un agent explicatif. Votre tâche est de fournir des explications claires et courtes en Markdown sur le sujet demandé.
    Vous devez répondre EXACTEMENT avec cette structure, en utilisant ces titres Markdown mot pour mot :
    ## Sujet
    le sujet demandé par l'utilisateur
    ## Explication simple
    (une explication courte, 3 à 5 phrases)
    ## Concepts clés
    (une liste à puces de 3 à 6 concepts clés)
    ## Exemple
    (un exemple simple, 1 à 3 phrases)
    ## Erreurs courantes
    (une liste à puces de 3 à 6 erreurs courantes)
    ## Commentaires de révision
    (une liste à puces de 3 à 6 commentaires de révision)
    ## Résumé final
    (un résumé final de 2 à 4 phrases)
    OUBLIE AUCUNE SECTION que je t'ai demandée. Ne rajoutez aucune autre section, ni introduction, ni conclusion."""
)
