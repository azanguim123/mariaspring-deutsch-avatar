# Mariaspring Deutsch Avatar

Application d'entraînement à l'expression orale en allemand basée sur un avatar interactif et des supports de cours structurés par **niveau** (`A1`–`B2`), **titre de chapitre** et **photos thématiques**.

## Contexte du projet

Ce projet est né d'un besoin observé au centre de langues **Mariaspring** : les apprenants disposent de bases théoriques et de cours structurés, mais manquent d'occasions régulières et sans appréhension de pratiquer l'allemand à voix haute en dehors des heures de cours.

L'application vise à :
- Proposer des dialogues oraux alignés sur le programme et le vocabulaire de chaque chapitre.
- S'appuyer sur les photos liées au thème pour stimuler la prise de parole et la description.
- Adapter le niveau de langue, les relances et les corrections (grammaire, ordre des mots, prononciation) au niveau de l'étudiant.
- Fournir un outil complémentaire utile aux étudiants comme aux encadrants.

## Architecture du projet

```text
mariaspring-deutsch-avatar/
├── .env.example                  # Exemple de variables d'environnement
├── .gitignore                    # Règles d'exclusion Git
├── README.md                     # Documentation du projet
├── requirements.txt              # Dépendances Python
├── data/
│   └── chapters.json             # Données des chapitres, objectifs, vocabulaire et photos
├── assets/
│   └── chapters/                 # Images associées aux niveaux et thèmes
├── src/
│   ├── __init__.py
│   ├── config.py                 # Configuration et chemins du projet
│   ├── prompt_builder.py         # Construction dynamique du prompt système
│   ├── dialogue_engine.py        # Pipeline oral (STT -> LLM -> TTS) [en cours]
│   ├── avatar_controller.py      # Gestion et animation de l'avatar [en cours]
│   └── app.py                    # Application principale [en cours]
└── tests/
    └── test_prompt_builder.py    # Tests unitaires

```  
1. Installation de l'environnement
Cloner le dépôt et entrer dans le dossier : git clone <URL_DU_DEPOT>
cd mariaspring-deutsch-avatar

2. Créer et activer un environnement virtuel Python : python -m venv .venv
.\.venv\Scripts\Activate.ps1

3. Installer les dépendances :
pip install --upgrade pip
pip install -r requirements.txt

4. Configurer les variables d'environnement :
Copier .env.example vers .env et ajuster les paramètres selon votre machine :
copy .env.example .env

Feuille de route de développement
    [x] Étape 1 : Modélisation des données par chapitre (chapters.json) et génération dynamique du prompt système (src/prompt_builder.py).

    [x] Étape 2 : Moteur de dialogue oral en allemand (STT -> LLM -> TTS).

    [ ] Étape 3 : Intégration de l'avatar et synchronisation/réactivité.

    [ ] Étape 4 : Interface utilisateur complète (choix du niveau, chapitre, photo active, session orale).

    [ ] Étape 5 : Tests pilotes et présentation au centre de langues Mariaspring.