import sounddevice as sd
import numpy as np
import whisper
import re
import json
import os

MAPPING_FILE = "voice_mapping.json"

print("🧠 Loading Whisper (small.en) for max accuracy…")
model = whisper.load_model("small.en")

SAMPLERATE = 16000
DURATION = 3  # best settings for your voice

# ---------------- Mapping Memory ---------------- #

def load_mapping():
    if os.path.exists(MAPPING_FILE):
        try:
            with open(MAPPING_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_mapping(mapping):
    with open(MAPPING_FILE, "w") as f:
        json.dump(mapping, f, indent=2)

voice_mapping = load_mapping()
print(f"📁 Learned mappings loaded: {len(voice_mapping)} phrases.\n")

# ---------------- Parsing ---------------- #

piece_keywords = {
    "pawn": "P",
    "night": "N",
    "knight": "N",
    "bishop": "B",
    "rook": "R",
    "queen": "Q",
    "king": "K",
}

def detect_piece(text):
    for word, symbol in piece_keywords.items():
        if word in text:
            return symbol
    return "P"  # default pawn

def parse_chess_move(text):
    text = text.lower()

    # Common replacements for accents
    replacements = {
        "for": "4", "four": "4",
        "to": "2", "too": "2", "two": "2",
        "one": "1", "won": "1",
        "free": "3", "three": "3",
        "sea": "c", "see": "c",
        "bee": "b", "be ": "b ",
        "dee": "d",
        "gee": "g"
    }
    for k, v in replacements.items():
        text = text.replace(k, v)

    # Detect piece
    piece = detect_piece(text)

    # Extract squares
    coords = re.findall(r"[a-h][1-8]", text)

    if len(coords) == 2:
        return piece, coords[0], coords[1]
    return None, None, None

# ---------------- Main Loop ---------------- #

print("🎤 Speak moves like: 'knight g1 to f3' or 'pawn e2 e4'")
print("🤖 I will ask: Is this correct? (y/n)")
print("(Ctrl+C to stop)\n")

while True:
    print("🎧 Listening...")
    audio = sd.rec(int(SAMPLERATE * DURATION), samplerate=SAMPLERATE, channels=1)
    sd.wait()

    audio = np.squeeze(audio)
    result = model.transcribe(audio, language="en")
    text = result["text"].strip()

    if not text:
        print("😅 Didn't catch that!\n")
        continue

    print(f"\n👂 Heard: {text}")

    norm = text.lower().strip()

    # Check if learned already
    if norm in voice_mapping:
        move = voice_mapping[norm]
        piece, src, dst = move["piece"], move["src"], move["dst"]
        print(f"📚 Known phrase → {piece} {src} → {dst}")
    else:
        piece, src, dst = parse_chess_move(text)
        if src and dst:
            print(f"🧩 Guess: {piece} from {src} → {dst}")
        else:
            print("❌ Could not parse move.")

    ans = input("Correct? (y/n): ").strip().lower()
    if ans == "y" and src and dst:
        voice_mapping[norm] = {"piece": piece, "src": src, "dst": dst}
        save_mapping(voice_mapping)
        print("💾 Saved.\n")
        continue

    print("↩ Correction needed:")
    corr = input("Enter correct move (e.g., N g1 f3 or e2 e4): ").strip().lower()

    m = re.match(r"([pnbrqk])?\s*([a-h][1-8])\s+([a-h][1-8])", corr)
    if m:
        piece = m.group(1) if m.group(1) else "P"
        src = m.group(2)
        dst = m.group(3)
        voice_mapping[norm] = {"piece": piece, "src": src, "dst": dst}
        save_mapping(voice_mapping)
        print(f"👌 Learned: {piece} {src} → {dst}\n")
    else:
        print("⚠️ Invalid correction format.\n")
