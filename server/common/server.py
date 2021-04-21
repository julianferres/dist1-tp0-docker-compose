import socket
import logging
from multiprocessing import Process, Queue


class Server:
    def __init__(self, port, listen_backlog):
        # Initialize server socket
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.bind(('', port))
        self._server_socket.listen(listen_backlog)
        self.client_sock_queue = Queue()
        self.number_of_workers = 5 # serverWorkers pool amount

    def run(self):
        """
        Producer-Consumer server loop
        The server mantains a queue of accepted sockets and a pool
        of serverWorkers handles them as soon as they can
        """

        self.workers = [Process(target=self.__handle_client_connection, args=(id, self.client_sock_queue,))
                        for id in range(self.number_of_workers)]
        for w in self.workers:
            w.start()

        try:
            while True:
                client_sock = self.__accept_new_connection()
                self.client_sock_queue.put(client_sock) # Add to the queue
        except:
            print("Se termino el servicio")
        finally:
            # Gracefully join all workers and queue
            for worker in self.workers: 
                worker.join()
            self.client_sock_queue.close()


    def __handle_client_connection(self, id, queue):
        """
        Read message from a specific client socket and closes the socket

        If a problem arises in the communication with the client, the
        client socket will also be closed
        """
        while True:
            try:
                client_sock = queue.get() # Blocking if empty
                msg = client_sock.recv(1024).rstrip()
                logging.info(
                    'Message received from connection {}. Msg: {}'
                        .format(client_sock.getpeername(), msg))
                client_sock.send("Your Message has been received by worker {}: {}\n".format(id, msg).encode('utf-8'))
            except OSError:
                logging.info("Error while reading socket {}".format(client_sock))
            finally:
                client_sock.close()


    def __accept_new_connection(self):
        """
        Accept new connections

        Function blocks until a connection to a client is made.
        Then connection created is printed and returned
        """

        # Connection arrived
        logging.info("Proceed to accept new connections")
        c, addr = self._server_socket.accept()
        logging.info('Got connection from {}'.format(addr))
        return c