import socket
import threading
import secrets
import el_gamal
import RSA

class ChatServer:
    def __init__(self):
        self.HOST = None
        self.PORT = None
        self.LISTENER_LIMIT = 5
        self.active_clients = []
        self.ElgamalKey = None
        self.flagmethod = None

    def choose_method(self):
        """Function to choose encryption method"""
        encryption_methods = ["DES", "ELGAMAL", "RSA"]
        print("---------Welcome to our secure chat")
        print("1- DES (Data encryption standard)")
        print("2- ElGamal encryption system")
        print("3- RSA (Rivest–Shamir–Adleman)")

        while True:
            try:
                num = int(input("Choose the encryption system (1-3): "))
                if 1 <= num <= 3:
                    print(f"{encryption_methods[num-1]} mode has been started")
                    return str(num)
            except ValueError:
                pass
            print("Please enter a valid number (1-3)")

    def send_message_to_client(self, client, message):
        """Send message to a single client"""
        try:
            client.sendall(message.encode())
            print("SEND:", message)
        except Exception as e:
            print(f"Error sending message: {e}")
            self.remove_client(client)

    def send_messages_to_all(self, message):
        """Send message to all connected clients"""
        disconnected_clients = []
        for client_info in self.active_clients:
            try:
                self.send_message_to_client(client_info[1], message)
            except:
                disconnected_clients.append(client_info)

        # Remove disconnected clients
        for client_info in disconnected_clients:
            self.active_clients.remove(client_info)

    def remove_client(self, client):
        """Remove client from active clients list"""
        for client_info in self.active_clients:
            if client_info[1] == client:
                self.active_clients.remove(client_info)
                break

    def listen_for_messages(self, client, username, key, elgamal_public_key, rsa_string):
        """Listen for upcoming messages from a client"""
        while True:
            try:
                message = client.recv(2048).decode('utf-8')
                if message:
                    final_msg = f"{username}~{message}~{key}~{self.flagmethod}~{elgamal_public_key}~{rsa_string}"
                    self.send_messages_to_all(final_msg)
                else:
                    print(f"Empty message from client {username}")
                    break
            except:
                print(f"Error receiving message from {username}")
                self.remove_client(client)
                break

    def client_handler(self, client, key):
        """Handle individual client connections"""
        try:
            username = client.recv(2048).decode('utf-8')
            if username:
                # Generate keys and parameters
                key = secrets.token_hex(8).upper()
                n, E, D = RSA.calc()
                rsa_string = f"{n},{E},{D},"

                elgamal_public_key = ",".join(str(x) for x in self.ElgamalKey)

                # Add client to active clients
                self.active_clients.append((username, client, key))

                # Send welcome message
                prompt_message = f"SERVER~{username} added to the chat~{key}~{self.flagmethod}~{elgamal_public_key}~{rsa_string}"
                self.send_messages_to_all(prompt_message)

                print(f"Session key successfully generated for {username} ==> {key}")

                # Start listening for messages
                threading.Thread(target=self.listen_for_messages,
                               args=(client, username, key, elgamal_public_key, rsa_string)).start()
            else:
                print("Empty username received")
                client.close()
        except Exception as e:
            print(f"Error handling client: {e}")
            client.close()

    def start_server(self):
        """Start the chat server"""
        # Get host and port from the user
        self.HOST = input("Enter the server host (e.g., 192.168.1.8 or localhost): ")
        self.PORT = int(input("Enter the server port (e.g., 1234): "))

        # Generate ElGamal keys
        self.ElgamalKey = el_gamal.generate_public_key()

        # Choose encryption method
        self.flagmethod = self.choose_method()

        # Create server socket
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            # Bind the server to the host and port
            server.bind((self.HOST, self.PORT))
            print(f"Running the server on {self.HOST}:{self.PORT}")
            server.listen(self.LISTENER_LIMIT)

            while True:
                # Accept new client connections
                client, address = server.accept()
                print(f"Successfully connected to client {address[0]}:{address[1]}")
                threading.Thread(target=self.client_handler, args=(client, "")).start()

        except Exception as e:
            print(f"Error starting server: {e}")
        finally:
            if server:
                server.close()

def main():
    server = ChatServer()
    server.start_server()

if __name__ == '__main__':
    main()