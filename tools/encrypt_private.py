"""Encrypt the private family itinerary into itinerary.html.

Reads the clear-text HTML fragment (both family timelines, planner, map) from private/family-o.local.html (git-ignored) and the
family code from .env (FAMILY_O_CODE). Writes an AES-256-GCM payload, with the key derived by
PBKDF2-SHA256, into the PRIVATE_O block of itinerary.html. The page decrypts it in the browser
with Web Crypto once the family types the code.

Strength = the code's entropy only (16 random chars from 31 ~ 79 bits). Never use a short code.

Usage:
  python tools/encrypt_private.py [--json]
Exit codes: 0 ok, 1 tool failed (missing input, bad config), 2 ran but verification failed.
Dependency: `cryptography` (pip install cryptography) - stdlib has no AES-GCM.
"""
import argparse, base64, html, json, os, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "private" / "family-o.local.html"
PAGE = ROOT / "itinerary.html"
ENV = ROOT / ".env"
ITERATIONS = 300_000  # keep identical to PRIVATE_ITER in itinerary.html
BLOCK = re.compile(r"(/\*PRIVATE_O:BEGIN\*/).*?(/\*PRIVATE_O:END\*/)", re.S)


def normalise(code: str) -> str:
    # Same rule as the page: lowercase, drop spaces and dashes.
    return re.sub(r"[\s\-]", "", code).lower()


def read_code() -> str:
    # A FAMILY_O_CODE environment variable wins (used for browser tests with a throwaway code).
    if os.environ.get("FAMILY_O_CODE"):
        return normalise(os.environ["FAMILY_O_CODE"])
    if not ENV.exists():
        raise SystemExit(f"missing {ENV} - add a line FAMILY_O_CODE=<16 random chars>")
    for line in ENV.read_text(encoding="utf-8").splitlines():
        if line.startswith("FAMILY_O_CODE="):
            code = normalise(line.split("=", 1)[1].strip())
            if len(code) < 16:
                raise SystemExit("FAMILY_O_CODE is shorter than 16 chars - generate a longer random code")
            return code
    raise SystemExit(f"FAMILY_O_CODE not found in {ENV} - add it")


def plain_terms(fragment: str) -> list[str]:
    # Every visible name/address in the fragment; none may appear in the built page.
    terms = re.findall(r'data-copy="([^"]+)"', fragment) + re.findall(r"<strong>([^<]+)</strong>", fragment)
    # Booked events live as JSON in <script id="o-fixed">: their venue names ("n") and addresses ("a") are private.
    m = re.search(r'<script type="application/json" id="o-fixed">(.*?)</script>', fragment, re.S)
    if m:
        data = json.loads(m.group(1).replace("<\\/", "</"))
        # Per-family shape {"fam": {"o": {"fixed": ...}, "m": {...}}}; the older flat {"fixed": ...} is still read.
        groups = [data.get("fixed", {})] + [f.get("fixed", {}) for f in data.get("fam", {}).values()]
        for events in [e for g in groups for e in g.values()] + [data.get("pins", [])]:
            terms += [e[k] for e in events for k in ("n", "a") if e.get(k)]
    out = set()
    for t in terms:
        t = html.unescape(t).strip()
        if t.startswith("Sân bay"):  # airports are public facts, not private
            continue
        out.add(t)
        out.add(t.split(",")[0].strip())  # the venue name alone
    return sorted(out)


def publishable_files() -> list[Path]:
    # Every file git would commit: tracked + untracked-but-not-ignored.
    import subprocess
    out = subprocess.run(["git", "ls-files", "--cached", "--others", "--exclude-standard"],
                         cwd=ROOT, capture_output=True, text=True, encoding="utf-8", check=True).stdout
    return [ROOT / p for p in out.splitlines() if p and (ROOT / p).is_file()]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    def done(ok, summary, findings=(), code=0):
        if args.json:
            print(json.dumps({"ok": ok, "summary": summary, "findings": list(findings), "outputs": [str(PAGE)] if ok else []}))
        else:
            for f in findings:
                print(f"- {f}")
            print(summary)
        return code

    try:
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
        from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
        from cryptography.hazmat.primitives import hashes
    except ImportError:
        return done(False, "cryptography not installed - run: pip install cryptography", code=1)
    if not SRC.exists():
        return done(False, f"missing {SRC} - recreate the private fragment (it is git-ignored)", code=1)
    try:
        code = read_code()
    except SystemExit as e:
        return done(False, str(e), code=1)

    fragment = SRC.read_text(encoding="utf-8")
    salt, iv = os.urandom(16), os.urandom(12)
    key = PBKDF2HMAC(hashes.SHA256(), 32, salt, ITERATIONS).derive(code.encode())
    ct = AESGCM(key).encrypt(iv, fragment.encode("utf-8"), None)
    b64 = lambda b: base64.b64encode(b).decode()
    payload = json.dumps({"s": b64(salt), "i": b64(iv), "c": b64(ct)})

    raw = PAGE.read_bytes().decode("utf-8")
    if not BLOCK.search(raw):
        return done(False, "PRIVATE_O markers not found in itinerary.html - restore the /*PRIVATE_O:BEGIN*/.../*PRIVATE_O:END*/ block", code=1)
    built = BLOCK.sub(lambda m: f"{m.group(1)}{payload}{m.group(2)}", raw, count=1)
    PAGE.write_bytes(built.encode("utf-8"))

    # Verify: round-trip decrypt, and no clear-text term left in the page.
    findings = []
    m = re.search(r"/\*PRIVATE_O:BEGIN\*/(.*?)/\*PRIVATE_O:END\*/", PAGE.read_text(encoding="utf-8"), re.S)
    p = json.loads(m.group(1))
    back = AESGCM(PBKDF2HMAC(hashes.SHA256(), 32, base64.b64decode(p["s"]), ITERATIONS).derive(code.encode())).decrypt(
        base64.b64decode(p["i"]), base64.b64decode(p["c"]), None).decode()
    if back != fragment:
        findings.append("round-trip decrypt does not match the source fragment")
    terms = plain_terms(fragment)
    if not terms:
        findings.append("no terms extracted from the fragment - the plaintext check proved nothing")
    # Tầm Vị is also listed in the public Hà Nội restaurant guide; only the booking is private.
    public_ok = {"tầm vị"}
    check = [t.lower() for t in terms if t.lower() not in public_ok]
    for f in publishable_files():
        try:
            text = html.unescape(f.read_text(encoding="utf-8")).lower()
        except (UnicodeDecodeError, OSError):
            continue
        n = sum(1 for t in check if t in text)
        if n:
            findings.append(f"{n} private term(s) in clear text in {f.relative_to(ROOT)} - remove them before committing")
    if findings:
        return done(False, "encrypted, but verification FAILED", findings, code=2)
    return done(True, f"encrypted {len(fragment)} chars into itinerary.html; round-trip ok; 0 of {len(terms)} private terms in clear text")


if __name__ == "__main__":
    sys.exit(main())
