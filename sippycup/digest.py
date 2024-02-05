import hashlib


# Resources:
# - RFC for Sip-specific digest auth: https://datatracker.ietf.org/doc/html/rfc8760
# - Digest auth: https://en.wikipedia.org/wiki/Digest_access_authentication
class Digest:
    @staticmethod
    def generate_auth_header(username, password, realm, nonce, method, uri):
        ha1_payload = f"{username}:{realm}:{password}"
        ha1 = hashlib.md5(ha1_payload.encode())
        ha1_digest = ha1.hexdigest()
        # uri appears to be the "To" recipient
        ha2 = hashlib.md5(f"{method}:{uri}".encode())
        ha2_digest = ha2.hexdigest()
        response = hashlib.md5(f"{ha1_digest}:{nonce}:{ha2_digest}".encode())
        return f'Digest username="{username}", realm="{realm}", nonce="{nonce}", uri="{uri}", response="{response.hexdigest()}"'
