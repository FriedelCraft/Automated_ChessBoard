import pygame
import chess
import chess.engine
import sounddevice as sd
import numpy as np
import whisper
import re
import json
import os

# === VOICE MODEL ===
print("🧠 Loading Whisper (small.en)...")
model = whisper.load_model("small.en")

SAMPLERATE = 16000
DURATION = 3
MAPPING_FILE = "voice_mapping.json"

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
print(f"🔁 Loaded {len(voice_mapping)} learned speech commands.\n")

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

def parse_move(text):
    text = text.lower()

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

    piece = detect_piece(text)
    coords = re.findall(r"[a-h][1-8]", text)

    if len(coords) == 2:
        return piece, coords[0], coords[1]
    return None, None, None


# === CHESS ENGINE + BOARD ===
board = chess.Board()
engine = chess.engine.SimpleEngine.popen_uci("/usr/games/stockfish")

pygame.init()
WIDTH = HEIGHT = 640
SQ_SIZE = WIDTH // 8
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Voice-Controlled Chess")

IMAGES = {}
piecefiles = os.listdir("images")
for file in piecefiles:
    name = file.split(".")[0]
    IMAGES[name] = pygame.transform.scale(
        pygame.image.load("images/" + file),
        (SQ_SIZE, SQ_SIZE)
    )

def draw_board():
    colors = [pygame.Color("white"), pygame.Color("gray")]
    for r in range(8):
        for c in range(8):
            pygame.draw.rect(SCREEN, colors[(r+c) % 2], pygame.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def draw_pieces():
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            r = 7 - (square // 8)
            c = square % 8
            color = 'w' if piece.color else 'b'
            key = color + piece.symbol().lower()
            SCREEN.blit(IMAGES[key], pygame.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def make_user_move(piece, src, dst):
    move = chess.Move.from_uci(src+dst)
    if move in board.legal_moves:
        board.push(move)
        print(f"🎯 You: {piece} {src} → {dst}")
        return True
    print("❌ Illegal move")
    return False

def ai_move():
    result = engine.play(board, chess.engine.Limit(time=0.5))
    board.push(result.move)
    print(f"🤖 AI: {result.move}")

def listen_and_interpret():
    print("\n🎤 Speak your move...")
    audio = sd.rec(int(SAMPLERATE * DURATION), samplerate=SAMPLERATE, channels=1)
    sd.wait()

    audio = np.squeeze(audio)
    result = model.transcribe(audio, language="en")
    text = result["text"].strip().lower()

    print(f"Heard: {text}")

    if text in voice_mapping:
        move = voice_mapping[text]
        return move["piece"], move["src"], move["dst"]

    piece, src, dst = parse_move(text)
    if piece and src and dst:
        return piece, src, dst

    print("😅 Say it again")
    return None, None, None

# === GAME LOOP ===
running = True
while running and not board.is_game_over():
    draw_board()
    draw_pieces()
    pygame.display.flip()

    piece, src, dst = listen_and_interpret()
    if piece and src and dst:
        if make_user_move(piece, src, dst):
            ai_move()

print("🏁 Game Over:", board.result())
engine.quit()
pygame.quit()
