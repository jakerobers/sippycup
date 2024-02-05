from sippycup.sip_payload.sip_payload import SipPayload
from sippycup.utils import generate_hex_id_string, generate_branch_name

class TLSInvitePayload(SipPayload):
    def __init__(self, config):
        self.config = config

    def payload(self, args):
        client_ip = self.config['client_ip']
        proxy_host = self.config['proxy_host']
        proxy_port = self.config['proxy_port']
        from_display = self.config['from_display']
        from_uri = self.config['from_uri']
        userinfo = self.config['userinfo']

        to = args['to']
        digest = args['digest']
        reserved_port = args['reserved_port']
        c_seq = args['c_seq']

        branch = generate_branch_name()
        from_tag = generate_hex_id_string()
        call_id = generate_hex_id_string()

        sip_payload = [
            f'INVITE sip:{to} SIP/2.0',
            # ;alias: the server should add the connection to an indexed internal list.
            #         The idea is that this connection can be found again later,
            #         allowing the same connection to be re-used.
            # ;rport: the server should send the response back to the source port
            #         that the request came from. This is useful for NAT traversal.
            # ;branch: a unique identifier for this transaction. This is used to
            #         match responses to requests.
            # ;sent-by: If the host portion of the "sent-by" parameter contains a
            #         domain name, or if it contains an IP address that differs from
            #         the packet source address, the server MUST add a "received"
            #         parameter to that Via header field value. A port is optional.
            f'Via: SIP/2.0/TLS {client_ip}:{reserved_port};branch={branch};sent-by={client_ip}:{reserved_port};rport;alias',
            f'Route: <sip:{proxy_host}:{proxy_port};lr>',
            f'From: "{from_display}" <sip:{userinfo}@{from_uri}>;tag={from_tag}',
            f'To: <sip:{to}>',
            f'Call-ID: {call_id}@{from_uri}',
            f'CSeq: {c_seq} INVITE',
            f'Contact: <sip:{userinfo}@{client_ip}:{reserved_port}>;transport=tls',
            f'Max-Forwards: 70',
            f'User-Agent: TEST SCRIPT',
            f'Allow: INVITE, ACK, OPTIONS, CANCEL, BYE, SUBSCRIBE, NOTIFY, INFO, REFER, UPDATE, MESSAGE',
            # TODO: Figure out SDP payload
            # f'Content-Type: application/sdp',
            f'Content-Length: 0',
            f'',
            f''
        ]

        if digest:
            sip_payload.insert(8, f'Proxy-Authorization: {digest}')

        return "\r\n".join(sip_payload)

