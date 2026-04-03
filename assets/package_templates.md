# MuOS Packaging Templates

## Template 1: Simple Terminal Helper

Use when:

- proving a concept
- debugging live over SSH
- building the first working version

Suggested layout:

```text
simple-terminal-app/
  README.md
  install.sh
  bin/
    app-start
    app-status
    app-stop
    app-menu
```

## Template 2: Applications Wrapper

Use when:

- the backend scripts work
- you want it visible in muOS `Applications`

Suggested layout:

```text
muos-wrapper/
  App Name.sh
  README.md
```

Launcher target:

```bash
/opt/app-name/bin/app-menu
```

## Template 3: Archive Package Plan

Use when:

- the app is ready for sharing
- you want GitHub releases and Archive Manager installation

Suggested contents:

```text
app-package/
  manifest or metadata
  launcher
  payload/
  README.md
  icons/
```

Possible future formats:

- `.muxapp`
- `.muxzip`
- `.muxupd`

## Template 4: AI Memory Layout

Use for every muOS app project:

```text
Ai-memory/
  README.md
  project_memory_report.md
  decisions.md
  next_steps.md
  session_log.md
```
