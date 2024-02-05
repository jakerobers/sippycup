class UDPInstructionsRunner:
    def __init__(self, config, sock):
        self.config = config
        self.sock = sock

    # Register command
    def r(self, args):
        reserved_port = self.sock.getsockname()[1]
        stream = tls_register_payload(reserved_port, self.config)
        encoded_stream = stream.encode()
        self.sock.sendto(encoded_stream, self.get_destination_address())
        response = read_response(self.sock)

    # Options request to recipient
    def o(self, args):
        reserved_port = self.sock.getsockname()[1]
        stream = tls_options_payload(reserved_port, self.config, args[0])
        encoded_stream = stream.encode()
        self.sock.sendto(encoded_stream, self.get_destination_address())
        response = read_response(self.sock)

    # Invites recipient
    def i(self, args):
        stream = tls_invite_payload(reserved_port, config)
        encoded_stream = stream.encode()
        self.sock.sendto(encoded_stream, self.get_destination_address())
        response = read_response(self.sock)

    # Accepts invitation from inviter
    def ai(self, args):
        raise NotImplementedError

    # Declines invitation from inviter
    def di(self, args):
        raise NotImplementedError

    def get_destination_address(self):
        return (
            self.config['proxy_host'],
            int(self.config['proxy_port'])
        )

