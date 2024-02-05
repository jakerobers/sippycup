# Sippy Cup

An experimental and incomplete client for interacting with a sip server. The
motive for this project is to learn more about the sip protcol from the
ground-up -- implementing as I work through the RFC.

## Usage

Create a config file which will interact with your SIP proxy.

```
# config/testscript@myinstance123.json

{
  "from_display": "TEST SCRIPT",
  "from_uri": "myinstance123",
  "userinfo": "testscript",
  "password": "mysecretpassword",
  "client_ip": "10.10.10.17",
  "proxy_host": "myinstance123.some-pbx.net",
  "proxy_port": "5061",
  "transport": "tls"
}
```

Then you can run it with:

```
./sc --config ./config/testscript@myinstance123.json 'r;i=deskphone@myinstance123.some-pbx.net'
```

## Development

```
poetry run black .
poetry run flake8
```

