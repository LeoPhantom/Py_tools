Basic TCP Server in Python
This repository contains a simple, multi-threaded TCP server written in Python. It listens for incoming client connections, receives messages, echoes them back to the client, and handles multiple clients concurrently.

Features
Multi-threaded: Each new client connection is handled in a separate thread, allowing the server to manage multiple active clients simultaneously without blocking.

Echo Functionality: The server receives messages from clients and sends back a confirmation message.

Basic Error Handling: Includes error handling for common network issues like "Address already in use" or "Permission denied" during server startup, and connection resets during client communication.

Connection Logging: Prints connection status and received messages to the console.

How to Run the Server
Save the Code:
Save the provided Python code into a file named tcp_server.py.

Open Your Terminal:
Navigate to the directory where you saved tcp_server.py using your preferred terminal (Command Prompt, PowerShell, Git Bash, or WSL terminal).

Execute the Server:
Run the server using the Python interpreter:

python tcp_server.py

You should see output indicating the server has started and is listening on 0.0.0.0:65432:

[SERVER STARTING] Listening on 0.0.0.0:65432

The server will now be running and waiting for incoming client connections.

How to Test the Server
You can test the server using a simple network utility like netcat (or nc) or a basic Python client.

Option 1: Using netcat (Recommended for Quick Tests)
Open a new terminal window (do not close the server's terminal) and run the appropriate command for your operating system:

On Linux / WSL / macOS:

nc 127.0.0.1 65432

On Windows (if nc or ncat from Nmap is installed):

nc 127.0.0.1 65432

Once connected, type a message and press Enter. You should see your message appear in the server's terminal, and the server's response will be displayed in your client terminal.

Option 2: Using a Simple Python TCP Client
Create a new file named tcp_client.py with the following content:

import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    try:
        client_socket.connect((HOST, PORT))
        print(f"Connected to {HOST}:{PORT}")

        while True:
            message = input("Enter message (or 'exit' to quit): ")
            if message.lower() == 'exit':
                break

            client_socket.sendall(message.encode('utf-8'))
            data = client_socket.recv(1024)
            print(f"Received from server: {data.decode('utf-8')}")

    except ConnectionRefusedError:
        print(f"Error: Connection refused. Is the server running on {HOST}:{PORT}?")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client_socket.close()
        print("Client disconnected.")

Save tcp_client.py and run it in a new terminal window:

python tcp_client.py

You can then type messages in the client terminal, and observe the interaction between the client and server.
