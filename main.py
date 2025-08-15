import configparser
import os
import subprocess

import uvicorn
from fastapi import FastAPI


def parse_conf(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)

    result = {
        "secretKey": "",
        "address": [],
        "publicKey": "",
        "allowedIps": [],
        "endpoint": "",
        "dns": [],
        "mtu": "",
    }

    if "Interface" in config:
        interface = config["Interface"]
        result["secretKey"] = interface.get("PrivateKey", "")
        addresses = interface.get("Address", "")
        result["address"] = [addr.strip() for addr in addresses.split(",") if addr.strip()]
        dns_list = interface.get("DNS", "")
        result["dns"] = [dns.strip() for dns in dns_list.split(",") if dns.strip()]
        result["mtu"] = interface.get("MTU", "")

    if "Peer" in config:
        peer = config["Peer"]
        result["publicKey"] = peer.get("PublicKey", "")
        allowed_ips = peer.get("AllowedIPs", "")
        result["allowedIps"] = [ip.strip() for ip in allowed_ips.split(",") if ip.strip()]
        result["endpoint"] = peer.get("Endpoint", "")

    return result


app = FastAPI()


@app.get("/generate")
def register():
    flag = True
    while flag:
        result = subprocess.run(
            ["./wgcf", "register", "--accept-tos"],
            capture_output=True,
            text=True,
            cwd="/app/assets"
        )
        print(result.stderr)
        if "500 Internal Server Error" not in result.stderr:
            flag = False  # دیگه تکرار نمی‌کنه

    # حالا generate
    subprocess.run(
        ["./wgcf", "generate"],
        capture_output=True,
        text=True,
        cwd="/app/assets"
    )

    config = parse_conf("/app/assets/wgcf-profile.conf")

    os.remove("/app/assets/wgcf-account.toml")
    os.remove("/app/assets/wgcf-profile.conf")

    return config


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
