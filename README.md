# pinghub — DevSecOps demo app

A tiny (~25-line) Flask service used as a **live instructor demo** before students
work the full PayFlow lab. It carries **three planted flaws**, one per gate, so the
class can watch the whole *add gate → fail on a real finding → fix → pass* loop
once before doing it themselves.

> ⚠️ Insecure on purpose. Fake credentials, but real patterns. Don't deploy it.

| Flaw | File | Gate |
|------|------|------|
| Command injection | `app.py` | SAST (Semgrep) |
| Committed secret | `.env` | Secret scan (Gitleaks) |
| Vulnerable dependency | `requirements.txt` | SCA (Trivy) |

Same toolchain and pipeline shape as PayFlow — only smaller and faster, so it runs
in ~15 minutes at the front of the room.

- **`DEMO_SCRIPT.md`** — the minute-by-minute presenter walkthrough (run this).
- **`solutions/`** — fixed app, fixed requirements, finished pipeline, answer key.

Run the app (optional): `pip install -r requirements.txt && python app.py`
# pinghub
