---
name: muos-import-game
description: Use when deploying or importing a game or native port onto muOS, especially for manual PortMaster-style installs on RG35XX devices. Covers the correct ports folder structure, SD2 deployment assumptions, launcher placement, SSH/SCP copy flow, permissions, and first-run log collection.
---

# muOS Import Game

Use this skill when the task is to place a game, runtime, or native port onto a muOS device by hand.

## What to assume first

- Prefer the current MustardOS / PortMaster-style split layout.
- Ask the user first if they save their games on SD1 or SD2. If the user says their games live on the second SD card, assume SD2 is the target.
- In this workflow, SD2 is commonly mounted at `/mnt/sdcard`.
- Do not default to an all-in-one `ROMS/Ports/<game>/...` payload layout unless the user explicitly wants a legacy/custom structure.

## Correct folder structure

For a manually installed port:

- Payload files go in `/ports/<portname>/`
- Visible launcher script goes in `/roms/Ports/<Launcher>.sh`

Typical device paths when targeting SD2:

- payload: `/mnt/sdcard/ports/<portname>/`
- launcher: `/mnt/sdcard/roms/Ports/<Launcher>.sh`

Example:

- payload folder: `/mnt/sdcard/ports/pingpong/`
- launcher script: `/mnt/sdcard/roms/Ports/PingPong.sh`

## Typical payload contents

Put the runnable files in the payload folder, for example:

- runtime binary such as `godot_runtime`
- game pack such as `PingPong.pck`
- optional support files, assets, config, or logs

## Runtime location rule

There are two different runtime patterns on muOS and they should not be mixed up.

For a custom self-contained test port:

- keep the runtime inside the payload folder
- example: `/mnt/sdcard/ports/pingpong/godot_runtime`

For shared PortMaster-managed runtimes:

- MustardOS / PortMaster may store runtime `.squashfs` files under `MUOS/PortMaster/libs`
- that is a different model from a self-contained custom runtime test

For Godot 4 custom runtime experiments like this project:

- prefer the self-contained payload model first
- place the runtime next to the `.pck` inside `/ports/<portname>/`
- do not assume the runtime belongs in `MUOS/PortMaster/libs` unless the project is explicitly being converted into a true shared PortMaster runtime

## Launcher pattern

The launcher should enter the payload directory, then run the runtime or binary from there.

Example:

```sh
#!/bin/sh
set -eu
PORTDIR="/mnt/sdcard/ports/pingpong"
cd "$PORTDIR"
./godot_runtime --main-pack PingPong.pck > log.txt 2>&1
```

Notes:

- Redirecting output to `log.txt` is useful for first-run debugging.
- If the launch fails, inspect `/mnt/sdcard/ports/<portname>/log.txt`.

## SSH / SCP deployment workflow

When the user wants to copy files from their computer to the device, use this sequence:

1. Open an SSH session to the device in one terminal window and keep it open.
2. In that SSH terminal, inspect the existing folder layout before creating anything new.
3. Create the payload and launcher directories on the device only if needed.
2. Copy payload files into `/mnt/sdcard/ports/<portname>/`.
3. Create or copy the launcher into `/mnt/sdcard/roms/Ports/`.
4. `chmod +x` the runtime and launcher.
5. Test over SSH before asking the user to launch from the menu.

Be explicit about where each command runs:

- Commands starting with `ssh muOS ...` or `scp ... muOS:...` are run on the Mac terminal.
- Commands shown without `ssh muOS` are meant to be run inside the already-open SSH terminal on the device.

Recommended two-terminal workflow:

- Terminal A on Mac: open `ssh muOS` and keep that remote shell open.
- Terminal B on Mac: use `scp` and any additional `ssh muOS '...'` one-shot commands.

Inside the SSH terminal, inspect first:

```sh
ls -lah /mnt/sdcard
ls -lah /mnt/sdcard/ports 2>/dev/null || echo "/mnt/sdcard/ports does not exist yet"
ls -lah /mnt/sdcard/roms/Ports 2>/dev/null || echo "/mnt/sdcard/roms/Ports does not exist yet"
```

Then create missing folders if needed:

```sh
mkdir -p /mnt/sdcard/ports/pingpong
mkdir -p /mnt/sdcard/roms/Ports
```

Then, from the Mac terminal, copy the files:

```sh
scp local/godot_runtime muOS:/mnt/sdcard/ports/pingpong/
scp local/PingPong.pck muOS:/mnt/sdcard/ports/pingpong/
```

Then either create the launcher inside the SSH terminal or push it from the Mac.

Create it inside the SSH terminal:

```sh
cat > /mnt/sdcard/roms/Ports/PingPong.sh <<'EOF'
#!/bin/sh
set -eu
PORTDIR="/mnt/sdcard/ports/pingpong"
cd "$PORTDIR"
./godot_runtime --main-pack PingPong.pck > log.txt 2>&1
EOF
chmod +x /mnt/sdcard/roms/Ports/PingPong.sh
chmod +x /mnt/sdcard/ports/pingpong/godot_runtime
```

Reference example using one-shot Mac commands:

```sh
ssh muOS 'mkdir -p /mnt/sdcard/ports/pingpong /mnt/sdcard/roms/Ports'
scp local/godot_runtime muOS:/mnt/sdcard/ports/pingpong/
scp local/PingPong.pck muOS:/mnt/sdcard/ports/pingpong/
ssh muOS "cat > /mnt/sdcard/roms/Ports/PingPong.sh <<'EOF'
#!/bin/sh
set -eu
PORTDIR=\"/mnt/sdcard/ports/pingpong\"
cd \"\$PORTDIR\"
./godot_runtime --main-pack PingPong.pck > log.txt 2>&1
EOF
chmod +x /mnt/sdcard/roms/Ports/PingPong.sh
chmod +x /mnt/sdcard/ports/pingpong/godot_runtime"
```

## First-run verification

Before telling the user to launch from the menu, prefer an SSH test:

Inside the open SSH terminal:

```sh
cd /mnt/sdcard/ports/pingpong
./godot_runtime --main-pack PingPong.pck
```

If it fails, collect:

Inside the SSH terminal:

```sh
cat /mnt/sdcard/ports/pingpong/log.txt 2>/dev/null || echo "No log.txt yet"
```

## Practical reminders

- Use lowercase payload folder names unless the port specifically expects otherwise.
- Keep the launcher filename user-friendly, for example `PingPong.sh`.
- If the user is unsure whether SD2 is mounted at `/mnt/sdcard`, verify on-device before copying.
- Prefer keeping one SSH terminal open and using a second Mac terminal for `scp`.
- Tell the user explicitly which commands belong in the Mac terminal and which belong in the SSH terminal.
- If a menu entry appears but does not launch, the next checks are:
  - launcher permissions
  - runtime permissions
  - path correctness
  - `log.txt`

## What not to forget

- The split layout matters.
- SD2 targeting matters.
- Self-contained custom runtimes live in the payload folder, not in `MUOS/PortMaster/libs`.
- Test over SSH before concluding the menu integration is broken.
