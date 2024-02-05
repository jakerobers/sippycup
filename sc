#!/usr/bin/env python
#
# COMMANDS
# r; registers current config to proxy
# o=101@some-pbx.org; fetches options of 101@some-pbx.org
# i=101@some-pbx.org; invites 101@some-pbx.org
# ai; accepts invite from inviter
# di; declines invite from inviter
#
# Useful resources
# Session initiation protocol: https://datatracker.ietf.org/doc/html/rfc3261

import ssl
import logging
import argparse
import json
import sys
import socket

from sippycup.digest import Digest
from sippycup.instructions_runner.tls_instructions_runner import TLSInstructionsRunner

def main():
    parser = argparse.ArgumentParser(prog='Call', description='SIP communication program')
    parser.add_argument('-c', '--config')
    parser.add_argument('instructions', help='What the SIP device should do', nargs=1)
    args = parser.parse_args()

    fd = open(args.config, 'r')
    config = json.loads(fd.read())
    fd.close()

    sock = None
    if config['transport'] == 'tls':
        tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock = ssl.wrap_socket(tcp_sock, ssl_version=ssl.PROTOCOL_TLSv1_2)
        sock.connect((config['proxy_host'], int(config['proxy_port'])))

        instructions_runner = TLSInstructionsRunner(config, sock)
    else:
        # AF_INET = IPv4; SOCK_DGRAM = UDP
        # SOCK_DGRAM matches the transport protocol in the Contact header
        # sendto used for UDP.
        # Instead establish conn via listen()/accept() if TCP is needed.
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('', 0))
        instructions_runner = UDPInstructionsRunner(config, sock)

    split_ins = args.instructions[0].split(';')
    for ins in split_ins:
        ins = ins.strip()
        args_split = ins.split("=")
        if len(args_split) > 1:
            instructions_runner.__getattribute__(args_split[0])(args_split[1])
        else:
            instructions_runner.__getattribute__(args_split[0])(None)

    sock.close()

if __name__ == '__main__':
    main()
