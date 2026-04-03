# SSH Diagnostics Cookbook

A reference of tested SSH command sequences for diagnosing muOS app behavior on-device.

**General rule:** Use small, targeted commands. Never start with `find /` or broad searches.

---

## Bluetooth

```bash
# Stack overview
rfkill list
which bluetoothctl
find /bin /sbin /usr/bin /usr/sbin /opt -name bluetoothd 2>/dev/null
ps aux | grep -E 'bluetooth|rtk_hciattach' | grep -v grep
dmesg | grep -i -E 'bluetooth|hci|rfkill|rtl' | tail -n 80

# Attach/init sequence (Realtek chipset, common on RG35XX)
find /opt /usr/lib -name 'rtk_hciattach' 2>/dev/null
find /lib/firmware /opt -name '*.hcd' 2>/dev/null | head -10

# Check controller after attach
hciconfig -a
hcitool dev
```

---

## WiFi / Networking

```bash
# Interface state
ip link show
ifconfig 2>/dev/null || ip addr show

# Connectivity manager (muOS uses connman or wpa_supplicant)
ps aux | grep -E 'connman|wpa_supplicant|dhclient|udhcpc' | grep -v grep
which connmanctl 2>/dev/null
connmanctl state 2>/dev/null
connmanctl services 2>/dev/null | head -20

# wpa_supplicant config if used directly
cat /etc/wpa_supplicant.conf 2>/dev/null || echo missing
find /etc /opt -name 'wpa_supplicant.conf' 2>/dev/null

# DNS
cat /etc/resolv.conf
ping -c 1 8.8.8.8 2>&1 | head -5
```

---

## muOS Visual State

```bash
# UI state files (control icons and status glyphs in muOS)
ls -l /run/muos/global/visual/
cat /run/muos/global/visual/bluetooth 2>/dev/null || echo missing
cat /run/muos/global/visual/network 2>/dev/null || echo missing

# All global state files
find /run/muos/global -type f | sort
```

---

## muOS UI Modules

```bash
# Find mux* binaries
find /opt/muos -type f | grep -i 'mux' | sed -n '1,200p'

# Inspect a specific module
file /opt/muos/extra/muxconnect
strings /opt/muos/extra/muxconnect | grep -i -E 'blue|bt|connect|network|visual'
strings /opt/muos/extra/lib/libmux.so | grep -i -E 'blue|bt|connect|network|visual'

# Find which mux* module handles Applications
find /opt/muos -name 'muxapp*' 2>/dev/null
```

---

## App Launch Path Debugging

```bash
# Check if app appears in Applications
ls /mnt/mmc/MUOS/application/
ls /mnt/mmc/MUOS/application/$APP_NAME/

# Verify launcher script exists and is executable
ls -la /mnt/mmc/MUOS/application/$APP_NAME/launch.sh
cat /mnt/mmc/MUOS/application/$APP_NAME/launch.sh

# Check script runs directly (test outside muOS UI)
sh /mnt/mmc/MUOS/application/$APP_NAME/launch.sh

# Environment when muOS launches apps (differs from SSH shell)
# muOS apps inherit a limited environment — check PATH explicitly
env | sort
echo $PATH
echo $HOME

# Compare: what does the launcher see vs your SSH session?
# Add this to your launch.sh for debugging:
# env > /tmp/app_env_debug.txt 2>&1
```

---

## Log Inspection

```bash
# Primary logs
cat /tmp/muos.log 2>/dev/null | tail -40
cat /tmp/app.log 2>/dev/null | tail -40
cat /var/log/syslog 2>/dev/null | tail -40

# dmesg for kernel/hardware events
dmesg | tail -60
dmesg | grep -i -E 'error|fail|warn' | tail -30

# App-specific log (if your app writes one)
cat /tmp/$YOUR_APP.log 2>/dev/null | tail -40

# Live log watching (useful during testing)
# tail -f /tmp/muos.log
```

---

## File Permissions and Ownership

```bash
# Check script is executable
ls -la /usr/bin/$YOUR_BINARY
ls -la /opt/$YOUR_APP/bin/

# Fix permissions if needed
chmod +x /path/to/script
chmod 755 /path/to/binary

# Check config file ownership
ls -la /root/.your-app.conf 2>/dev/null

# muOS runs apps as root — ownership rarely an issue, but confirm:
id
whoami
```

---

## Processes

```bash
# Full process list (limit output)
ps aux | sed -n '1,120p'

# Find a specific app or daemon
ps aux | grep -E "$YOUR_APP_NAME" | grep -v grep

# Kill a stuck process
kill $(ps aux | grep "$DAEMON_NAME" | grep -v grep | awk '{print $1}')
```

---

## Storage and Package Paths

```bash
# Mount points
mount | sed -n '1,120p'

# Key muOS storage layout
ls /mnt/mmc/MUOS/
ls /run/muos/storage/

# Runtime symlinks (confirm they resolve)
ls -la /run/muos/storage/
readlink /run/muos/storage/retroarch

# App installation paths
ls /mnt/mmc/MUOS/application/
find /mnt/mmc/MUOS/application -maxdepth 2 -type f | sed -n '1,60p'

# Archive manager packages
find /mnt/mmc/ARCHIVE -maxdepth 2 2>/dev/null | head -30

# Ports
find /mnt/union/ports -maxdepth 2 -type f | sed -n '1,160p'
```

---

## Binary and Dependency Checks

```bash
# Confirm a binary exists and is the right type
which $BINARY_NAME
file $(which $BINARY_NAME)

# Check shared library dependencies (if not a static binary)
ldd $(which $BINARY_NAME) 2>/dev/null | head -20

# Find a binary anywhere on device
find /bin /sbin /usr/bin /usr/sbin /opt -name "$BINARY_NAME" 2>/dev/null

# Confirm curl is available (needed for API calls)
which curl
curl --version | head -1
```

---

## Package Inspection

```bash
# Inspect an installed muOS archive package
find /mnt/mmc/ARCHIVE/$PACKAGE_NAME -type f 2>/dev/null
cat /mnt/mmc/ARCHIVE/$PACKAGE_NAME/README.md 2>/dev/null

# Inspect an installed app
find /mnt/mmc/MUOS/application/$APP_NAME -type f
cat /mnt/mmc/MUOS/application/$APP_NAME/launch.sh

# Check if a script is installed to /usr/bin
ls -la /usr/bin/$APP_NAME
