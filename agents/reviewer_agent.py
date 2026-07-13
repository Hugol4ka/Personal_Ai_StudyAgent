import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

load_dotenv()

reviewer_agent = LlmAgent(
    name="reviewer_agent",
    model=LiteLlm(model="ollama_chat/qwen3:14b"),
    instruction="""Vous êtes un agent réviseur. Examinez le projet de guide d’étude (cours et exercice) fourni.
    Votre rôle est d'analyser ce qui a été fait, de pointer les pièges et d'apporter la touche finale de qualité.
    
    Vous DOIS générer votre réponse en utilisant EXACTEMENT ces trois titres Markdown mot pour mot :
    
    ## Erreurs courantes
    (Une liste à puces des pièges classiques ou erreurs de syntaxe des débutants sur ce sujet)
    
    ## Commentaires de révision
    (Vos critiques constructives sur le brouillon, les points améliorés ou clarifiés)
    
    ## Résumé final
    (Un résumé de conclusion ultra-clair de 2 à 4 phrases maximum)
    
    Ne réécrivez pas l'intégralité du guide. Ne générez aucune autre section que ces trois-là."""
)
