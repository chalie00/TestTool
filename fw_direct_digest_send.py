# fw_direct_digest_matrix.py
import ssl, socket, time, hashlib, binascii, re, secrets

HOST, PORT = "192.168.100.159", 443
USER, PW   = "root", "tbtseyeon2024!"

BAUDS = [57600, 38400]       # 1) 57600 우선
NODES = ["ttyS1", "ttyS0"]   # 2) 노드 교차
PARITY = "n"                  # 3) 소문자 n 고정
DBITS, SBITS = 8, 1
FRAMES = [b"", b"\r", b"\r\n"]  # 4) 프레이밍 후보

SEND_CMD = bytes([0xff,0x00,0x21,0x13,0x00,0x01,0x35])
SOCK_TMO, READ_MAX = 5.0, 8192

def make_ctx():
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    try: ctx.minimum_version = ssl.TLSVersion.TLSv1
    except: pass
    ctx.set_ciphers("ALL:@SECLEVEL=0")
    ctx.check_hostname, ctx.verify_mode = False, ssl.CERT_NONE
    return ctx

def tls_connect():
    raw = socket.create_connection((HOST, PORT), timeout=5)
    s = make_ctx().wrap_socket(raw, server_hostname=None)
    s.settimeout(SOCK_TMO)
    return s

def enc_cookie(user,pw):
    enc = hashlib.sha256(f"{pw}:1:{user}".encode()).hexdigest()
    return f"id={user};sc=1;response={enc};"

def get_admin_challenge():
    # 관리자 페이지에서 401 받아 realm/nonce 확보 (없어도 MD5 추정값으로 진행)
    s = tls_connect()
    fp = s.makefile("rb", buffering=0)
    req = (f"GET /admin/aindex_m.asp HTTP/1.0\r\nHost: {HOST}\r\nConnection: close\r\n\r\n").encode()
    s.sendall(req)
    # 헤더 읽기(짧게)
    start = time.time()
    def readl(): return fp.readline().decode("iso-8859-1","replace")
    status = readl()
    realm = "GoAhead"; nonce = ""; opaque = ""
    while time.time() - start < 2.0:
        line = readl()
        if line in ("\r\n","\n",""): break
        if line.lower().startswith("www-authenticate:"):
            w = line.split(":",1)[1]
            r = re.search(r'realm="([^"]+)"', w); n = re.search(r'nonce="([^"]+)"', w); o = re.search(r'opaque="([^"]+)"', w)
            if r: realm = r.group(1)
            if n: nonce = n.group(1)
            if o: opaque = o.group(1)
    try: s.close()
    except: pass
    return dict(realm=realm, nonce=nonce, opaque=opaque, algorithm="MD5", qop="auth")

def build_auth(user,pw,method,uri,chal,nc="00000001"):
    H = hashlib.md5   # MD5로 고정 시도 (장비 호환성 ↑)
    cnonce = secrets.token_hex(16)
    HA1 = H(f"{user}:{chal['realm']}:{pw}".encode()).hexdigest()
    HA2 = H(f"{method}:{uri}".encode()).hexdigest()
    resp = H(f"{HA1}:{chal['nonce']}:{nc}:{cnonce}:auth:{HA2}".encode()).hexdigest()
    parts = [
        f'username="{user}"', f'realm="{chal["realm"]}"',
        f'nonce="{chal["nonce"]}"', f'uri="{uri}"',
        f'response="{resp}"', 'algorithm="MD5"',
        'qop=auth', f'nc={nc}', f'cnonce="{cnonce}"'
    ]
    if chal.get("opaque"):
        parts.append(f'opaque="{chal["opaque"]}"')
    return "Digest " + ",".join(parts)

def open_tunnel(baud, node):
    uri = (f"/cgi-bin/fwtransparent.cgi?BaudRate={baud}&DataBit={DBITS}&StopBit={SBITS}"
           f"&ParityBit={PARITY}&Node={node}&FwCgiVer=0x0001")
    s = tls_connect()
    cookie = enc_cookie(USER,PW)
    chal = get_admin_challenge()  # realm/nonce 확보 (MD5로 계산)
    authz = build_auth(USER,PW,"GET",uri,chal)

    # 헤더 응답은 안 기다리고 바로 명령 보낼 수 있게 HTTP/1.0 요청만 전송
    req = (f"GET {uri} HTTP/1.0\r\n"
           f"Host: {HOST}\r\n"
           f"Authorization: {authz}\r\n"
           f"Cookie: -goahead-session-={cookie}\r\n"
           "Accept: */*\r\nUser-Agent: py-client\r\n"
           "Connection: keep-alive\r\n\r\n").encode()
    s.sendall(req)
    return s

def try_once(baud, node, frame_bytes):
    s = open_tunnel(baud, node)
    payload = SEND_CMD + frame_bytes
    time.sleep(0.3)  # 서버가 터널 준비할 시간
    s.sendall(payload)
    # 응답 모으기(최대 3초)
    end_by = time.time() + 10.0
    total = bytearray()
    while time.time() < end_by:
        try:
            chunk = s.recv(READ_MAX)
            if not chunk:
                break
            total += chunk
        except socket.timeout:
            break
    s.close()
    return bytes(total)

def main():
    for baud in BAUDS:
        for node in NODES:
            for fb in FRAMES:
                label = f"baud={baud}, node={node}, frame={'NONE' if fb==b'' else fb!r}"
                try:
                    data = try_once(baud, node, fb)
                    hexout = binascii.hexlify(data).decode() if data else ""
                    print(f"[TEST] {label} -> recv {len(data)} bytes")
                    if data:
                        # 앞 64바이트만 프리뷰
                        print("       hex:", hexout[:128], "..." if len(hexout)>128 else "")
                    # 성공 케이스가 나오면 여기서 조기 종료해도 됨
                except Exception as e:
                    print(f"[TEST] {label} -> EXC: {e!r}")

if __name__ == "__main__":
    main()
