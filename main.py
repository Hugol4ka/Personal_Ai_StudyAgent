import asyncio
import sys

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
import warnings
from litellm.exceptions import APIConnectionError

from agents.explainer_agent import explainer_agent
from tools.file_writer import save_markdown_file
from tools.validation import validate_required_sections
from agents.practise_designer_agent import practice_designer_agent
from agents.reviewer_agent import reviewer_agent


APP_NAME = "study_guide_generator"
USER_ID = "local_user"
SESSION_ID_EXPLAINER = "explainer_session"
SESSION_ID_PRACTICE = "practice_session"
SESSION_ID_REVIEWER = "reviewer_session"


warnings.filterwarnings("ignore", message="Pydantic serializer warnings")


async def run_multi_agent_pipeline(topic: str) -> str:

    YELLOW = "\033[93m"
    RESET = "\033[0m"
    session_service = InMemorySessionService()
    
    # Lancement de l'Explainer Agent
    await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID_EXPLAINER)
    runner_explainer = Runner(agent=explainer_agent, app_name=APP_NAME, session_service=session_service)
    
    user_message = types.Content(role="user", parts=[types.Part(text=f"Topic: {topic}")])
    
    explanation_response = ""
    async for event in runner_explainer.run_async(user_id=USER_ID, session_id=SESSION_ID_EXPLAINER, new_message=user_message):
        if event.is_final_response() and event.content and event.content.parts:
            explanation_response = event.content.parts[0].text

    print(f"{YELLOW}🤖 Explainer Agent a terminé sa partie.{RESET}")

    # Lancement du Practice Designer Agent
    await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID_PRACTICE)
    runner_practice = Runner(agent=practice_designer_agent, app_name=APP_NAME, session_service=session_service)
    
    # Transmission du sujet ET ce que le premier agent a écrit
    context_for_practice = f"Sujet d'origine : {topic}\n\nExplication du cours :\n{explanation_response}"
    practice_message = types.Content(role="user", parts=[types.Part(text=context_for_practice)])
    
    practice_response = ""
    async for event in runner_practice.run_async(user_id=USER_ID, session_id=SESSION_ID_PRACTICE, new_message=practice_message):
        if event.is_final_response() and event.content and event.content.parts:
            practice_response = event.content.parts[0].text

    print(f"{YELLOW}🤖 Practice Designer Agent a terminé sa partie.{RESET}")

    # Lancement du Reviewer Agent
    await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID_REVIEWER)
    runner_reviewer = Runner(agent=reviewer_agent, app_name=APP_NAME, session_service=session_service)

    # Transmission du sujet ET ce que les deux premiers agents ont écrit
    context_for_reviewer = f"Sujet d'origine : {topic}\n\nExplication du cours :\n{explanation_response}\n\nExercice pratique :\n{practice_response}"
    reviewer_message = types.Content(role="user", parts=[types.Part(text=context_for_reviewer)])

    reviewer_response = ""
    async for event in runner_reviewer.run_async(user_id=USER_ID, session_id=SESSION_ID_REVIEWER, new_message=reviewer_message):
        if event.is_final_response() and event.content and event.content.parts:
            reviewer_response = event.content.parts[0].text

    print(f"{YELLOW}🤖 Reviewer Agent a terminé sa partie.{RESET}")

    # Fusion des résultats
    full_guide = f"## Sujet\n{topic}\n\n{explanation_response}\n\n{practice_response}\n\n{reviewer_response}"
    return full_guide


def main():
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RESET = "\033[0m"

    topic = sys.argv[1] if len(sys.argv) > 1 else None
    if not topic or not topic.strip():
        print("❌ Erreur : Le sujet (topic) ne peut pas être vide.")
        sys.exit(1)

    print(f"{CYAN}--- Génération de l'explication pour : {topic} ---{RESET}\n")
    try:
        result = asyncio.run(run_multi_agent_pipeline(topic))
        print(result)
    except APIConnectionError as e:
        print(f"❌ Erreur lors de la génération : {e}")
        print("💡 Vérifie qu'Ollama est bien lancé (commande : ollama serve) et que le modèle est disponible.")
        sys.exit(1)

    print(f"{CYAN}--- Validation des sections requises ---{RESET}")
    validation = validate_required_sections(result)
    if validation['missing_sections']:
        print(f"{YELLOW}Sections manquantes : {', '.join(validation['missing_sections'])}{RESET}")
    else:
        print(f"{GREEN}Sections valide : {validation['is_valid']}{RESET}")

    print(f"{CYAN}--- [TOOL] Sauvegarde du fichier ---{RESET}")
    save_md = save_markdown_file(f"output/{topic.replace(' ', '_')}.md", result)
    print(f"{GREEN}{save_md}{RESET}")


if __name__ == "__main__":
    main()
