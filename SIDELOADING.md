# Building and sideloading onto the Supernote A5X

Supernote A5X runs an Android-based firmware, so "sideloading" here means
building a normal Android APK and installing it manually (outside any app
store). This doc covers both steps.

## 1. Build the APK

This has to happen on a Linux machine (or WSL on Windows) — `buildozer`
downloads and drives the Android SDK/NDK and doesn't run on macOS/Windows
natively.

```bash
pip install --user buildozer cython
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip \
    autoconf libtool pkg-config zlib1g-dev libncurses5-dev \
    libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

cd Superfortress
buildozer android debug
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

## 3. Allow installing from unknown sources

Android blocks installing APKs from outside the Play Store by default.
On the Supernote:

1. Settings → About → tap the firmware/version number ~7 times to unlock
   Developer Options (standard Android trick — Supernote inherits this).
2. Find whichever file manager app you'll use to open the APK (Supernote's
   built-in Files app, or another) and enable "Install unknown apps" /
   "Allow from this source" for it.

Exact menu wording varies by firmware version — if these labels don't
match what you see, search Supernote's support site or community wiki for
your specific firmware build; the underlying Android mechanism is the
same, just the settings screen may be reorganized.

## 4. Install and launch

Open the Files app on the Supernote, navigate to the APK you copied over,
and tap it. Confirm the install prompt. Superfortress should then appear
in the app drawer like any other sideloaded app.

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
