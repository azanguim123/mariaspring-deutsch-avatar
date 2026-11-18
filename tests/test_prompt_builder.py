from src.prompt_builder import build_system_prompt


def test_build_system_prompt_includes_level_and_title():
    chapter = {
        "id": "a1_beim_arzt",
        "level": "A1",
        "title": "Beim Arzt",
        "objectives": ["Dire où l'on a mal"],
        "vocabulary": ["der Kopf"],
        "grammar_focus": ["wehtun au datif"],
        "photos": [],
    }
    prompt = build_system_prompt(chapter, None)
    assert "A1" in prompt
    assert "Beim Arzt" in prompt