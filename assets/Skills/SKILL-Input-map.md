---
name: muos-map-input
description: Use when a developer needs to map handheld controls for a game running on muOS, especially on RG35XX-style devices. Guides the agent through raw input capture with evtest, in-engine verification, interpretation of D-pad, face buttons, shoulders, triggers, stick axes, stick clicks, and turning the results into game or engine mappings without confusing Linux evdev codes with Godot or SDL button indices.
---

# muOS Map Input

Use this skill when a developer needs help figuring out what buttons, sticks, triggers, or menu controls a muOS handheld is actually sending.

## Goal

Build a reliable control map from real device data, then use it to update a game, launcher, `gptokeyb` config, or engine/plugin input preset.

## First distinction

Always separate these two questions:

1. What raw Linux input events does the device emit?
2. What input events does the game engine see?

Do not assume those are identical.

Important rule:

- `evtest` gives Linux evdev truth.
- Godot input actions depend on how the runtime maps those controls.
- For standard controls, evdev and engine behavior may align closely.
- For unusual handheld layouts, they may not.

## Preferred workflow

1. Identify the correct input device.
2. Capture raw events with `evtest`.
3. Run a structured button test in a fixed order.
4. Run a second focused pass for ambiguous controls.
5. If the target is Godot or another engine, do an in-engine verification pass for nonstandard buttons.
6. Produce a final mapping table with confidence notes.

## Finding the device

On the device over SSH, prefer:

```sh
which evtest || echo "evtest not installed"
cat /proc/bus/input/devices
ls -lah /dev/input
```

Explain each command briefly when giving it to the user.

Look for:

- the handheld gamepad-like device name
- `js0`
- matching `eventX`

## Structured test method

Use fixed-order capture so the output is easy to interpret.

Recommended full pass:

1. D-pad Up
2. D-pad Down
3. D-pad Left
4. D-pad Right
5. A
6. B
7. X
8. Y
9. L1
10. R1
11. L2
12. R2
13. Start
14. Select
15. Menu/Home

For uncertain controls, ask for a focused second pass.

## Best capture style

For clean `evtest` logs:

- press each control more than once
- pause about 1 second between repeated presses
- pause about 3-4 seconds before moving to the next control

This makes grouping much easier when reading timestamps.

For analog sticks:

- test left, right, up, down separately
- return to center after each movement
- test stick clicks separately

## Reading the results

Interpret:

- `EV_KEY` as button-style events
- `EV_ABS` as D-pad hats, sticks, or trigger-like axes

Common patterns:

- `ABS_HAT0X` / `ABS_HAT0Y` often mean D-pad
- signed axis extremes usually indicate stick directions
- extra keys like `KEY_GOTO` may appear alongside a special menu button

## Godot-specific warning

If the developer wants to update a Godot input preset:

- do not assume raw evdev codes directly equal Godot `JOY_BUTTON_*` indices
- use `evtest` for raw truth
- use a Godot-side tester or targeted game behavior check to confirm how Godot exposes nonstandard controls

It is safe to be confident about:

- raw D-pad hat directions
- repeated raw key/button identities
- repeated raw axis identities

Be cautious about:

- special handheld buttons
- stick clicks
- nonstandard shoulder/trigger labels
- any attempt to translate raw evdev names directly into Godot constants without verification

## Deliverable

End with a flat table:

- physical control
- raw event
- interpretation confidence
- engine mapping status

Then recommend one of:

- update the game mapping now
- update the engine/plugin preset now
- do one last in-engine verification pass for unresolved controls

## Reference map: measured RG35XX H on muOS

This is a real measured raw-input reference collected from an RG35XX H on muOS using `evtest` against `/dev/input/event1`.

Use it as a starting point, not as universal truth.

Raw input map:

- D-pad Up: `ABS_HAT0Y = -1`
- D-pad Down: `ABS_HAT0Y = 1`
- D-pad Left: `ABS_HAT0X = -1`
- D-pad Right: `ABS_HAT0X = 1`
- A: `BTN_SOUTH` (`304`)
- B: `BTN_EAST` (`305`)
- X: `BTN_NORTH` (`307`)
- Y: `BTN_C` (`306`)
- L1: `BTN_WEST` (`308`)
- R1: `BTN_Z` (`309`)
- L2: `BTN_SELECT` (`314`)
- R2: `BTN_START` (`315`)
- Start: `BTN_TR` (`311`)
- Select: `BTN_TL` (`310`)
- Menu/Home: `BTN_TL2` (`312`) and also `KEY_GOTO` (`354`)
- Left stick click: `BTN_TR2` (`313`)
- Right stick click: `BTN_MODE` (`316`)
- Left stick horizontal: `ABS_Z` negative/positive
- Right stick horizontal: `ABS_RX` negative/positive
- Right stick vertical: `ABS_RY` negative/positive
- Additional vertical-style axis observed: `ABS_RZ` negative/positive

Important note:

- This map is raw Linux evdev data.
- Do not assume it directly equals Godot `JOY_BUTTON_*` indices or SDL labels.
- If the developer needs to remap controls for a different device, a different runtime, or a different engine path, rerun the exact capture process in this skill rather than guessing from the table above.
