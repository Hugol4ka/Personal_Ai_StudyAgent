from pathlib import Path

def save_markdown_file(file_path: str, content: str) -> str:
    """
    Save the given content to a markdown file at the specified path.

    Args:
        file_path (str): The path where the markdown file will be saved.
        content (str): The content to be written to the markdown file.
    """

    try:
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            return f"Le fichier a été sauvegardé avec succès à l'emplacement : {file_path}"
    except OSError as e:
        return f"Une erreur s'est produite lors de l'écriture dans le fichier : {e}"

