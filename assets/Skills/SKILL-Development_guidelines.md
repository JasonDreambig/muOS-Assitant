---
name: development-guidelines
description: Use when choosing a tech stack or app architecture for a new muOS app or game — covers shell/GMUI, native C/SDL2, Python, cross-compilation requirements, and PortMaster runtime patterns.
---

# muOS Development Guidelines

## Standard Application Architecture
On muOS, "Applications" are fundamentally treated as standard Linux executables or shell scripts that can be invoked directly from the operating system's main interface.

Native muOS applications are stored in:
`[SD CARD]/MUOS/application/`

### The Launcher Script
Every app must have an entry point (usually a `.sh` shell script). This script is placed inside an application folder and handles launching the actual binary or python script.

```bash
#!/bin/sh
# Example launcher script for muOS
export SDL_VIDEODRIVER="fbcon"
export SDL_RENDER_DRIVER="software"
export HOME="/mnt/sdcard/MUOS/application/MyApp"

cd "${HOME}"
# Launch the C executable or Python interpreter
./my_app_binary
```

## Tech Stack Options

### 1. Bash / GMUI (Text-Only)
The easiest way to write native utility apps is using bash.
- **Tools**: `gmui` or `dialog`
- **Output**: Terminal-style menus.
- **Pros**: Perfectly native, incredibly lightweight, reads settings easily.
- **Cons**: Cannot render pictures, GUI elements, or custom fonts.

### 2. Native C / C++ with SDL2 (The Standard)
If you want rich graphics, building a binary executable targeting the Anbernic hardware via SDL2 is the ideal path.
- **Tools**: `make`, `gcc`, `SDL2`, `SDL2_image`
- **Architecture target**: `aarch64-linux-gnu` (ARM64)
- **Compilation**: Because the console doesn't have a built-in compiler, you must use a Cross-Compiler via Docker or Homebrew on a Mac/PC workstation. The compiled binary is then transferred to the console.
- **Pros**: Lightning fast, direct hardware access, tiny file payloads (< 500kb).
- **Cons**: Requires complex memory management and strict compilation toolchains.

### 3. Interpreted Languages (Python)
muOS includes natively pre-installed interpreters like Python 3.
- **Tools**: Python 3.11, standard libraries (`urllib`, `os`, `zipfile`).
- **Caveats**: Barebones muOS does **not** include graphical Python libraries (like Pygame or Tkinter), and it lacks the `pip` package manager.
- **The Workaround**: To build GUI apps in Python, you must manually download the pre-compiled `aarch64` Linux wheel for your specific library (e.g., Pygame) and package it *directly* alongside your `.py` scripts so it loads locally. 

## Best Practices
- **Network Requests**: Heavily rely on lightweight APIs (`urllib` in Python, or native `wget`/`curl` shell commands in C).
- **Video Previews**: Avoid compiling enormous decoding engines like `ffmpeg` into your binaries. Instead, use OS-level calls to natively installed video players (`mpv` or `ffplay`) and let the console handle decoding!
- **Testing**: Using SSH or `adb shell` on a wired connection is required to debug. 
- **PortMaster Ecosystem**: For games specifically, adhering to PortMaster script structures (`/mnt/sdcard/ROMS/PORTS/`) enables muOS to leverage their vast pre-installed library runtimes (e.g. `libpython3`, `mono`, `godot`) automatically.
