class ResponseParser():
    def parse(self, response):
        response_lines = response.decode().split("\r\n")
        response_lines = response_lines[:-2]
        response_lines = [line.split(": ") for line in response_lines]

        # pop first element off
        title = response_lines.pop(0)
        title = title[0]
        protocol_ver = ""

        # pop the protocol version
        while title[0] != " ":
            protocol_ver += title[0]
            title = title[1:]

        # pop the space
        title = title[1:]

        # pop the status code
        status_code = ""
        while title[0] != " ":
            status_code += title[0]
            title = title[1:]

        message = title[1:]

        headers = {}
        for line in response_lines:
            if line[0] == "Proxy-Authenticate":
                value = line[1]
                auth_type = ""
                while value[0] != " ":
                    auth_type += value[0]
                    value = value[1:]

                value = value[1:]
                value = value.split(", ")
                realm = ""
                nonce = ""
                for v in value:
                    key, val = v.split("=")
                    if key == "realm":
                        realm = val[1:-1]
                    elif key == "nonce":
                        nonce = val[1:-1]

                headers["Proxy-Authenticate"] = {
                    "type": auth_type,
                    "realm": realm,
                    "nonce": nonce
                }
            elif line[0] == "Via":
                headers["Via"] = line[1]
            elif line[0] == "From":
                headers["From"] = line[1]
            elif line[0] == "To":
                headers["To"] = line[1]
            elif line[0] == "Call-ID":
                headers["Call-ID"] = line[1]
            elif line[0] == "CSeq":
                value = line[1].split(" ")
                seq_num = int(value[0])
                method = value[1]

                headers["CSeq"] = {
                    "seq_num": seq_num,
                    "method": method
                }
            elif line[0] == "Contact":
                headers["Contact"] = line[1]
            elif line[0] == "Content-Length":
                headers["Content-Length"] = int(line[1])

        return {
            "protocol_ver": protocol_ver,
            "status_code": int(status_code),
            "message": message,
            "headers": headers
        }

