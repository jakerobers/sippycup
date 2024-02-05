import random

MAGIC_COOKIE = "z9hG4bK"

def generate_id():
    return random.randrange(0, 1000000000)

def generate_hex_id_string():
    hex_string = hex(generate_id())
    return hex_string[2:]

def generate_branch_name():
    return f'{MAGIC_COOKIE}{generate_id()}'

def read_response(sock):
    return sock.recv(1024)

