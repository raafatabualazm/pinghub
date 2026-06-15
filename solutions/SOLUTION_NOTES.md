# pinghub — demo answer key

Three planted flaws, one per gate. Each is the same red → fix → green loop the
students will repeat on PayFlow.

| Flaw | File | Gate / tool | Fix |
|------|------|-------------|-----|
| Command injection (CWE-78) | `app.py` `/ping` | SAST · Semgrep | `app.fixed.py` — validate input, `subprocess.run([...])`, no shell |
| Committed secret | `.env` | Secret scan · Gitleaks | add `.env` to `.gitignore`, `git rm --cached .env`, rotate the key |
| Vulnerable dependency | `requirements.txt` (`requests==2.19.1`) | SCA · Trivy | bump to `requests==2.32.3`; re-scan |

**Removing the secret properly:**
```bash
echo ".env" >> .gitignore
git rm --cached .env
git commit -m "stop tracking secrets"
# real life: also rotate the leaked key and scrub git history (git filter-repo / BFG)
```
