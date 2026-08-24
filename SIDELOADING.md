# Building and sideloading onto the Supernote A5X

Supernote A5X runs an Android-based firmware, so "sideloading" here means
building a normal Android APK and installing it manually (outside any app
store). This doc covers both steps.

## 1. Build the APK

This has to happen on a Linux machine (or WSL on Windows) — `buildozer`
downloads and drives the Android SDK/NDK and doesn't run on macOS/Windows
natively.

On recent Ubuntu/WSL (23.04+/24.04), `pip install` at the system level is
blocked by default ("externally-managed-environment"). Use a virtual
environment to keep the build tooling isolated:

```bash
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip python3-venv \
    autoconf libtool pkg-config zlib1g-dev libncurses5-dev \
    libncursesw5-dev cmake libffi-dev libssl-dev

python3 -m venv ~/buildozer-venv
source ~/buildozer-venv/bin/activate
pip install --upgrade pip
pip install buildozer cython

cd Superfortress
buildozer android debug
```

Any time you come back to build later, re-activate the venv first:
`source ~/buildozer-venv/bin/activate`.

### `libtinfo5` not found (WSL / Ubuntu 22.04+)

`libtinfo5` was dropped from Ubuntu's repos starting with 22.04, so it's
left out of the `apt install` line above. It's only needed for some of
the older 32-bit Android SDK command-line tools (e.g. `aapt`), so it
only bites during the `buildozer android debug` step itself, not before.
If the build complains about a missing `libtinfo.so.5`, fix it with
either of these before re-running `buildozer android debug`:

```bash
# Option A: symlink to libtinfo6 (usually enough)
sudo apt install -y libtinfo6
sudo ln -s /usr/lib/x86_64-linux-gnu/libtinfo.so.6 /usr/lib/x86_64-linux-gnu/libtinfo.so.5

# Option B: install the real libtinfo5 package directly
wget http://archive.ubuntu.com/ubuntu/pool/universe/n/ncurses/libtinfo5_6.2-0ubuntu2_amd64.deb
sudo dpkg -i libtinfo5_6.2-0ubuntu2_amd64.deb
```

The first run downloads the Android SDK/NDK (multiple GB) and will take a
while. Subsequent builds are much faster. Output APK lands in `bin/`, e.g.
`bin/superfortress-0.1.0-arm64-v8a-debug.apk`.

If you'd rather sanity-check the app before spending time on an Android
build, run it as a normal desktop Kivy app first:

```bash
pip install kivy
python main.py
```

That won't tell you anything about e-ink behavior, but it confirms the
simulation and UI logic work.

## 2. Get the APK onto the device

Plug the Supernote into your computer via USB-C. It should mount as a
storage device (MTP). Copy the APK into a folder you can find later, e.g.
`Document/` or a new `Sideload/` folder.

## 3. Install the APK via ADB

**Confirmed on a real A5X: tapping the APK in Supernote's built-in file
manager fails with "Unsupported file format."** The stock file manager
doesn't associate `.apk` with the package installer at all — this isn't
a bad transfer or a broken build, it just doesn't know what to do with
the file. Installing over ADB sidesteps the file manager entirely and is
the reliable path.

1. Download Android Platform Tools (adb) for your OS:
   https://developer.android.com/tools/releases/platform-tools — extract
   it somewhere handy, e.g. `C:\platform-tools` on Windows.
2. On the Supernote: Settings → About → tap the firmware/version number
   ~7 times to unlock Developer Options (standard Android trick —
   Supernote inherits this), then open Developer Options and enable
   **USB debugging**.
3. Plug the Supernote into your computer via USB-C. It should prompt on
   the Supernote screen to allow the connection (an RSA key fingerprint
   prompt) — tap **Allow**.
4. From a terminal in the `platform-tools` folder, confirm the device is
   visible and authorized:
   ```
   adb devices
   ```
   It should list a device ID, not `unauthorized` (if it says
   `unauthorized`, check the Supernote screen for the allow prompt).
5. Install directly — no need to copy the APK onto the device at all:
   ```
   adb install path/to/superfortress-0.1.0-arm64-v8a-debug.apk
   ```

Superfortress should now appear in the Supernote's app drawer.

Exact Developer Options menu wording can vary by firmware version — if
labels don't match what you see, the underlying Android mechanism is the
same, just the settings screen may be reorganized.

## What to expect on first launch

- A grid map fills most of the screen: light gray = grass, dark gray =
  trees, mid gray = stone, near-black = water.
- A white dot is the worker — it walks to the nearest tree, "harvests"
  it (tree turns to grass, wood count ticks up), then moves to the next
  one.
- Top bar shows wood/trees/tick counters and a Pause/Resume button.
- Redraws only happen when something actually changes (worker moves or
  harvests), and the frame rate is capped low — this is deliberate, to
  keep it friendly to the e-ink panel rather than fighting it with
  constant refreshes.

If the app installs and the map renders at all, that's the core goal
(proving sideloading works) validated — everything else is iteration.
