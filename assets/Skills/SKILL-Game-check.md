---
name: muos-game-check
description: Use when a developer is about to export or publish a Godot game targeting muOS on RG35XX devices. Runs a structured pre-export review covering exit mechanism, input mapping, display settings, renderer, performance, audio, save system, pause menu, metadata, and muOS-specific packaging requirements.
---

# muOS Game Check — Pre-Export Review

Use this skill before the developer exports their Godot game for muOS. Walk through each section below. For every item, ask the developer to confirm or check, then surface any issues before export begins.

The goal is to catch the things indie developers most commonly forget — not just Godot oversights, but muOS-specific packaging requirements that will silently break the game on device.

---

## How to run this check

Go section by section. For each item:

- Ask the developer to verify it in Godot or in the project files.
- If the answer is "I haven't done that" or "I don't know", treat it as a blocker and resolve it before moving on.
- Mark each section as clear before moving to the next.

Do not skip sections. The most dangerous issues are the ones that seem unrelated to the developer's immediate goal.

---

## Section 1 — Exit Mechanism

This is the single most commonly skipped item on handheld games. Without it the player cannot exit without hard-resetting the device.

**1.1 Quit action exists in the InputMap**

- Open Project > Project Settings > Input Map.
- Confirm an action named `quit` (or equivalent) exists.
- Confirm it is bound to at least one joypad button — not only a keyboard key.
- On RG35XX H the recommended mapping is `BTN_SELECT` + `BTN_START` chord, or the Menu/Home button (`BTN_TL2`).

**1.2 Quit action calls `get_tree().quit()`**

- Confirm there is a node in the scene tree (or an autoload) that reads the quit action every frame and calls `get_tree().quit()`.
- Example pattern:
  ```gdscript
  func _input(event):
      if event.is_action_pressed("quit"):
          get_tree().quit()
  ```

**1.3 Save before quit**

- If the game has save data, confirm the quit handler saves state before calling `get_tree().quit()`.
- Calling quit without saving first is a data loss bug.

**1.4 `NOTIFICATION_WM_CLOSE_REQUEST` handled**

- If the muOS launcher or shell script sends a close signal to the process, the game should handle it cleanly.
- Confirm the main scene or an autoload handles this:
  ```gdscript
  func _notification(what):
      if what == NOTIFICATION_WM_CLOSE_REQUEST:
          # save if needed
          get_tree().quit()
  ```

---

## Section 2 — Input Mapping

**2.1 All gameplay actions have joypad bindings**

- Open Project > Project Settings > Input Map.
- For every action used in the game (`ui_accept`, `ui_cancel`, `jump`, `attack`, etc.), confirm a joypad button or axis is bound — not only keyboard.
- Games with keyboard-only bindings are unplayable on muOS.

**2.2 RG35XX H raw input awareness**

- The RG35XX H does not follow standard SDL/Godot button label assumptions. Key non-obvious mappings:
  - Physical Y button → `BTN_C` (code 306), not `BTN_NORTH`
  - L1 → `BTN_WEST` (308), R1 → `BTN_Z` (309)
  - L2 → `BTN_SELECT` (314), R2 → `BTN_START` (315)
  - Start → `BTN_TR` (311), Select → `BTN_TL` (310)
  - Menu/Home → `BTN_TL2` (312) and `KEY_GOTO` (354)
- If the developer mapped inputs by button labels on the device case, the bindings are likely wrong.
- Run the `SKILL-Input-map` workflow to verify with `evtest` if there is any doubt.

**2.3 Analog stick deadzone set**

- Confirm `Input.action_set_deadzone()` or per-action deadzone is configured for stick actions.
- No deadzone means stick drift registers as constant input on budget analog sticks.

**2.4 D-pad uses hat input, not axis**

- On RG35XX H, the D-pad emits `ABS_HAT0X` / `ABS_HAT0Y`, not axis events.
- Confirm D-pad actions are bound to the correct hat input type in the InputMap.

---

## Section 3 — Display and Viewport

**3.1 Viewport size matches the target device**

- RG35XX H native display resolution: **640×480**.
- Open Project > Project Settings > Display > Window.
- Confirm `viewport_width` and `viewport_height` are set to the intended base resolution.
- Do not ship with the Godot default of 1152×648 unless you have intentionally designed for it.

**3.2 Stretch mode is set**

- `display/window/stretch/mode` should be `canvas_items` for pixel-art or 2D games on handheld.
- The default `disabled` mode does not scale the game if the window size differs from viewport.

**3.3 Stretch aspect is set**

- `display/window/stretch/aspect` should be `keep` (letterboxed) or `expand` (fills screen, may distort) depending on the game's design intent.
- Do not leave it at default without a deliberate choice.

**3.4 Pixel snap enabled for pixel-art games**

- If the game is pixel art, confirm both:
  - `rendering/2d/snap/snap_2d_transforms_to_pixel = true`
  - `rendering/2d/snap/snap_2d_vertices_to_pixel = true`
- Without these, sprites jitter at sub-pixel positions.

**3.5 Handheld orientation set to landscape**

- `display/window/handheld/orientation` should be `landscape` for muOS on RG35XX.

---

## Section 4 — Renderer and Performance

**4.1 Renderer is set to Compatibility**

- Open Project > Project Settings > Rendering > Renderer.
- `rendering_method` must be `gl_compatibility` (the Compatibility renderer, OpenGL ES 3.0).
- Forward+ requires Vulkan and will not run on RG35XX embedded GPU drivers.
- Mobile renderer may also fail on this hardware.

**4.2 Max FPS is capped**

- Without a frame cap, Godot runs as fast as possible, consuming all CPU/GPU.
- On a constrained handheld this causes thermal throttling, battery drain, and inconsistent timing.
- Confirm `application/run/max_fps` is set. A value of `60` is a safe starting point.
- Alternatively confirm `Engine.max_fps` is set in code at startup.

**4.3 V-sync behavior is intentional**

- V-sync on embedded Linux is unpredictable and can cause frame pacing issues on muOS.
- Confirm `display/window/vsync/vsync_mode` is set deliberately, not left at default.
- Disabling v-sync and relying on the frame cap is often more stable on this hardware.

**4.4 Texture compression matches the export target**

- For Linux ARM Compatibility export, textures should use ETC2 compression.
- Confirm the export preset's texture compression setting is not left at the desktop default (BPTC/S3TC).

---

## Section 5 — Audio

**5.1 Audio bus layout is configured**

- Open the Audio panel (bottom bar).
- Confirm there is at least a Master bus, and ideally separate Music and SFX buses.
- A game with only a single Master bus cannot offer volume controls per category.

**5.2 Volume controls use `linear_to_db()` conversion**

- If the game has a settings menu with volume sliders, confirm the slider value is converted with `linear_to_db()` before passing to `AudioServer.set_bus_volume_db()`.
- Passing a raw linear 0.0–1.0 value to a dB parameter produces a perceptually wrong curve.

**5.3 Volume settings are saved and restored**

- Confirm volume preferences are written to a save file (ConfigFile or similar) and restored on startup.

**5.4 Audio driver compatibility**

- On muOS, the default PulseAudio driver may not be available.
- If the game has no audio on device, the launcher script may need `--audio-driver ALSA` or `--audio-driver Dummy` passed to the runtime.
- Note this as a potential first-boot issue to check during device testing.

---

## Section 6 — Save System

**6.1 `user://` path is reliable on muOS**

- On muOS, `$HOME` may be overridden by the Simple Terminal or launcher environment.
- Godot's `user://` path resolves through `$HOME`. If `$HOME` is wrong, save files land in the wrong place or fail to write.
- Confirm the launcher script sets `HOME=/root` before invoking the runtime, or that save files are written to a path relative to the game bundle using an absolute hardcoded base path.

**6.2 File write errors are handled**

- Confirm `FileAccess.open()` return values are checked for null.
- Confirm `ResourceSaver.save()` return values are checked.
- Silent save failures leave players with lost data and no error message.

**6.3 Save-on-quit is implemented**

- Confirm progress is saved when the game exits, not only at manual checkpoints.

---

## Section 7 — Pause Menu

**7.1 A pause menu exists**

- Confirm the game has a pause state the player can enter and exit.

**7.2 Pause menu node has correct `process_mode`**

- The pause menu node must have `process_mode` set to `PROCESS_MODE_WHEN_PAUSED`.
- Without this, calling `get_tree().paused = true` freezes the pause menu itself, making it unresponsive.

**7.3 Pause menu is fully joypad-navigable**

- Confirm every button in the pause menu can be reached and activated using D-pad and face buttons alone.
- Mouse-only or keyboard-only navigation is not usable on muOS.

**7.4 Pause menu includes a quit option**

- The pause menu should offer "Quit to Main Menu" and/or "Quit Game" so the player has an in-game exit path beyond the hardware quit action.

---

## Section 8 — Application Metadata

**8.1 Project name is set**

- Open Project > Project Settings > Application > Config.
- Confirm `name` is not "Unnamed Project" or a leftover test value.
- This name appears in the muOS launcher menu.

**8.2 Custom icon is set**

- Confirm `icon.png` at project root has been replaced with a game-specific image.
- The default Godot icon ships if this is not replaced.

**8.3 Version string is set**

- Confirm `application/config/version` is set in project settings.
- Include this in the export archive filename and in `port.json`.

---

## Section 9 — Export Preset

**9.1 Export templates are installed and version-matched**

- Confirm export templates are installed via Editor > Manage Export Templates.
- Confirm the template version exactly matches the editor version.
- Mismatched templates cause silent export failures or crashes on launch.

**9.2 A Linux ARM64 export preset exists**

- Confirm there is an export preset configured for Linux with architecture `arm64`.
- Exporting x86_64 and running it on RG35XX produces an "Exec format error".

**9.3 Export is set to Release mode**

- Confirm the export preset uses the Release template, not Debug.
- Debug exports include the editor console and are slow.

**9.4 Script export mode is intentional**

- `script_export_mode`: `0` = plain text (source visible), `1` = binary tokens, `2` = bytecode.
- Confirm the choice is deliberate. Mode `0` ships full GDScript source to players.

**9.5 Export filters exclude dev assets**

- Confirm the export exclude filter removes test scenes, editor scripts, and dev-only assets from the PCK.

---

## Section 10 — muOS Packaging Requirements

**10.1 Correct Ports directory structure**

muOS expects this exact layout on the SD card:

```
/mnt/sdcard/roms/Ports/<GameName>.sh        ← menu-visible launcher
/mnt/sdcard/ports/<gameslug>/launch.sh      ← actual launch logic
/mnt/sdcard/ports/<gameslug>/game/<game>.pck
/mnt/sdcard/ports/<gameslug>/godot_runtime  ← ARM64 runtime binary
```

A flat directory dump does not appear in the muOS Ports menu.

**10.2 ARM64 Godot runtime is included**

- A `.pck` file cannot launch itself. The ARM64 Linux Godot runtime binary must be present in the bundle.
- Confirm the runtime is present and is the ARM64 Linux build, not x86_64.
- Reference the launcher script to confirm it points to the correct runtime binary path.

**10.3 All shell scripts and the runtime are executable**

- Files copied from macOS via FAT32 SD card may lose execute permissions.
- The launcher script must explicitly `chmod +x` the runtime and launcher after copy, or the developer must run it manually after placing files on the device.
- Confirm `chmod +x` is part of the install instructions.

**10.4 `gptokeyb` config is present and launcher starts it**

- On muOS, `gptokeyb` translates joypad input into SDL/keyboard events that Godot can read.
- Confirm a `.gptk` config file exists in the bundle.
- Confirm the launcher script starts `gptokeyb` before launching the game binary.
- Confirm the launcher script kills `gptokeyb` after the game exits (capture the PID, kill on exit).

**10.5 Launcher script uses dynamic path resolution**

- Confirm the launcher script uses `$(dirname "$0")` or equivalent to build paths, not hardcoded `/mnt/sdcard/...` paths.
- Hardcoded paths break if the SD card mounts at a different path.

**10.6 Launcher script sets `HOME=/root`**

- Confirm the launcher script exports `HOME=/root` before invoking the runtime.
- This prevents `user://` save files from landing in an unexpected location on muOS.

**10.7 `port.json` exists in the payload folder**

- A `port.json` metadata file in `/ports/<gameslug>/` improves PortMaster compatibility and future tooling support.
- Minimum fields: `name`, `version`, `description`, `porter`, `runtime`.

**10.8 SSH test passes before menu test**

- Before asking the developer to launch from the muOS Ports menu, confirm the game runs successfully from an SSH terminal.
- A menu launch failure with no prior SSH test produces confusing signal.

---

## Section 11 — Final Pre-Export Checklist Summary

Print this summary once all sections are reviewed:

| # | Item | Status |
|---|------|--------|
| 1 | Quit action bound to joypad and calls `get_tree().quit()` | |
| 2 | Save-before-quit implemented | |
| 3 | `NOTIFICATION_WM_CLOSE_REQUEST` handled | |
| 4 | All gameplay actions have joypad bindings | |
| 5 | Input bindings verified against real RG35XX H evdev data | |
| 6 | Analog stick deadzone configured | |
| 7 | Viewport size set to 640×480 | |
| 8 | Stretch mode and aspect set | |
| 9 | Renderer set to Compatibility | |
| 10 | Max FPS capped | |
| 11 | Audio buses configured | |
| 12 | Volume settings saved/restored | |
| 13 | `user://` save path reliable (HOME set in launcher) | |
| 14 | Pause menu exists and is joypad-navigable | |
| 15 | Project name, icon, and version set | |
| 16 | Linux ARM64 export preset configured | |
| 17 | Export templates installed and version-matched | |
| 18 | Ports directory structure correct for muOS | |
| 19 | ARM64 runtime included in bundle | |
| 20 | Shell scripts and runtime marked executable | |
| 21 | gptokeyb config present and launcher manages it | |
| 22 | SSH test passes before menu launch test | |

All items must be confirmed before export. Do not export with open unknowns — each one is a likely silent failure on device.
