# pinghub — Instructor Demo Script

**When:** right before Lab 1 (≈ 15 min). **Who drives:** you. Students watch.
**Goal:** make the red → fix → green loop muscle-memory *before* they hit PayFlow.

**Why run scans locally (not in CI) for the demo:** it's instant and doesn't depend
on runner queue times or wifi. Push to GitHub Actions only as the capstone at the
end. Have the CLIs installed: `gitleaks`, `semgrep`, `trivy`.

**Pre-flight (do before class):**
- Repo cloned, terminal + editor + browser visible on the projector.
- `gitleaks version && semgrep --version && trivy --version` all work.
- Pre-pull Trivy's DB once (`trivy fs .` on any folder) so the live run is fast.
- Font size up; one terminal, one editor pane.

---

## Beat 0 — Meet the app  *(~2 min)*

Open `app.py` on screen. It's ~25 lines.

> "This is the entire app. One endpoint pings a host. There's a bug you can
> probably already see — and two more you can't. Let's let the pipeline find all
> three. Watch the pattern, because you'll repeat it on a much bigger app after
> lunch."

Point at the `/ping` line. Don't explain the fix yet.

---

## Beat 1 — Secret scanning  *(~3 min)*

> "Gate one: secrets. Never let a credential reach git."

```bash
gitleaks detect --no-banner -v
```

**Students see:** ❌ a finding for the AWS key in `.env`.

> "There it is — a committed credential. And here's the kicker: even if I delete
> the line now, it stays in git history forever. Deleting isn't fixing."

**Fix it live:**
```bash
echo ".env" >> .gitignore
git rm --cached .env
gitleaks detect --no-banner        # exits clean
```

> "Stop tracking it, and in real life rotate the key and scrub history. Gate green."

---

## Beat 2 — SAST  *(~4 min)*

> "Gate two: static analysis of our own code."

```bash
semgrep scan --config p/owasp-top-ten --config p/python
```

**Students see:** ❌ a **command-injection** finding on the `os.popen(f"ping ... {host}")`
line.

> "User input goes straight into a shell command. `?host=8.8.8.8; rm -rf /` and the
> server runs it. Semgrep caught it without running the app — that's the point of
> static analysis."

**Fix it live** — replace the body of `/ping` with the safe version from
`solutions/app.fixed.py` (validate the IP, `subprocess.run([...])`, no shell):

```bash
semgrep scan --config p/owasp-top-ten --config p/python   # clean
```

> "Argument list instead of a shell string. Input validated. No interpolation. Gate
> green."

---

## Beat 3 — SCA  *(~3 min)*

> "Gate three: the code we *didn't* write — our dependencies."

```bash
trivy fs --severity HIGH,CRITICAL .
```

**Students see:** ❌ CVEs for **`requests==2.19.1`** (and its transitive deps).

> "We wrote none of this, but we ship it, so we own it. Most real-world breaches
> ride in on an old dependency, not a clever bug in your code."

**Fix it live** — bump the pin in `requirements.txt` to `requests==2.32.3`:

```bash
trivy fs --severity HIGH,CRITICAL .    # clean
```

> "Gate green. Three gates, three real findings, three fixes."

---

## Beat 4 — Same thing, in CI  *(~2 min)*

Drop `solutions/security.yml` into `.github/workflows/`, commit, push, open the
**Actions** tab.

> "Exactly what we just did by hand, now automatic on every push: three jobs,
> failing the build on real findings. This is your finish line."

---

## The handoff to PayFlow

> "That loop — **add a gate, watch it go red on something real, fix it, watch it go
> green** — is the entire afternoon. PayFlow is bigger: a Spring Boot app with eight
> planted flaws across secrets, SAST, SCA, containers, infrastructure, and Kubernetes
> policy. Same tools. Same loop. Different language — notice the pipeline didn't
> care. Open `LAB_GUIDE.md` and start at Lab 0. Go."

---

## Timing

| Beat | Content | Time |
|------|---------|------|
| 0 | Meet the app | 2m |
| 1 | Secrets (Gitleaks) | 3m |
| 2 | SAST (Semgrep) | 4m |
| 3 | SCA (Trivy) | 3m |
| 4 | Same thing in CI | 2m |
| | **Total** | **~14m** |

## If something goes sideways

- **Trivy slow / DB download:** you pre-pulled it; if not, talk through Beat 0 while
  it finishes.
- **No internet:** Gitleaks and the local Semgrep registry rules cache work offline
  after first use; skip Beat 4 (CI) and describe it from `solutions/security.yml`.
- **A scan finds *more* than expected:** great — that's the triage lesson early.
  "Not every finding blocks; we decide which matter. More on that in Lab 1."

## Likely questions

- *"Why three tools instead of one?"* Different lenses: secrets ≠ your code ≠ your
  dependencies. Each is blind to the others' bugs.
- *"Won't this slow developers down?"* Only if it's noisy. We block on high-confidence
  findings and warn on the rest — you'll set that threshold yourself in Lab 1.
- *"Does this work for Java/Go/JS?"* Yes — you're about to do it on Java. The tools and
  the gate placement are what transfer, not the language.
