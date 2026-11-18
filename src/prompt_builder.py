from typing import Any, Dict, Optional


def build_system_prompt(chapter: Dict[str, Any], active_photo: Optional[Dict[str, Any]] = None) -> str:
    level = chapter["level"]
    title = chapter["title"]
    vocab = ", ".join(chapter.get("vocabulary", []))
    grammar = ", ".join(chapter.get("grammar_focus", []))
    objectives = "\n- ".join(chapter.get("objectives", []))

    if level in ("A1", "A2"):
        style_rules = (
            "- Utilise des phrases courtes, simples et claires en allemand.\n"
            "- Parle lentement et clairement dans l'esprit d'un tuteur bienveillant.\n"
            "- Si l'étudiant bloque, aide-le avec un mot-clé ou une question fermée simple."
        )
    else:
        style_rules = (
            "- Utilise un allemand naturel et nuancé adapté au niveau intermédiaire/avancé.\n"
            "- Pose des questions ouvertes et demande de justifier ou de reformuler.\n"
            "- Sois attentif à l'ordre des mots (verbe en 2e position, verbe en fin de subordonnée) et aux cas."
        )

    photo_context = ""
    if active_photo:
        questions_hint = ", ".join(active_photo.get("prompt_questions", []))
        photo_context = (
            f"\nPhoto active affichée à l'étudiant :\n"
            f"- Description : {active_photo.get('description', '')}\n"
            f"- Idées de relance visuelle : {questions_hint}\n"
        )

    return f"""Tu es un tuteur d'allemand oral intégré à l'application du centre de langues Mariaspring.
Ton rôle est de faire parler l'étudiant à voix haute sur le chapitre en cours.

Contexte du cours :
- Niveau : {level}
- Titre du chapitre : {title}
- Objectifs :
- {objectives}
- Vocabulaire cible : {vocab}
- Points de grammaire ciblés : {grammar}
{photo_context}
Règles pédagogiques :
{style_rules}
- Parle principalement en allemand adapté au niveau ({level}). N'utilise le français que pour de brèves explications grammaticales ou de correction.
- Réponds toujours d'abord de façon naturelle dans le dialogue pour maintenir la conversation vivante.
- Corrige maximum 1 ou 2 erreurs importantes à la fois : reformule la phrase correctement en allemand et explique brièvement en français (ou allemand simple selon le niveau) pourquoi.
- Ne fais pas de cours magistral : garde la conversation interactive et encourageante.
- Termine presque toujours par une question ou une relance liée au chapitre ou à la photo.
"""