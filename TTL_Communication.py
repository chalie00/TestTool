# 2025.11.12: Added for Seyeon TTL Version

import ssl, socket, time, hashlib, binascii, re, secrets, logging

import Constant as Cons


def _make_legacy_tls():
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    try:
        ctx.minimum_version = ssl.TLSVersion.TLSv1  # 장비 호환
    except Exception:
        pass
    ctx.set_ciphers("ALL:@SECLEVEL=0")
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx


def _tls_connect(host, port, timeout=5.0):
    raw = socket.create_connection((host, port), timeout=timeout)
    s = _make_legacy_tls().wrap_socket(raw, server_hostname=None)
    s.settimeout(5.0)
    return s


def _read_headers(fp, timeout=2.0):
    start = time.time()
    status = fp.readline().decode("iso-8859-1", "replace")
    headers = {}
    while True:
        if time.time() - start > timeout: break
        line = fp.readline().decode("iso-8859-1", "replace")
        if line in ("\r\n", "\n", ""): break
        if ":" in line:
            k, v = line.split(":", 1)
            headers.setdefault(k.strip(), []).append(v.strip())
    return status, headers


def _get_admin_challenge(host):
    # /admin/aindex_m.asp 로 401 챌린지만 한번 받아 realm/nonce 확보 (MD5로 사용)
    s = _tls_connect(host, Cons.selected_ch['port'])
    fp = s.makefile("rb", buffering=0)
    req = (f"GET /admin/aindex_m.asp HTTP/1.0\r\nHost: {host}\r\nConnection: close\r\n\r\n").encode()
    s.sendall(req)
    status, hdrs = _read_headers(fp, timeout=2.0)
    was = hdrs.get("WWW-Authenticate", []) + hdrs.get("Www-Authenticate", [])
    realm, nonce, opaque = "GoAhead", "", ""
    for w in was:
        r = re.search(r'realm="([^"]+)"', w)
        n = re.search(r'nonce="([^"]+)"', w)
        o = re.search(r'opaque="([^"]+)"', w)
        if r: realm = r.group(1)
        if n: nonce = n.group(1)
        if o: opaque = o.group(1)
        break
    try:
        s.close()
    except:
        pass
    return dict(realm=realm, nonce=nonce, opaque=opaque, qop="auth")


def _build_digest_md5(user, pw, method, uri, chal, nc="00000001"):
    H = hashlib.md5
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


def _enc_cookie(user, pw):
    enc = hashlib.sha256(f"{pw}:1:{user}".encode()).hexdigest()
    return f"id={user};sc=1;response={enc};"
