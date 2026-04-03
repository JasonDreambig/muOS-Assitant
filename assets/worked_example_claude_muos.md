# Worked Example: claude-muOS

This documents the full journey of building and shipping the claude-muOS app using the MuOS AppBuilder workflow. Use this as a reference when applying the workflow to new projects.

---

## Project Overview

**App name:** claude-muOS
**Goal:** On-device AI debugging assistant — lets users diagnose muOS problems over SSH without a laptop
**Device target:** Anbernic RG35XX, muOS 2601.0 JACARANDA
**Package type:** System binary (`/usr/bin/claude-muos`) + install script
**Final version shipped:** v1.5.0
**Distribution:** GitHub releases + itch.io

---

## Step 1: Define the App

**Idea:** A shell script that calls the Anthropic API via `curl` to answer muOS debugging questions. Runs over SSH or in Simple Terminal. Zero external dependencies.

**Constraints identified upfront:**
- Must be POSIX sh only (muOS has busybox, not bash)
- Must use `curl` (already on device)
- Config cannot use `$HOME` — Simple Terminal overrides HOME
- Must install to `/usr/bin/` not `/usr/local/bin/` (not in muOS PATH)

**Key unknown:** Does `curl` support HTTPS on this device? (Answer: yes, via OpenSSL)

---

## Step 2: Identify Integration Type

**Chosen type:** System binary (not Applications entry)
**Reason:** Designed for SSH use, not handheld UI. Install to `/usr/bin/claude-muos` so it's callable from any shell.

---

## Step 3: Prove the Manual Sequence

First working version was a minimal curl call:

```sh
curl -s -X POST https://api.anthropic.com/v1/messages \
  -H "x-api-key: $API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{"model":"claude-sonnet-4-6","max_tokens":1024,"messages":[{"role":"user","content":"hello"}]}'
```

Tested over SSH — confirmed the device could reach the API and parse JSON responses with `grep`/`sed`.

---

## Step 4: Inspect muOS Integration Points

Not heavily needed for this app — it's a terminal tool, not a UI app. Key finding:

- `$HOME` is unreliable from Simple Terminal — hardcode config to `/root/.claude.conf`
- `/tmp/` is writable and suitable for session history files (auto-cleaned on reboot)

---

## Step 5: Turn the Manual Flow Into Scripts

**v1.0 — Core loop:**
- Read API key from `/root/.claude.conf`
- `gather_context()` — collect device info (uname, muOS version, storage, processes) for first message
- Single-shot mode (`claude-muos "question"`) and interactive chat mode
- Rolling 6-turn conversation history in `/tmp/claude-history-$$` (deleted on exit)

**v1.4 — Added system prompt with full muOS filesystem map**
Embedded into the script so Claude always has device context.

**v1.5 — Added persistent memory:**
- `/root/.claude-memory.md` — auto-summary saved every 4 assistant turns
- `load_memory()` — prepended to gather_context on every session start
- `save_memory()` — quiet API call, max_tokens 512, writes 3-5 bullet summary
- Chat commands: `/memory` (view), `/clear-memory` (wipe)

**Key `<run>` block feature:**
Claude can propose commands wrapped in `<run>...</run>`. User must approve before execution. Parsed with `sed`, executed with `sh -c`.

---

## Step 6: Package It

**Chosen packaging path:** Install script + single binary

```
ai-app/
  claude-muOS.sh     — the main script (installed to /usr/bin/claude-muos)
  install.sh         — copies script, sets permissions, writes config template
```

**install.sh key steps:**
1. Copy `claude-muOS.sh` to `/usr/bin/claude-muos`
2. `chmod +x /usr/bin/claude-muos`
3. Write `/root/.claude.conf` with `API_KEY=` placeholder if not present
4. Print instructions for adding API key

**Update workflow (no reinstall needed):**
```bash
scp claude-muOS.sh root@10.0.1.49:/usr/bin/claude-muos
```

---

## Step 7: Verify On-Device

```bash
ssh root@10.0.1.49 "claude-muos --help"
ssh root@10.0.1.49 "claude-muos --version"
ssh root@10.0.1.49 "claude-muos 'what muOS version am I running?'"
```

Fresh boot verified: config persists, memory loads on startup, history cleared cleanly.

---

## Step 8: Document It

**README covers:**
- Requirements (muOS device, Anthropic API key, SSH access)
- Install steps (run install.sh, add API key to `/root/.claude.conf`)
- Usage: single-shot and chat modes
- Chat commands (`/memory`, `/clear-memory`, `/help`, `/exit`)
- `<run>` block approval flow
- Version history

---

## Step 9: Release

**GitHub:** `https://github.com/JasonDreambig/claude-muos`
**Package:** `claude-muos-v1.5.0.zip` containing source + install script
**Next:** itch.io page, muOS Discord and Reddit announcement

---

## Key Lessons From This Project

1. **Hardcode paths, never trust `$HOME`** — Simple Terminal breaks HOME. Always use `/root/`.
2. **POSIX sh only** — No `[[`, no arrays, no bash process substitution. Test with `sh`, not `bash`.
3. **`/usr/bin/` not `/usr/local/bin/`** — muOS PATH does not include `/usr/local/bin/`.
4. **Temp files for session state, persistent files for memory** — `/tmp/` is fine for per-session history. Use `/root/` for anything that should survive reboots.
5. **Keep API calls minimal** — The memory save is a separate quiet call (max_tokens 512). Don't bloat the main conversation call.
6. **`<run>` approval is essential** — Never auto-execute AI-proposed commands. Always prompt the user.
7. **gather_context() is the killer feature** — Sending real device state on the first message makes every session immediately useful.

---

## Reusable Patterns From This Project

| Pattern | Lesson |
|---|---|
| Config at `/root/.app.conf` | Safe from HOME override, survives reboots |
| Temp history in `/tmp/appname-$$` | Session-scoped, auto-cleaned |
| Persistent memory in `/root/.app-memory.md` | Cross-session context |
| Install to `/usr/bin/` | Globally accessible in muOS PATH |
| POSIX sh, no external deps | Works on stock muOS busybox |
| gather_context() on first turn | Real device state → better AI responses |
| Rolling N-turn history window | Keeps API payload size manageable |
