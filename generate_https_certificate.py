import os
import subprocess

config_content = """
[ req ]
distinguished_name = req_distinguished_name
prompt = no

[ req_distinguished_name ]
CN = localhost
"""

DIR = "https"
os.makedirs(DIR, exist_ok=True)

CONFIG_PATH = os.path.join(DIR, "openssl.cnf")
CERTIFICATE_PATH = os.path.join(DIR, "certificate.pem")
KEY_PATH = os.path.join(DIR, "key.pem")

with open(CONFIG_PATH, "w") as f:
    f.write(config_content.strip())

cmd = [
    "openssl", "req", "-x509", "-newkey", "rsa:4096",
    "-keyout", KEY_PATH, "-out", CERTIFICATE_PATH,
    "-days", "365", "-nodes", "-config", CONFIG_PATH
]

try:
    subprocess.run(cmd, check=True)
    print(f"Certificate and key generated: {CERTIFICATE_PATH}, {KEY_PATH}")
except subprocess.CalledProcessError as e:
    print("OpenSSL command failed:", e)
