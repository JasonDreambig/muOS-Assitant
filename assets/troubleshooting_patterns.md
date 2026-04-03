# MuOS Troubleshooting Patterns

## Pattern 1: Binary exists, feature does not work

Meaning:

- required binary may exist
- daemon or init process may still be missing

Examples:

- `bluetoothctl` exists but `bluetoothd` is not running
- tool exists but firmware/init step is missing

## Pattern 2: Manual flow works, packaged flow does not

Meaning:

- environment differs
- paths differ
- background process handling differs
- UI wrapper is not launching the same commands

Recommended response:

- compare exact manual commands with packaged script
- add logs
- confirm working directory and environment

## Pattern 3: UI icon or status does not match real state

Meaning:

- muOS UI may be driven by a state file rather than live daemon discovery

Example:

- `/run/muos/global/visual/bluetooth`

Recommended response:

- inspect nearby files in `/run/muos/global/...`
- look for strings in `mux*` binaries or `libmux.so`

## Pattern 4: Bluetooth stack partially exists

Meaning:

- controller hardware may exist
- rfkill may be clear
- BlueZ tools may exist
- controller still needs attach/init

Recommended response:

- inspect rfkill
- locate `bluetoothd`
- locate firmware
- identify attach/init tool
- test controller attach manually

## Pattern 5: One success followed by repeated attach failure

Meaning:

- controller state may be stuck
- cleanup is incomplete

Recommended response:

- kill helper/daemon processes
- retry once
- if still failing, reboot and retest
- document reboot as temporary recovery path

## Pattern 6: App should appear in Applications but does not

Meaning:

- wrapper exists but not in the correct muOS app layout
- `muxapp` likely expects a specific structure

Recommended response:

- inspect existing app paths
- compare against working application entries
- create a proper launcher wrapper

## Pattern 7: Grep/find commands hang on device

Meaning:

- search scope is too broad

Recommended response:

- search specific directories first
- avoid `find / ...` unless necessary
- prefer labeled, one-by-one commands
