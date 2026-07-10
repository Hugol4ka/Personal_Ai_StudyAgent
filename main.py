import os
from dotenv import load_dotenv
from litellm import completion

load_dotenv()

model_name = os.getenv("MODEL_NAME")
api_base = os.getenv("OLLAMA_API_BASE")

print(f"Using model: {model_name} with API base: {api_base}")

response = completion(
    model=model_name,
    messages=[{"role": "user", "content": "Dis-moi 'L'environnement local fonctionne !' en trois mots."}],
    api_base=api_base
)
print("\nSuccès ! Réponse du modele :")
print(response.choices[0].message.content)
