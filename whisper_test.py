import sounddevice as sd
import numpy as np
import whisper
import re

print("🧠 Loading Whisper (small.en) for max accuracy…")
model = whisper.load_model("small.en")

SAMPLERATE = 16000
DURATION = 3  # DO NOT CHANGE - best accuracy for your voice

def parse_chess_move(text):
    text = text.lower()

    # Fix common accent / mishear issues
    replacements = {
        "for": "4",
        "four": "4",
        "to ": "2 ",
        "too": "2",
        "two": "2",
        "one": "1",
        "won": "1",
        "free": "3",
        "three": "3",
        "eat": "e",
        "bee": "b",
        "be ": "b ",
        "see": "c",
        "sea": "c",
        "dee": "d",
        "gee": "g",
    }
    for k, v in replacements.items():
        text = text.replace(k, v)

    # Extract chess square coordinates
    coords = re.findall(r"[a-h][1-8]", text)

    if len(coords) == 2:
        return coords[0], coords[1]
    return None, None


print("\n🎤 Say something like: 'pawn e2 to e4'")
print("(Ctrl + C to stop)\n")

while True:
    print("🎧 Listening...")
    audio = sd.rec(int(SAMPLERATE * DURATION), samplerate=SAMPLERATE, channels=1)
    sd.wait()

    audio = np.squeeze(audio)
    result = model.transcribe(audio, language="en")
    text = result["text"].strip()

    if not text:
        print("😅 Didn't catch that, try again!")
        continue

    print("Heard:", text)

    src, dst = parse_chess_move(text)
    if src and dst:
        print(f"✔ Parsed Move: {src} → {dst}\n")
    else:
        print("❌ Couldn't detect a valid move\n")
