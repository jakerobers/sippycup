from sippycup.sip_payload.tls_invite_payload import TLSInvitePayload
from sippycup.sip_payload.tls_register_payload import TLSRegisterPayload
from sippycup.utils import read_response
from sippycup.response_parser import ResponseParser
from sippycup.digest import Digest

class TLSInstructionsRunner:
    def __init__(self, config, sock):
        self.config = config
        self.tls_register_payload = TLSRegisterPayload(config)
        self.tls_invite_payload = TLSInvitePayload(config)
        self.sock = sock

    # Register command
    def r(self, args):
        reserved_port = self.sock.getsockname()[1]
        args = {'reserved_port': reserved_port, 'c_seq': 2016, 'digest': None}
        stream = self.tls_register_payload.payload(args)
        encoded_stream = stream.encode()
        self.sock.send(encoded_stream)
        response = read_response(self.sock)
        response = ResponseParser().parse(response)

        # Assumes a 407 is returned. must follow up with another REGISTER
        assert response['status_code'] == 407

        proxy_auth = response['headers']['Proxy-Authenticate']
        auth_digest = Digest.generate_auth_header(
            self.config['userinfo'],
            self.config['password'],
            proxy_auth['realm'],
            proxy_auth['nonce'],
            'REGISTER',
            f'sip:{self.config["from_uri"]}'
        )
        args['digest'] = auth_digest

        args['c_seq'] = args['c_seq'] + 1
        stream = self.tls_register_payload.payload(args)
        encoded_stream = stream.encode()
        self.sock.send(encoded_stream)
        response = read_response(self.sock)

        print("REGISTERED")

        return response

    # Options request to recipient
    def o(self, args):
        raise NotImplementedError

    # Invites recipient
    def i(self, to):
        reserved_port = self.sock.getsockname()[1]
        args = {'reserved_port': reserved_port, 'c_seq': 2016, 'digest': None, 'to': to}
        stream = self.tls_invite_payload.payload(args)
        print(stream)
        encoded_stream = stream.encode()
        self.sock.send(encoded_stream)
        response = read_response(self.sock)
        response = ResponseParser().parse(response)
        print(response)

        # Assumes a 407 is returned. must follow up with another INVITE
        assert response['status_code'] == 407
        proxy_auth = response['headers']['Proxy-Authenticate']
        auth_digest = Digest.generate_auth_header(
            self.config['userinfo'],
            self.config['password'],
            proxy_auth['realm'],
            proxy_auth['nonce'],
            'REGISTER',
            f'sip:{to}'
        )
        args['digest'] = auth_digest

        args['c_seq'] = args['c_seq'] + 1
        stream = self.tls_invite_payload.payload(args)
        print(stream)
        encoded_stream = stream.encode()
        self.sock.send(encoded_stream)
        response = read_response(self.sock)
        response = ResponseParser().parse(response)

        print(response)
        return response

    # Accepts invitation from inviter
    def ai(self, args):
        raise NotImplementedError

    # Declines invitation from inviter
    def di(self, args):
        raise NotImplementedError

