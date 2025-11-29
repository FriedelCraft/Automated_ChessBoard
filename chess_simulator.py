import pygame
import chess
import chess.engine

# === Setup ===
pygame.init()
WIDTH = HEIGHT = 640
SQ_SIZE = WIDTH // 8
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Voice Chess Board")

# Load engine
engine = chess.engine.SimpleEngine.popen_uci("/usr/games/stockfish")

# Load piece images
IMAGES = {}
pieces = ["wp","bp","wn","bn","wb","bb","wr","br","wq","bq","wk","bk"]
for piece in pieces:
    IMAGES[piece] = pygame.transform.scale(
        pygame.image.load(f"/home/friedelcraft/Documents/Chessbot/images/{piece}.png"), 
        (SQ_SIZE,SQ_SIZE)
    )

board = chess.Board()

piece_map = {
    "P": chess.PAWN, "N": chess.KNIGHT, "B": chess.BISHOP,
    "R": chess.ROOK, "Q": chess.QUEEN, "K": chess.KING
}

def draw_board():
    colors = [pygame.Color("white"), pygame.Color("gray")]
    for r in range(8):
        for c in range(8):
            color = colors[(r+c) % 2]
            pygame.draw.rect(SCREEN, color, pygame.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def draw_pieces():
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            r = 7 - (square // 8)
            c = square % 8
            color = 'w' if piece.color else 'b'
            key = color + piece.symbol().lower()
            img = IMAGES[key]
            SCREEN.blit(img, pygame.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def make_user_move(move_str):
    parts = move_str.split()
    if len(parts) != 3:
        print("Format: P e2 e4")
        return False

    piece, src, dst = parts[0].upper(), parts[1], parts[2]

    move = chess.Move.from_uci(src+dst)

    if move not in board.legal_moves:
        print("Illegal move!")
        return False
    
    s = chess.parse_square(src)
    piece_at_src = board.piece_at(s)
    if not piece_at_src or piece_at_src.piece_type != piece_map[piece]:
        print("Wrong piece at source!")
        return False

    board.push(move)
    print(f"You: {piece} {src}->{dst}")
    return True

def make_ai_move():
    result = engine.play(board, chess.engine.Limit(time=0.5))
    board.push(result.move)
    print(f"AI: {result.move}")
    return result.move

# === MAIN LOOP ===
running = True
print(board)

while running and not board.is_game_over():
    draw_board()
    draw_pieces()
    pygame.display.flip()

    user_input = input("\nYour move (P e2 e4): ")

    if make_user_move(user_input):
        make_ai_move()

print("\nGame Over:", board.result())
engine.quit()
pygame.quit()
