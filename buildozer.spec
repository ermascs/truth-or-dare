
[app]

title = جرئت یا حقیقت
package.name = joratohaq
package.domain = org.example

source.dir = .
source.include_exts = py,kv,png,jpg,atlas,ttf

version = 1.0

requirements = python3,kivy,arabic-reshaper,python-bidi

orientation = portrait
fullscreen = 0

android.api = 35
android.minapi = 23
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True

[buildozer]

log_level = 2
warn_on_root = 1
