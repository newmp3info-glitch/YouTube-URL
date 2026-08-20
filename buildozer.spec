[app]
title = Video Downloader
package.name = videodownloader
package.domain = org.downloader
source.include_exts = py,png,jpg,kv,atlas
source.dir = .
version = 1.0

requirements = python3, kivy, requests, certifi

# পাইথন ৩.১৪ এরর এড়াতে নির্দিষ্টভাবে ৩.১১ ভার্সন সেট করা হলো
android.python_version = 3.11

orientation = portrait
fullscreen = 0

android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

android.archs = arm64-v8a
android.accept_sdk_license = True

log_level = 2
