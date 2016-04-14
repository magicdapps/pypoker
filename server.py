from poker import ServerSocket
import logging
import os


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG if 'DEBUG' in os.environ else logging.INFO)
    logger = logging.getLogger()

    host = "localhost" if "POKER5_HOST" not in os.environ else os.environ["POKER5_HOST"]
    port = 9000 if "POKER5_PORT" not in os.environ else os.environ["POKER5_PORT"]
    server_address = (host, port)

    server = ServerSocket(server_address, logger=logger)
    server.start()
