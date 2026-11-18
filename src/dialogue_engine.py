import asyncio
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests

from src.config import BASE_DIR
from src.prompt_builder import build_system_prompt

# Chargement paresseux des modèles lourds pour éviter de ralentir les imports
_whisper_model = None


def _get_whisper_model():
    global _whisper_model
    if _whisper_model is None:
        from faster_whisper import WhisperModel

        model_size = os.getenv("WHISPER_MODEL_SIZE", "small")
        device = os.getenv("WHISPER_DEVICE", "cpu")
        compute_type = os.getenv("WHISPER_COMPUTE_TYPE", "int8")
        _whisper_model = WhisperModel(
            model_size,
            device=device,
            compute_type=compute_type,
        )
    return _whisper_model


def transcribe_audio(audio_path: str | Path, language: str = "de") -> str:
    """Transcrit un fichier audio (.wav / .mp3) vers du texte en allemand."""
    model = _get_whisper_model()
    segments, _ = model.transcribe(
        str(audio_path),
        language=language,
        vad_filter=True,
    )
    text = " ".join(segment.text.strip() for segment in segments).strip()
    return text


def generate_llm_reply(
    messages: List[Dict[str, str]],
    model: Optional[str] = None,
    base_url: Optional[str] = None,
) -> str:
    """Envoie l'historique de conversation à Ollama et retourne la réponse de l'avatar."""
    ollama_url = base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    ollama_model = model or os.getenv("OLLAMA_MODEL", "llama3.2")

    payload = {
        "model": ollama_model,
        "messages": messages,
        "stream": False,
    }

    response = requests.post(
        f"{ollama_url.rstrip('/')}/api/chat",
        json=payload,
        timeout=120,
    )
    response.raise_for_status()
    data = response.json()
    return data["message"]["content"].strip()


async def _synthesize_edge_tts(text: str, output_file: Path, voice: str) -> Path:
    import edge_tts

    output_file.parent.mkdir(parents=True, exist_ok=True)
    communicate = edge_tts.Communicate(text=text, voice=voice)
    await communicate.save(str(output_file))
    return output_file


def synthesize_speech(
    text: str,
    output_file: str | Path,
    voice: Optional[str] = None,
) -> Path:
    """Génère un fichier audio (.mp3) en allemand à partir de la réponse texte."""
    target_path = Path(output_file)
    selected_voice = voice or os.getenv("TTS_VOICE_DE", "de-DE-KatjaNeural")
    return asyncio.run(_synthesize_edge_tts(text=text, output_file=target_path, voice=selected_voice))


def record_microphone_wav(output_path: str | Path, duration_sec: int = 5, sample_rate: int = 16000) -> Path:
    """Enregistre l'audio du microphone pendant duration_sec secondes dans un fichier WAV."""
    import sounddevice as sd
    from scipy.io.wavfile import write

    target = Path(output_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    recording = sd.rec(
        int(duration_sec * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype="int16",
    )
    sd.wait()
    write(str(target), sample_rate, recording)
    return target


class OralDialogueSession:
    """Gère une session de conversation orale liée à un chapitre et une photo."""

    def __init__(self, chapter: Dict[str, Any], active_photo: Optional[Dict[str, Any]] = None):
        self.chapter = chapter
        self.active_photo = active_photo
        self.system_prompt = build_system_prompt(chapter, active_photo)
        self.messages: List[Dict[str, str]] = [
            {"role": "system", "content": self.system_prompt}
        ]
        audio_dir = BASE_DIR / os.getenv("AUDIO_OUTPUT_DIR", "outputs/audio")
        self.audio_dir = audio_dir
        self.turn_index = 0

    def start_conversation(self) -> Dict[str, Any]:
        """Fait démarrer l'avatar en allemand sur le thème du chapitre."""
        starter_instruction = {
            "role": "user",
            "content": (
                "Beginne das Gespräch kurz und freundlich auf Deutsch zum aktuellen Kapitel "
                "und stelle eine einfache Einstiegsfrage."
            ),
        }
        reply_text = generate_llm_reply(self.messages + [starter_instruction])
        self.messages.append({"role": "assistant", "content": reply_text})
        self.turn_index += 1
        audio_path = self.audio_dir / f"{self.chapter['id']}_turn_{self.turn_index}.mp3"
        synthesize_speech(reply_text, audio_path)
        return {"text": reply_text, "audio_path": str(audio_path)}

    def send_user_text(self, user_text: str) -> Dict[str, Any]:
        """Traite un message texte de l'étudiant et génère texte + audio de réponse."""
        self.messages.append({"role": "user", "content": user_text})
        reply_text = generate_llm_reply(self.messages)
        self.messages.append({"role": "assistant", "content": reply_text})
        self.turn_index += 1
        audio_path = self.audio_dir / f"{self.chapter['id']}_turn_{self.turn_index}.mp3"
        synthesize_speech(reply_text, audio_path)
        return {"text": reply_text, "audio_path": str(audio_path)}

    def send_user_audio(self, audio_path: str | Path) -> Dict[str, Any]:
        """Transcrit l'audio de l'étudiant, génère la réponse et synthétise l'audio."""
        transcript = transcribe_audio(audio_path, language="de")
        if not transcript:
            return {
                "transcript": "",
                "text": "Entschuldigung, ich habe dich nicht gut verstanden. Kannst du das bitte noch einmal sagen?",
                "audio_path": None,
            }
        result = self.send_user_text(transcript)
        result["transcript"] = transcript
        return result


def load_chapter(chapters_json_path: str | Path, chapter_id: str) -> Dict[str, Any]:
    """Charge un chapitre précis depuis chapters.json."""
    with open(chapters_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    chapters = data["chapters"] if isinstance(data, dict) and "chapters" in data else data
    for chapter in chapters:
        if chapter["id"] == chapter_id:
            return chapter
    raise ValueError(f"Chapitre introuvable : {chapter_id}")