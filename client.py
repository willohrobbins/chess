import socket

def connect_to_server(server_ip, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((server_ip, port))
        return client_socket
    except ConnectionError:
        print("Unable to connect to the server.")
        return None

def send_move(client_socket, move):
    try:
        client_socket.sendall(move.encode())
    except BrokenPipeError:
        print("Lost connection to the server.")
        return False
    return True

def receive_game_state(client_socket):
    try:
        game_state = client_socket.recv(1024).decode()
        return game_state
    except ConnectionResetError:
        print("Lost connection to the server.")
        return None

def main():
    server_ip = '127.0.0.1'  # Replace with the server's IP address
    port = 8001  # The port number should match the server's port

    client_socket = connect_to_server(server_ip, port)
    if client_socket is None:
        return

    while True:
        # Display the current state of the game board
        game_state = receive_game_state(client_socket)
        if game_state is None:
            break
        print(game_state)

        # Get the player's move
        move = input("Enter your move: ")
        if not send_move(client_socket, move):
            break

    client_socket.close()

if __name__ == "__main__":

    main()
