import socket
import threading
import chess
print(chess.__file__)

def client_thread(conn, player, opponent_conn):
    while True:
        try:
            # Receive a move from the player
            move = conn.recv(1024).decode()
            if not move:
                break

            # Update the board with the received move
            try:
                board.push(chess.Move.from_uci(move))
            except ValueError:
                continue  # Invalid move received, skip it

            # Send the updated game state to both players
            game_state = board.fen()
            conn.sendall(game_state.encode())
            opponent_conn.sendall(game_state.encode())

        except ConnectionError:
            break

    conn.close()

# Initialize the game board
board = chess.Board()

# Set up the server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 8001))  # Bind to your public IP and port
server.listen(2)

print("Server started. Waiting for connections...")

player1_conn, _ = server.accept()
print("Player 1 connected.")

player2_conn, _ = server.accept()
print("Player 2 connected.")

# Start a thread for each player
threading.Thread(target=client_thread, args=(player1_conn, "White", player2_conn)).start()
threading.Thread(target=client_thread, args=(player2_conn, "Black", player1_conn)).start()