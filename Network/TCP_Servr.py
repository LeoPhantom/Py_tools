import socket
import threading
import sys

HOST = '0.0.0.0'
PORT = 65432

def handle_client(conn, addr):
    print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
    print(f"[NEW CONNECTION] {addr} connected.")

    try:
        while True:
            data = conn.recv(1024)
            if not data:
                print(f"[DISCONNECTED] {addr} disconnected.")
                break

            message = data.decode('utf-8')
            print(f"[{addr}] received: {message}")

            response_message = f"Server received your message: '{message}'"
            
            conn.sendall(response_message.encode('utf-8'))

    except ConnectionResetError:
        print(f"[CONNECTION RESET] {addr} forcibly disconnected.")
    except Exception as e:
        print(f"[ERROR] Error handling client {addr}: {e}")
    finally:
        conn.close()
        print(f"[CONNECTION CLOSED] {addr} socket closed.")

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server_socket.bind((HOST, PORT))
        print(f"[SERVER STARTING] Listening on {HOST}:{PORT}")

        server_socket.listen(5)

        while True:
            conn, addr = server_socket.accept()
            
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()
            
    except OSError as e:
        if e.errno == 98:
            print(f"[ERROR] Port {PORT} is already in use. Please choose another port or wait.")
        elif e.errno == 13:
            print(f"[ERROR] Permission denied. You might need to run as administrator/root for this port, or use a port > 1023.")
        else:
            print(f"[ERROR] OS Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"[FATAL ERROR] Server crashed: {e}")
        sys.exit(1)
    finally:
        server_socket.close()
        print("[SERVER SHUTDOWN] Server socket closed.")

if __name__ == "__main__":
    start_server()
