[app]
title = Video Downloader
package.name = videodownloader
package.domain = org.downloader
source.include_exts = py,png,jpg,kv,atlas
source.dir = .
version = 1.0

# পাইথন ৩.১৪ এরর চিরতরে বন্ধ করতে এখানে সরাসরি python3.11 নির্দিষ্ট করে দেওয়া হলো
requirements = python3.11, kivy, requests, certifi

# পাইথন ভার্সন নিশ্চিত করার জন্য
android.python_version = 3.11

orientation = portrait
fullscreen = 0

android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

android.archs = arm64-v8a
android.accept_sdk_license = True

log_level = 2
