from sippycup.sip_payload.sip_payload import SipPayload

class UDPOptionsPayload(SipPayload):
    def __init__(self, config):
        self.config = config

    def payload(self, args):
        reserved_port = args['reserved_port']
        from_display = self.config['from_display']
        from_uri = self.config['from_uri']
        userinfo = self.config['userinfo']
        client_ip = self.config['client_ip']
        proxy_host = self.config['proxy_host']
        proxy_port = self.config['proxy_port']

        branch = generate_branch_name()
        from_tag = generate_hex_id_string()
        call_id = generate_hex_id_string()

        sip_payload = [
            f'OPTIONS sip:{proxy_host}:{proxy_port} SIP/2.0',
            f'Via: SIP/2.0/UDP {client_ip}:{reserved_port};branch={branch};sent-by={client_ip}:{reserved_port};rport;alias',
            f'Max-Forwards: 70',
            f'From: "{from_display}" <sip:{userinfo}@{from_uri}>;tag={from_tag}',
            f'To: <sip:{to}>',
            f'Call-ID: {call_id}@{from_uri}',
            f'CSeq: 6 OPTIONS',
            f'Contact: <sip:{userinfo}@{client_ip}:{reserved_port}>;transport=udp',
            f'Content-Length: 0',
            f'',
            f''
        ]

        return "\r\n".join(sip_payload)

