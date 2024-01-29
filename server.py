import socket
import threading
import chess

def client_thread(conn, player, opponent_conn, board_lock):
    global board, current_turn

    while True:
        try:
            # Only allow the player whose turn it is to make a move
            with board_lock:
                if board.turn != player:
                    continue

            # Receive a move from the player
            move = conn.recv(1024).decode()
            if not move:
                break

            # Update the board with the received move
            try:
                with board_lock:
                    board.push(chess.Move.from_uci(move))
                    current_turn = chess.BLACK if current_turn == chess.WHITE else chess.WHITE
            except ValueError:
                continue  # Invalid move received, skip it

            # Send the updated game state to both players
            game_state = board.fen()
            conn.sendall(game_state.encode())
            opponent_conn.sendall(game_state.encode())

        except ConnectionError:
            break

    conn.close()

# Initialize the game board and current turn
board = chess.Board()
current_turn = chess.WHITE  # White starts
board_lock = threading.Lock()

# Set up the server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 8001))  # Bind to your local IP and port
server.listen(2)

print("Server started. Waiting for connections...")

player1_conn, _ = server.accept()
print("Player 1 (White) connected.")

player2_conn, _ = server.accept()
print("Player 2 (Black) connected.")

# Start a thread for each player
threading.Thread(target=client_thread, args=(player1_conn, chess.WHITE, player2_conn, board_lock)).start()
threading.Thread(target=client_thread, args=(player2_conn, chess.BLACK, player1_conn, board_lock)).start()
