from sippycup.sip_payload.sip_payload import SipPayload
from sippycup.utils import generate_hex_id_string, generate_branch_name

class TLSRegisterPayload(SipPayload):
    def __init__(self, config):
        self.config = config

    def payload(self, args):
        reserved_port = args['reserved_port']
        c_seq = args['c_seq']
        digest = args['digest']

        from_display = self.config['from_display']
        from_uri = self.config['from_uri']
        userinfo = self.config['userinfo']
        client_ip = self.config['client_ip']
        proxy_host = self.config['proxy_host']
        proxy_port = self.config['proxy_port']

        call_id = generate_hex_id_string()
        branch = generate_branch_name()
        from_tag = generate_hex_id_string()

        sip_payload = [
            # TODO: Do we need the port included after from_uri on this REGISTER
            f'REGISTER sip:{from_uri} SIP/2.0',
            f'Via: SIP/2.0/TLS {client_ip}:{reserved_port};branch={branch};sent-by={client_ip}:{reserved_port};rport;alias',
            f'Route: <sip:{proxy_host}:{proxy_port};lr>', # lr="loose routing"
            f'From: "{from_display}" <sip:{userinfo}@{from_uri}>;tag={from_tag}',
            # The To header field contains the address of record whose registration
            # is to be created, queried, or modified.  The To header field and the
            # Request-URI field typically differ, as the former contains a user
            # name.  This address-of-record MUST be a SIP URI or SIPS URI.
            f'To: <sip:{userinfo}@{from_uri}>',
            f'Call-ID: {call_id}@{from_uri}',
            f'CSeq: {c_seq} REGISTER', # TODO: actually increment these
            f'Contact: <sip:{userinfo}@{client_ip}:{reserved_port}>;transport=tls',
            # TODO: Do we need Proxy-Authorization?
            f'Max-Forwards: 70',
            f'User-Agent: TEST SCRIPT',
            f'Allow: INVITE, ACK, OPTIONS, CANCEL, BYE, SUBSCRIBE, NOTIFY, INFO, REFER, UPDATE, MESSAGE',
            f'Content-Length: 0',
            f'',
            f''
        ]

        if digest:
            sip_payload.insert(8, f'Proxy-Authorization: {digest}')

        return "\r\n".join(sip_payload)

