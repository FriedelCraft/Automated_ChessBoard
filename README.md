# 🤖 Automated Voice-Controlled Chess Board

A Raspberry Pi powered smart chessboard that allows players to speak their chess moves.  
The system interprets voice commands using Whisper AI, validates moves using Stockfish,
and visually simulates the game using Pygame.

Future versions include controlling real chess pieces with an XY gantry and magnets.

---

## ✨ Features
- 🎤 Voice-controlled chess moves (Whisper AI)
- ♟️ Real-time chessboard GUI (Pygame)
- 🤖 Stockfish AI opponent
- 🧠 Reinforcement learning (adapts to your voice)
- ✓ Chess legality check with python-chess

---

## 🛠 Requirements
- Python 3.8+
- Raspberry Pi / Linux / Windows

### 🧩 Python Dependencies
```bash
pip3 install pygame python-chess sounddevice numpy whisper
pip3 install torch --extra-index-url https://download.pytorch.org/whl/cpu
```

### 🔊 Audio Libraries (Linux / Raspberry Pi)
```bash
sudo apt install -y portaudio19-dev libasound2 libasound-dev
```

### ♟️ Install Stockfish
```bash
sudo apt update
sudo apt install -y stockfish
```

Verify installation:
```bash
which stockfish
```
Expected output:
```bash
/usr/games/stockfish
```

---

## 📁 Assets Required
'images' folder contains the piece images:

| File | Description |
|------|-------------|
| wp.png | White Pawn |
| bp.png | Black Pawn |
| wn.png | White Knight |
| bn.png | Black Knight |
| wb.png | White Bishop |
| bb.png | Black Bishop |
| wr.png | White Rook |
| br.png | Black Rook |
| wq.png | White Queen |
| bq.png | Black Queen |
| wk.png | White King |
| bk.png | Black King |

---

## ▶️ Run the Main Application
```bash
python3 voice_chess_pygame.py
```

Then speak moves like:
```bash
"pawn e2 to e4"
"knight g1 to f3"
```

---
## ▶️ Training Voice Model
To train the voice model, run the voice_chess_rl.py:
```bash
python3 voice_chess_rl.py
```
This python script ask you everytime if the command guessed by the model is correct or not, if not type n and give the correct command. then it stores it in voice_mapping.json file. I have already trained with a very few commmands.

---

## 🧠 How It Works
| Module | Purpose |
|--------|---------|
| Whisper AI | Converts speech → text |
| Reinforcement Learning | Learns & corrects your accent over time |
| python-chess | Validates moves, board logic |
| Stockfish | Opponent AI |
| pygame | Renders graphical chessboard |

---

## 🚧 Future Development
- 🔗 Arduino movement control
- 🧲 magnets + XY gantry to move real pieces
- 📡 Wireless input
- 🗣 AI move narration
- 📺 LCD screen to show your moves

---


