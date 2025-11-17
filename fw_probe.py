# fw_probe.py
import sys, time, ssl, hashlib, binascii, warnings
import requests
from requests.adapters import HTTPAdapter
from requests.auth import HTTPDigestAuth
from urllib3.util.ssl_ import create_urllib3_context
from urllib3.exceptions import InsecureRequestWarning
warnings.filterwarnings("ignore", category=InsecureRequestWarning)

HOST = "192.168.100.159"
USER = "root"
PW   = "tbtseyeon2024!"

URL  = (f"https://{HOST}:443/cgi-bin/fwtransparent.cgi"
        f"?BaudRate=38400&DataBit=8&StopBit=1&ParityBit=n&Node=ttyS1&FwCgiVer=0x0001")

SEND_CMD = bytes([0xff, 0x00, 0x21, 0x13, 0x00, 0x01, 0x35])
READ_MAX = 4096

def log(msg):
    print(msg, flush=True)

class TLSLegacyAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        ctx = create_urllib3_context()
        ctx.minimum_version = ssl.TLSVersion.TLSv1
        ctx.set_ciphers("ALL:@SECLEVEL=0")
        ctx.check_hostname = False
        kwargs["ssl_context"] = ctx
        kwargs["assert_hostname"] = False
        return super().init_poolmanager(*args, **kwargs)

log("[1] starting fw_probe.py")
s = requests.Session()
s.verify = False
s.headers.update({"Connection": "close", "Accept": "*/*", "User-Agent": "py-client"})
s.mount("https://", TLSLegacyAdapter())

try:
    log("[2] warmup GET /")
    s.get(f"https://{HOST}:443/", timeout=5, allow_redirects=True)
    log("[2] warmup GET /index_multi_login.asp")
    s.get(f"https://{HOST}:443/index_multi_login.asp", timeout=5, allow_redirects=True)
except Exception as e:
    log(f"[2] warmup exc: {e!r}")

enc = hashlib.sha256(f"{PW}:1:{USER}".encode()).hexdigest()
cookie_val = f"id={USER};sc=1;response={enc};"
s.cookies.set("-goahead-session-", cookie_val, domain=HOST, path="/")
auth = HTTPDigestAuth(USER, PW)

log("[3] opening fwtransparent stream (10s timeout)")
try:
    r = s.get(URL, auth=auth, timeout=10, stream=True, allow_redirects=False)
    log(f"[3] status_code={r.status_code}")
except Exception as e:
    log(f"[3] GET exc: {e!r}")
    sys.exit(1)

raw = getattr(r, "raw", None)
log(f"[4] raw present? {'yes' if raw else 'no'}")
sock = None
for path in ("_fp.fp.raw._sock", "_fp._sock"):
    try:
        obj = raw
        for attr in path.split("."):
            obj = getattr(obj, attr)
        sock = obj
        log(f"[4] socket path ok: raw.{path} -> {type(sock)}")
        break
    except Exception as e:
        log(f"[4] try raw.{path}: {e!r}")

if sock is None:
    log("[4] could not extract socket; abort")
    try: r.close(); s.close()
    except: pass
    sys.exit(1)

try:
    sock.settimeout(3.0)
except Exception as e:
    log(f"[4] settimeout exc: {e!r}")

log("[5] pre-read up to 512 bytes (3s)")
try:
    time.sleep(0.2)
    pre = sock.recv(512)
    log(f"[5] pre-read len={len(pre)} hex={binascii.hexlify(pre).decode() if pre else ''}")
except Exception as e:
    log(f"[5] pre-read exc: {e!r}")

log("[6] send command bytes")
try:
    sock.sendall(SEND_CMD)
    log(f"[6] sent {len(SEND_CMD)} bytes hex={binascii.hexlify(SEND_CMD).decode()}")
except Exception as e:
    log(f"[6] send exc: {e!r}")

log("[7] post-read up to 1024 bytes (3s)")
try:
    time.sleep(0.3)
    post = sock.recv(1024)
    log(f"[7] post-read len={len(post)} hex={binascii.hexlify(post).decode() if post else ''}")
except Exception as e:
    log(f"[7] post-read exc: {e!r}")

log("[8] cleanup")
try:
    try: sock.shutdown(1)
    except: pass
    r.close(); s.close()
except Exception as e:
    log(f"[8] cleanup exc: {e!r}")

log("[9] done")
