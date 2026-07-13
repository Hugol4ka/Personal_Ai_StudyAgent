import asyncio
import sys

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
import warnings

from agents.explainer_agent import explainer_agent
from tools.file_writer import save_markdown_file


APP_NAME = "study_guide_generator"
USER_ID = "local_user"
SESSION_ID = "explainer_session"



warnings.filterwarnings("ignore", message="Pydantic serializer warnings")

async def run_explainer(topic: str) -> str:
    session_service = InMemorySessionService()
    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
    )

    runner = Runner(
        agent=explainer_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    user_message = types.Content(
        role="user",
        parts=[types.Part(text=f"Topic: {topic}")],
    )

    final_response = ""
    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=user_message,
    ):
        if event.is_final_response() and event.content and event.content.parts:
            final_response = event.content.parts[0].text

    return final_response


def main():
    topic = sys.argv[1] if len(sys.argv) > 1 else "Python decorators" 
    print(f"--- Génération de l'explication pour : {topic} ---\n")

    result = asyncio.run(run_explainer(topic))
    print(result)

    save_md = save_markdown_file(f"output/{topic.replace(' ', '_')}.md", result)
    print(save_md)


if __name__ == "__main__":
    main()