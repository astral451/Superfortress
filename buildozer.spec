[app]
title = Superfortress
package.name = superfortress
package.domain = org.astral451

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 0.1.0
requirements = python3,kivy

orientation = portrait
fullscreen = 0

# Supernote A5X runs an Android-based firmware. minapi 21 keeps this
# broadly compatible; adjust android.api upward if a future firmware
# needs a newer target SDK.
android.minapi = 21
android.api = 33
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
