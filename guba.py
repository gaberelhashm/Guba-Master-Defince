#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Guba-Master-Defence v1.0
Modern Defensive Security Toolkit • 2027 Edition
Defense Only • Termux / Linux / macOS
"""

import os
import sys
import json
import time
import hashlib
import re
import base64
import getpass
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime
from pathlib import Path

# ────────────────────────────────────────────────
# Paths & Config
# ────────────────────────────────────────────────
HOME = Path.home()
CONFIG_DIR = HOME / ".guba_defence"
CONFIG_FILE = CONFIG_DIR / "config.json"
HISTORY_FILE = CONFIG_DIR / "history.json"
LOG_FILE = CONFIG_DIR / "guba.log"

DEFAULT_USER = "admin"
DEFAULT_PASS = "guba2027"

def ensure_dirs():
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

def load_config():
    ensure_dirs()
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "vt_api_key": "",
        "username": DEFAULT_USER,
        "password_hash": hashlib.sha256(DEFAULT_PASS.encode()).hexdigest(),
    }

def save_config(cfg):
    ensure_dirs()
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)

def log(msg):
    ensure_dirs()
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{ts}] {msg}\n")

def add_history(entry):
    ensure_dirs()
    history = []
    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                history = json.load(f)
        except Exception:
            pass
    history.insert(0, entry)
    history = history[:50]
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)

# ────────────────────────────────────────────────
# 2027 Modern Color Palette
# ────────────────────────────────────────────────
class C:
    # Core
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"

    # 2027 Neon / Cyber palette
    CYAN    = "\033[38;5;51m"      # Electric cyan
    BLUE    = "\033[38;5;39m"      # Soft electric blue
    PURPLE  = "\033[38;5;141m"     # Soft violet
    PINK    = "\033[38;5;213m"     # Neon pink accent
    GREEN   = "\033[38;5;48m"      # Mint / success
    YELLOW  = "\033[38;5;221m"     # Soft gold
    ORANGE  = "\033[38;5;208m"     # Warm orange
    RED     = "\033[38;5;203m"     # Soft red
    WHITE   = "\033[38;5;255m"
    GRAY    = "\033[38;5;245m"
    DARK    = "\033[38;5;238m"

    # Backgrounds
    BG_RED  = "\033[48;5;52m"
    BG_YEL  = "\033[48;5;94m"
    BG_GRN  = "\033[48;5;22m"

def clear():
    os.system("clear" if os.name != "nt" else "cls")

def ok(msg):   print(f"  {C.GREEN}▸{C.RESET} {msg}")
def warn(msg): print(f"  {C.YELLOW}▸{C.RESET} {msg}")
def err(msg):  print(f"  {C.RED}▸{C.RESET} {msg}")
def info(msg): print(f"  {C.CYAN}▸{C.RESET} {msg}")
def title(msg):
    print(f"\n  {C.BOLD}{C.CYAN}{msg}{C.RESET}\n")

def pause():
    input(f"\n  {C.GRAY}⏎  Press Enter to return...{C.RESET}")

# ────────────────────────────────────────────────
# Compact Owner Signature (ASCII)
# ────────────────────────────────────────────────
FACE = r"""
  @@@@@@%%%%@@@@@%##**####@@@@@@%%
  @@@%%@@@@@%#++-:::::  .:-=*#%@@@
  @@%@@@%#*=:.               ..=+%@
  @%@%*=:                       .:*@
  %@#=..                           -*
  %%#-      .:----:--=---===+++=-.  .
  @%*.  :--=*****++++++********##*-  
  %#-.*#%%##****+++++++++++++++*##*: 
  +..#@@%#****++++++++++++++++++***- 
  +.=@%%#**++++++++++++++++++==+++*- 
  +:*@%#**++++++++++++++++++=====++*+
  =.+%#********+++++++++++====-==++**
  #.=##*+***++++++++===-:.........-**
  @-=##*+=--:::...:=-    ....     .-+
  @#+%#=:.        .--:.:           .-+
  %@*#:..        :.=+=:.            -+
  %%*-            :**+-.           .=+
  @%*=           .=**+=-.         :==+
  %%%#+.        .:+#*++=-:......:----=
  *#%%#*=:.  ..::=+==--::-::--=====---
  *##****+++++=---        :---=====---
"""

def banner(cfg):
    vt = f"{C.GREEN}ONLINE{C.RESET}" if cfg.get("vt_api_key") else f"{C.RED}OFFLINE{C.RESET}"
    print(f"""
{C.CYAN}{C.BOLD}
  ╭──────────────────────────────────────────────╮
  │     G U B A  ·  M A S T E R  ·  D E F E N C E │
  │           Defensive Security Toolkit           │
  │                  v1.0  ·  2027                 │
  ╰──────────────────────────────────────────────╯{C.RESET}
{C.DARK}{FACE}{C.RESET}
  {C.GRAY}Owner Signature  ·  VirusTotal {vt}  ·  Defense Only{C.RESET}
""")

# ────────────────────────────────────────────────
# Login
# ────────────────────────────────────────────────
def login(cfg):
    max_attempts = 3
    for attempt in range(max_attempts):
        clear()
        print(f"""
{C.CYAN}{C.BOLD}
  ╭──────────────────────────────────────────────╮
  │     G U B A  ·  M A S T E R  ·  D E F E N C E │
  │                  AUTHENTICATION                │
  ╰──────────────────────────────────────────────╯{C.RESET}
{C.DARK}{FACE}{C.RESET}
""")
        print(f"  {C.GRAY}Secure access required{C.RESET}\n")
        user = input(f"  {C.CYAN}Username  › {C.RESET}").strip()
        try:
            pwd = getpass.getpass(f"  {C.CYAN}Password  › {C.RESET}")
        except Exception:
            pwd = input(f"  {C.CYAN}Password  › {C.RESET}")

        stored_user = cfg.get("username", DEFAULT_USER)
        stored_hash = cfg.get("password_hash", hashlib.sha256(DEFAULT_PASS.encode()).hexdigest())
        if user == stored_user and hashlib.sha256(pwd.encode()).hexdigest() == stored_hash:
            print()
            ok("Access granted")
            log(f"Login success: {user}")
            time.sleep(0.8)
            return True
        left = max_attempts - attempt - 1
        print()
        err(f"Invalid credentials · {left} attempts left")
        log(f"Failed login: {user}")
        time.sleep(1.3)

    err("Too many failed attempts · Locked")
    log("Login lockout")
    time.sleep(1.2)
    sys.exit(1)

# ────────────────────────────────────────────────
# VirusTotal
# ────────────────────────────────────────────────
VT = "https://www.virustotal.com/api/v3"

def vt_req(endpoint, key, method="GET", data=None):
    url = f"{VT}{endpoint}"
    headers = {"x-apikey": key, "Accept": "application/json", "User-Agent": "GubaMasterDefence/1.0"}
    try:
        if method == "GET":
            req = urllib.request.Request(url, headers=headers)
        else:
            body = json.dumps(data).encode() if data else b""
            req = urllib.request.Request(url, data=body, headers=headers, method=method)
            req.add_header("Content-Type", "application/json")
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode() if e.fp else ""
        try:
            msg = json.loads(body).get("error", {}).get("message", str(e))
        except Exception:
            msg = str(e)
        raise Exception(f"VT {e.code}: {msg}")
    except Exception as e:
        raise Exception(f"Connection: {e}")

def vt_url_report(url, key):
    uid = base64.urlsafe_b64encode(url.encode()).decode().strip("=")
    return vt_req(f"/urls/{uid}", key)

def vt_url_scan(url, key):
    data = urllib.parse.urlencode({"url": url}).encode()
    headers = {"x-apikey": key, "Content-Type": "application/x-www-form-urlencoded", "User-Agent": "GubaMasterDefence/1.0"}
    req = urllib.request.Request(f"{VT}/urls", data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode())

def vt_file_report(sha, key):
    return vt_req(f"/files/{sha}", key)

def print_verdict(stats, title="VirusTotal Verdict"):
    if not stats:
        warn("No report available yet")
        return
    mal = stats.get("malicious", 0)
    sus = stats.get("suspicious", 0)
    harm = stats.get("harmless", 0)
    und = stats.get("undetected", 0)
    total = mal + sus + harm + und

    if mal > 0:
        color, verdict = C.RED, "MALICIOUS"
    elif sus > 0:
        color, verdict = C.YELLOW, "SUSPICIOUS"
    else:
        color, verdict = C.GREEN, "CLEAN"

    print(f"\n  {C.BOLD}{title}{C.RESET}")
    print(f"  {C.DARK}{'─'*42}{C.RESET}")
    print(f"  {color}{C.BOLD}Verdict     {verdict}{C.RESET}")
    print(f"  Malicious  {C.RED}{mal}{C.RESET}   Suspicious {C.YELLOW}{sus}{C.RESET}")
    print(f"  Harmless   {C.GREEN}{harm}{C.RESET}   Undetected {C.GRAY}{und}{C.RESET}")
    print(f"  Engines    {total}")
    if total:
        mbar = int(mal / total * 22)
        sbar = int(sus / total * 22)
        bar = f"{C.RED}{'█'*mbar}{C.YELLOW}{'█'*sbar}{C.DARK}{'░'*(22-mbar-sbar)}{C.RESET}"
        print(f"  Risk       [{bar}]")

# ────────────────────────────────────────────────
# Modules
# ────────────────────────────────────────────────
def scan_url(cfg):
    clear(); banner(cfg)
    title("URL Threat Scanner")
    url = input(f"  {C.CYAN}URL › {C.RESET}").strip()
    if not url:
        err("No URL provided"); pause(); return
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    print(); info(f"Target  {url}"); log(f"URL: {url}")

    print(f"\n  {C.BOLD}[1/3] Local Heuristics{C.RESET}")
    findings, score = [], 0
    patterns = [
        (r"(bit\.ly|tinyurl|t\.co|goo\.gl|ow\.ly|is\.gd|buff\.ly|rebrand\.ly|cutt\.ly)", "URL shortener", 15),
        (r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", "Direct IP instead of domain", 20),
        (r"(login|signin|verify|account|secure|update|bank|paypal|wallet|crypto|gift|prize)", "Phishing keywords", 10),
        (r"(\.exe|\.apk|\.scr|\.bat|\.cmd|\.js|\.vbs|\.ps1|\.msi)(\?|$)", "Dangerous extension", 25),
        (r"@", "Hidden domain via @", 30),
        (r"(ngrok\.io|serveo\.net|localtunnel\.me|cloudflared|trycloudflare)", "Tunnel service (RAT indicator)", 35),
        (r"(free|bonus|claim|urgent|limited|act.?now|click.?here)", "Urgency language", 8),
    ]
    for pat, desc, pts in patterns:
        if re.search(pat, url, re.I):
            findings.append((desc, pts)); score += pts
    if urllib.parse.urlparse(url).netloc.count(".") > 3:
        findings.append(("Complex subdomain structure", 10)); score += 10
    if findings:
        for d, p in findings:
            print(f"  {C.RED}•{C.RESET} {d}  {C.GRAY}+{p}{C.RESET}")
    else:
        ok("No strong local indicators")
    print(f"\n  {C.BOLD}Local Risk  {score}/100{C.RESET}")

    print(f"\n  {C.BOLD}[2/3] Headers & Redirects{C.RESET}")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "GubaMasterDefence/1.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            final = r.geturl()
            ok(f"Status   {r.status}")
            info(f"Final    {final}")
            info(f"Type     {r.headers.get('Content-Type', '—')}")
            info(f"Server   {r.headers.get('Server', '—')}")
            if final.rstrip("/") != url.rstrip("/"):
                warn("Redirect detected"); score += 15
    except urllib.error.HTTPError as e:
        warn(f"HTTP {e.code}"); score += 5
    except Exception as e:
        err(f"Connection failed: {e}"); score += 10

    print(f"\n  {C.BOLD}[3/3] VirusTotal{C.RESET}")
    key = cfg.get("vt_api_key", "").strip()
    if not key:
        warn("API key not set · Go to Settings [7]")
        print(f"  {C.GRAY}https://www.virustotal.com/gui/url/{base64.urlsafe_b64encode(url.encode()).decode().strip('=')}/detection{C.RESET}")
    else:
        try:
            info("Querying VirusTotal...")
            report = vt_url_report(url, key)
            attrs = report.get("data", {}).get("attributes", {})
            print_verdict(attrs.get("last_analysis_stats", {}))
            if attrs.get("title"):
                print(f"  Title  {attrs['title'][:55]}")
        except Exception as e:
            if "404" in str(e) or "NotFound" in str(e):
                warn("Not in database · Submitting...")
                try:
                    vt_url_scan(url, key); ok("Submitted · Retry in 30-60s")
                except Exception as e2:
                    err(str(e2))
            else:
                err(str(e))

    print(f"\n  {C.DARK}{'═'*46}{C.RESET}")
    if score >= 40:
        print(f"  {C.BG_RED}{C.WHITE}{C.BOLD} HIGH RISK {C.RESET}  Score {score}")
        warn("Do not open this link")
    elif score >= 20:
        print(f"  {C.BG_YEL}{C.WHITE}{C.BOLD} MEDIUM RISK {C.RESET}  Score {score}")
        warn("Proceed with caution")
    else:
        print(f"  {C.BG_GRN}{C.WHITE}{C.BOLD} LOW RISK {C.RESET}  Score {score}")
        ok("No strong local indicators")

    add_history({"type": "url", "target": url, "score": score, "time": datetime.now().isoformat()})
    pause()

def analyze_file(cfg):
    clear(); banner(cfg)
    title("File / APK Analysis")
    path = input(f"  {C.CYAN}Path › {C.RESET}").strip()
    if not path or not os.path.isfile(path):
        err("File not found"); pause(); return
    path = os.path.abspath(path)
    size = os.path.getsize(path)
    info(f"File  {path}")
    info(f"Size  {size:,} bytes ({size/1024:.1f} KB)")
    log(f"File: {path}")

    print(f"\n  {C.BOLD}[1/4] Hashes{C.RESET}")
    md5, sha1, sha256 = hashlib.md5(), hashlib.sha1(), hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            md5.update(chunk); sha1.update(chunk); sha256.update(chunk)
    h_md5, h_sha1, h_sha256 = md5.hexdigest(), sha1.hexdigest(), sha256.hexdigest()
    print(f"  MD5     {h_md5}")
    print(f"  SHA1    {h_sha1}")
    print(f"  SHA256  {C.BOLD}{h_sha256}{C.RESET}")

    print(f"\n  {C.BOLD}[2/4] Structure{C.RESET}")
    with open(path, "rb") as f:
        magic = f.read(8)
    if magic[:2] == b"PK":
        ok("ZIP / APK archive")
        try:
            import zipfile
            with zipfile.ZipFile(path, "r") as z:
                names = z.namelist()
                info(f"Entries  {len(names)}")
                if "AndroidManifest.xml" in names:
                    ok("AndroidManifest.xml → APK detected")
                interesting = [n for n in names if any(x in n.lower() for x in
                    ["payload", "shell", "meter", "rat", "trojan", "classes.dex", "lib/", "assets/"])]
                print(f"\n  {C.YELLOW}Key files{C.RESET}")
                for n in names[:10]:
                    mark = f"{C.RED}★{C.RESET}" if n in interesting else " "
                    print(f"   {mark} {n}")
                if len(names) > 10:
                    print(f"   ... +{len(names)-10} more")
                if interesting:
                    print(f"\n  {C.RED}Notable{C.RESET}")
                    for n in interesting[:8]:
                        print(f"   • {n}")
        except Exception as e:
            warn(f"ZIP error: {e}")
    elif magic[:4] == b"\x7fELF":
        ok("ELF binary")
    elif magic[:2] == b"MZ":
        warn("Windows PE · unusual on Android")
    else:
        info(f"Magic  {magic.hex()}")

    print(f"\n  {C.BOLD}[3/4] Strings{C.RESET}")
    try:
        with open(path, "rb") as f:
            data = f.read(3_000_000)
        text = data.decode("utf-8", errors="ignore")
        keywords = {
            "C2 / Tunnel": ["ngrok", "serveo", "localtunnel", "webhook.site", "burpcollaborator"],
            "RAT Indicators": ["payload", "shellcode", "meterpreter", "reverse_tcp", "bind_tcp", "msfvenom"],
            "Dangerous Android": ["SEND_SMS", "READ_SMS", "RECEIVE_SMS", "CALL_PHONE", "RECORD_AUDIO",
                                  "CAMERA", "ACCESSIBILITY", "DEVICE_ADMIN", "SYSTEM_ALERT_WINDOW",
                                  "REQUEST_INSTALL_PACKAGES", "BIND_ACCESSIBILITY_SERVICE"],
            "Code Execution": ["Runtime.getRuntime", "ProcessBuilder", "Runtime.exec", "su -c"],
            "Obfuscation": ["base64_decode", "fromCharCode", "eval(", "Function(", "atob("],
        }
        found = False
        for cat, words in keywords.items():
            hits = [w for w in words if w.lower() in text.lower()]
            if hits:
                found = True
                print(f"  {C.RED}{cat}{C.RESET}")
                for h in hits:
                    print(f"     • {h}")
        if not found:
            ok("No obvious suspicious keywords")
    except Exception as e:
        warn(f"Strings failed: {e}")

    print(f"\n  {C.BOLD}[4/4] VirusTotal{C.RESET}")
    key = cfg.get("vt_api_key", "").strip()
    if not key:
        warn("API key not set")
        print(f"  {C.GRAY}https://www.virustotal.com/gui/file/{h_sha256}{C.RESET}")
    else:
        try:
            info("Querying VirusTotal...")
            report = vt_file_report(h_sha256, key)
            attrs = report.get("data", {}).get("attributes", {})
            print_verdict(attrs.get("last_analysis_stats", {}), "File Verdict")
            if attrs.get("names"):
                print(f"  Names  {', '.join(attrs['names'][:5])}")
            if attrs.get("tags"):
                print(f"  Tags   {', '.join(attrs['tags'][:8])}")
            print(f"\n  Report  https://www.virustotal.com/gui/file/{h_sha256}")
        except Exception as e:
            if "404" in str(e) or "NotFound" in str(e):
                warn("Not in database · Upload manually if needed")
            else:
                err(str(e))

    add_history({"type": "file", "target": path, "sha256": h_sha256, "size": size, "time": datetime.now().isoformat()})
    pause()

def check_hash(cfg):
    clear(); banner(cfg)
    title("Hash Reputation Lookup")
    h = input(f"  {C.CYAN}Hash › {C.RESET}").strip().lower()
    if not h or not re.fullmatch(r"[a-f0-9]{32}|[a-f0-9]{40}|[a-f0-9]{64}", h):
        err("Invalid hash"); pause(); return
    print()
    key = cfg.get("vt_api_key", "").strip()
    if key and len(h) == 64:
        try:
            info("Querying VirusTotal...")
            report = vt_file_report(h, key)
            attrs = report.get("data", {}).get("attributes", {})
            print_verdict(attrs.get("last_analysis_stats", {}))
            if attrs.get("names"):
                print(f"\n  Names  {', '.join(attrs['names'][:6])}")
            print(f"\n  Report  https://www.virustotal.com/gui/file/{h}")
        except Exception as e:
            err(str(e))
            print(f"  {C.GRAY}https://www.virustotal.com/gui/file/{h}{C.RESET}")
    else:
        info("Lookup links")
        print(f"  VirusTotal      https://www.virustotal.com/gui/file/{h}")
        print(f"  Hybrid Analysis https://www.hybrid-analysis.com/search?query={h}")
        print(f"  MalwareBazaar   https://bazaar.abuse.ch/browse.php?search=sha256%3A{h}")
        if not key:
            print(); warn("Set API key in Settings [7] for full reports")
    add_history({"type": "hash", "target": h, "time": datetime.now().isoformat()})
    pause()

def permissions_guide(cfg):
    clear(); banner(cfg)
    title("Dangerous Android Permissions")
    groups = [
        (f"{C.RED}CRITICAL{C.RESET}  RAT / Spyware", [
            ("SEND_SMS / RECEIVE_SMS / READ_SMS", "Classic banking trojan behavior"),
            ("BIND_ACCESSIBILITY_SERVICE", "Full UI control — extremely dangerous"),
            ("DEVICE_ADMIN", "Can lock or wipe the device"),
            ("SYSTEM_ALERT_WINDOW", "Overlay attacks"),
            ("REQUEST_INSTALL_PACKAGES", "Install apps outside the store"),
        ]),
        (f"{C.ORANGE}HIGH{C.RESET}", [
            ("RECORD_AUDIO / CAMERA", "Silent recording"),
            ("READ_CALL_LOG / CALL_PHONE", "Call monitoring"),
            ("ACCESS_FINE_LOCATION", "Persistent tracking"),
            ("READ_CONTACTS / GET_ACCOUNTS", "Contact theft"),
            ("QUERY_ALL_PACKAGES", "Enumerate installed apps"),
        ]),
        (f"{C.YELLOW}MEDIUM{C.RESET}", [
            ("READ/WRITE_EXTERNAL_STORAGE", "File access"),
            ("INTERNET + NETWORK_STATE", "Normal, risky when combined"),
            ("RECEIVE_BOOT_COMPLETED", "Auto-start after reboot"),
            ("FOREGROUND_SERVICE", "Persistent background service"),
        ]),
    ]
    for title_, items in groups:
        print(f"\n  {C.BOLD}{title_}{C.RESET}")
        for perm, desc in items:
            print(f"  {C.RED}•{C.RESET} {C.BOLD}{perm}{C.RESET}")
            print(f"    {C.GRAY}{desc}{C.RESET}")
    print(f"\n  {C.YELLOW}{C.BOLD}Rule{C.RESET}")
    print("  3+ CRITICAL permissions without clear reason → delete the APK")
    print("  Tools: jadx · apktool · MobSF · Quark-Engine")
    pause()

def network_check(cfg):
    clear(); banner(cfg)
    title("Network Health Check")
    targets = ["8.8.8.8", "1.1.1.1", "google.com", "cloudflare.com", "github.com", "virustotal.com"]
    print(f"  {'Host':<20} {'Status':<10} Latency")
    print(f"  {C.DARK}{'─'*42}{C.RESET}")
    for host in targets:
        try:
            start = time.time()
            url = f"https://{host}" if not host.replace(".", "").isdigit() else f"http://{host}"
            urllib.request.urlopen(url, timeout=5)
            ms = (time.time() - start) * 1000
            print(f"  {host:<20} {C.GREEN}OK{C.RESET}         {ms:.0f} ms")
        except Exception as e:
            print(f"  {host:<20} {C.RED}FAIL{C.RESET}       {type(e).__name__}")
    print()
    info("Repeated failures may indicate DNS issues or blocking")
    pause()

def ai_chat(cfg):
    clear(); banner(cfg)
    title("Defense Assistant")
    print(f"  {C.GRAY}Commands: scan url · permissions · payload · help · exit{C.RESET}\n")
    knowledge = {
        "url": "Use [1] to scan any link (heuristics + headers + VirusTotal).",
        "link": "Menu [1] or type a full URL here.",
        "file": "Menu [2] — provide APK or file path.",
        "apk": "Menu [2] checks Manifest, strings and VirusTotal.",
        "hash": "Menu [3] — paste any hash for reputation lookup.",
        "permission": "Menu [4] lists dangerous Android permissions.",
        "sms": "READ_SMS / SEND_SMS without clear reason = strong Trojan signal.",
        "payload": "Use [2] to search for payload / shellcode / C2 indicators.",
        "ngrok": "ngrok / serveo / localtunnel are frequently abused by RATs.",
        "accessibility": "BIND_ACCESSIBILITY_SERVICE grants near full device control.",
        "defense": "1) Avoid sideloading  2) Play Protect  3) Scan links  4) Review permissions",
        "api": "Set your free VirusTotal key in Settings [7].",
        "help": "scan url · analyze file · hash · permissions · payload · defense · exit",
    }
    while True:
        try:
            user = input(f"  {C.GREEN}You › {C.RESET}").strip()
        except (EOFError, KeyboardInterrupt):
            break
        low = user.lower()
        if low in ("exit", "quit", "q", "back"):
            break
        if not user:
            continue
        if low.startswith(("http://", "https://", "scan ")):
            print(f"  {C.CYAN}Guba › {C.RESET}Use menu [1] and paste the URL")
            continue
        matched = False
        for k, v in knowledge.items():
            if k in low:
                print(f"  {C.CYAN}Guba › {C.RESET}{v}")
                matched = True
                break
        if not matched:
            print(f"  {C.CYAN}Guba › {C.RESET}Try: scan url · permissions · payload · help")
    ok("Left assistant")

def settings(cfg):
    while True:
        clear(); banner(cfg)
        title("Settings")
        key = cfg.get("vt_api_key", "")
        masked = (key[:6] + "••••" + key[-4:]) if len(key) > 12 else ("(empty)" if not key else "••••")
        user = cfg.get("username", DEFAULT_USER)
        print(f"  {C.GREEN}[1]{C.RESET}  VirusTotal API Key     {C.GRAY}{masked}{C.RESET}")
        print(f"  {C.GREEN}[2]{C.RESET}  Change Credentials     {C.GRAY}{user}{C.RESET}")
        print(f"  {C.GREEN}[3]{C.RESET}  Scan History")
        print(f"  {C.GREEN}[4]{C.RESET}  Clear History")
        print(f"  {C.GREEN}[5]{C.RESET}  View Log")
        print(f"  {C.RED}[b]{C.RESET}  Back\n")
        ch = input(f"  {C.CYAN}› {C.RESET}").strip().lower()

        if ch == "1":
            print()
            info("Free key: https://www.virustotal.com/gui/my-apikey")
            new = input(f"  {C.CYAN}API Key › {C.RESET}").strip()
            if new:
                cfg["vt_api_key"] = new
                save_config(cfg)
                ok("Saved"); log("API key updated")
            time.sleep(1)
        elif ch == "2":
            print()
            new_user = input(f"  {C.CYAN}New username (Enter = keep) › {C.RESET}").strip()
            try:
                p1 = getpass.getpass(f"  {C.CYAN}New password › {C.RESET}")
                p2 = getpass.getpass(f"  {C.CYAN}Confirm › {C.RESET}")
            except Exception:
                p1 = input(f"  {C.CYAN}New password › {C.RESET}")
                p2 = input(f"  {C.CYAN}Confirm › {C.RESET}")
            if p1 and p1 == p2:
                if new_user:
                    cfg["username"] = new_user
                cfg["password_hash"] = hashlib.sha256(p1.encode()).hexdigest()
                save_config(cfg)
                ok("Credentials updated"); log("Credentials changed")
            elif p1 != p2:
                err("Passwords do not match")
            time.sleep(1.1)
        elif ch == "3":
            clear(); title("History")
            if not HISTORY_FILE.exists():
                info("Empty")
            else:
                try:
                    with open(HISTORY_FILE) as f:
                        hist = json.load(f)
                    for i, e in enumerate(hist[:20], 1):
                        t = e.get("time", "")[:19].replace("T", " ")
                        print(f"  {C.GRAY}{i:02d}{C.RESET}  [{e.get('type','?'):4}]  {t}  {e.get('target', e.get('sha256','?'))[:45]}")
                except Exception as e:
                    err(str(e))
            pause()
        elif ch == "4":
            if HISTORY_FILE.exists():
                HISTORY_FILE.unlink(); ok("Cleared")
            else:
                info("Already empty")
            time.sleep(0.9)
        elif ch == "5":
            clear(); title("Log")
            if LOG_FILE.exists():
                with open(LOG_FILE) as f:
                    for line in f.readlines()[-25:]:
                        print(f"  {C.GRAY}{line.rstrip()}{C.RESET}")
            else:
                info("No log yet")
            pause()
        elif ch in ("b", "q", "back"):
            break

def main_menu(cfg):
    while True:
        clear(); banner(cfg)
        print(f"  {C.BOLD}Select Module{C.RESET}\n")
        print(f"  {C.CYAN}[1]{C.RESET}  URL Threat Scanner")
        print(f"  {C.CYAN}[2]{C.RESET}  File / APK Analysis")
        print(f"  {C.CYAN}[3]{C.RESET}  Hash Lookup")
        print(f"  {C.CYAN}[4]{C.RESET}  Android Permissions Guide")
        print(f"  {C.CYAN}[5]{C.RESET}  Network Health Check")
        print(f"  {C.PURPLE}[6]{C.RESET}  Defense Assistant")
        print(f"  {C.YELLOW}[7]{C.RESET}  Settings")
        print(f"  {C.RED}[q]{C.RESET}  Quit\n")
        choice = input(f"  {C.CYAN}› {C.RESET}").strip().lower()
        if choice == "1": scan_url(cfg)
        elif choice == "2": analyze_file(cfg)
        elif choice == "3": check_hash(cfg)
        elif choice == "4": permissions_guide(cfg)
        elif choice == "5": network_check(cfg)
        elif choice == "6": ai_chat(cfg)
        elif choice == "7":
            settings(cfg)
            cfg = load_config()
        elif choice in ("q", "quit", "exit"):
            print(f"\n  {C.GREEN}▸{C.RESET} Session ended. Stay safe.\n")
            sys.exit(0)
        else:
            err("Invalid choice"); time.sleep(0.6)

def main():
    ensure_dirs()
    cfg = load_config()
    save_config(cfg)
    login(cfg)
    main_menu(cfg)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n  {C.GREEN}▸{C.RESET} Stopped.\n")
        sys.exit(0)
