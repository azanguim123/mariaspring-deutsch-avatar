from src.config import DATA_DIR
from src.dialogue_engine import load_chapter, OralDialogueSession, record_microphone_wav


def main():
    chapter = load_chapter(DATA_DIR / "chapters.json", "a1_beim_arzt")
    photo = chapter["photos"][0] if chapter.get("photos") else None

    session = OralDialogueSession(chapter=chapter, active_photo=photo)
    opening = session.start_conversation()
    print("Avatar :", opening["text"])
    print("Audio généré :", opening["audio_path"])

    while True:
        choice = input("\nAppuie sur Entrée pour parler (5s), tape 't' pour écrire, ou 'q' pour quitter : ").strip().lower()
        if choice == "q":
            break
        elif choice == "t":
            user_msg = input("Toi (allemand) : ").strip()
            if not user_msg:
                continue
            res = session.send_user_text(user_msg)
            print("Avatar :", res["text"])
            print("Audio :", res["audio_path"])
        else:
            wav_file = session.audio_dir / "user_input.wav"
            print("Parle en allemand maintenant...")
            record_microphone_wav(wav_file, duration_sec=5)
            res = session.send_user_audio(wav_file)
            print("Transcription :", res.get("transcript", ""))
            print("Avatar :", res["text"])
            if res.get("audio_path"):
                print("Audio :", res["audio_path"])


if __name__ == "__main__":
    main()