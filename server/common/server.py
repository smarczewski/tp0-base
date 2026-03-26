from time import sleep

from .comms import read_bet, send_ack
from .utils import store_bets
import socket
import logging


class Server:
    def __init__(self, port, listen_backlog):
        # Initialize server socket
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.bind(("", port))
        self._server_socket.listen(listen_backlog)
        self.client_sock_arr: list[socket.socket] = []
        self.running = False

    def run(self):
        """
        Dummy Server loop

        Server that accept a new connections and establishes a
        communication with a client. After client with communucation
        finishes, servers starts to accept new connections again
        """

        self.running = True
        while self.running:
            try:
                client_sock = self.__accept_new_connection()
                self.client_sock_arr.append(client_sock)
                self.__handle_client_connection(client_sock)
            except OSError as e:
                if self.running:
                    logging.error(
                        f"action: accept_connections | result: fail | err: {e}"
                    )

    def shutdown(self, signum=None, frame=None):
        self.running = False

        if self._server_socket:
            self._server_socket.close()

        if self.client_sock_arr:
            for client_sock in self.client_sock_arr:
                client_sock.close()

        logging.info("action: exit | result: success")

    def __handle_client_connection(self, client_sock: socket.socket):
        """
        Read bet from a specific client socket and closes the socket

        If a problem arises in the communication with the client, the
        client socket will also be closed
        """
        try:
            file = client_sock.makefile()
            bet = read_bet(file)
            store_bets([bet])
            logging.info(
                f"action: apuesta_almacenada | result: success | dni: ${bet.document} | numero: ${bet.number}"
            )
            send_ack(client_sock, bet.document, bet.number)
        except Exception as e:
            logging.error(f"action: apuesta_almacenada | result: fail | error: {e}")
        finally:
            file.close()
            client_sock.close()
            try:
                self.client_sock_arr.remove(client_sock)
            except ValueError:
                pass

    def __accept_new_connection(self):
        """
        Accept new connections

        Function blocks until a connection to a client is made.
        Then connection created is printed and returned
        """

        # Connection arrived
        logging.info("action: accept_connections | result: in_progress")
        c, addr = self._server_socket.accept()
        logging.info(f"action: accept_connections | result: success | ip: {addr[0]}")
        return c
