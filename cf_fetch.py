import hashlib, json, sys, time, urllib.request
API = "https://api.uouin.com/index.php/index/Cloudflare"
SALT_A = "DdlTxtN0sUOu"
SALT_B = "70cloudflareapikey"
LINE_NAME = {"bgp":"CF BGP优选","ctcc":"CF 电信优选","cmcc":"CF 移动优选","cucc":"CF 联通优选","ipv6":"CF IPv6优选"}
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
def make_key(ts):
    return hashlib.md5((hashlib.md5(SALT_A.encode()).hexdigest() + SALT_B + ts).encode()).hexdigest()
def fetch():
    ts = str(int(time.time() * 1000))
    url = f"{API}?key={make_key(ts)}&time={ts}"
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Referer": "https://api.uouin.com/cloudflare.html"})
    with urllib.request.urlopen(req, timeout=25) as resp:
        return json.load(resp)
def to_edgetunnel(data):
    lines = []
    for group, rows in data.items():
        label = LINE_NAME.get(group, group)
        for r in rows.get("info", []):
            ip = r["ip"]
            host = f"[{ip}]" if ":" in ip else ip
            lines.append(f"{host}:443#{label} | {ip}")
    return chr(10).join(lines) + chr(10)

def update_gist(text):
    import os
    gid = os.environ.get("GIST_ID")
    tok = os.environ.get("GH_TOKEN")
    if not gid or not tok:
        print("skip gist upload: GIST_ID/GH_TOKEN not set")
        return
    body = json.dumps({"files": {"cfip.txt": {"content": text}}}).encode()
    req = urllib.request.Request(
        f"https://api.github.com/gists/{gid}",
        data=body,
        method="PATCH",
        headers={"Content-Type": "application/json",
                 "User-Agent": "cfip-bot",
                 "Authorization": f"Bearer {tok}"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        print("gist updated, status", resp.status)

if __name__ == "__main__":
    resp = fetch()
    if str(resp.get("code")) != "200":
        sys.exit("API error: " + str(resp)[:200])
    text = to_edgetunnel(resp["data"])
    update_gist(text)
    if len(sys.argv) > 1:
        with open(sys.argv[1], "w", encoding="utf-8") as f:
            f.write(text)
        print("written to", sys.argv[1])
    else:
        print(text, end="")
