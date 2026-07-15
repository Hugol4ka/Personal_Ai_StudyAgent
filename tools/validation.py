required_sections = [
    "## Sujet",
    '## Explication simple',
    "## Concepts clés",
    "## Exemple",
    "## Exercice pratique",
    "## Erreurs courantes",
    "## Commentaires de révision",
    "## Résumé final",
    ]

def validate_required_sections(markdown: str) -> dict:
    """Validate that the markdown content contains all required sections.

    Args:
        markdown (str): The markdown content to validate.
    Returns:
        dict: A dictionary containing whether the content is valid ("is_valid")
            and a list of any missing sections ("missing_sections").
    """
    missing_sections = []
    for section in required_sections:
        if section not in markdown:
            missing_sections.append(section)
    return {
        "is_valid": len(missing_sections) == 0,
        "missing_sections": missing_sections
    }

