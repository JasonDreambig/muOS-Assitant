# muOS Release Checklist

## Pre-Release

- confirm exact target device(s)
- confirm target muOS version(s)
- confirm the app launches from a clean boot
- confirm install path and runtime paths are correct
- confirm logs are written somewhere useful
- document any reboot-required recovery behavior

## Packaging

- include all required scripts
- include icons/art if needed
- include README/install instructions
- verify file permissions
- verify launcher entry points
- verify package name/version

## UX

- confirm the app name is clear
- confirm menu labels are understandable
- confirm failure messages are readable
- confirm status output is useful

## Technical Verification

- test install
- test first launch
- test second launch
- test stop/restart
- test trusted device or saved state behavior
- test any UI state files used by muOS

## Distribution

- prepare GitHub release notes
- upload source and package files
- include install instructions
- include compatibility notes

## Memory Update

- update project memory report
- update next steps
- update session log
