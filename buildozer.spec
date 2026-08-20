[app]
title = Video Downloader
package.name = videodownloader
package.domain = org.downloader
source.include_exts = py,png,jpg,kv,atlas
source.dir = .
version = 1.0

requirements = python3, kivy, cython==0.29.36, requests, certifi

orientation = portrait
fullscreen = 0

android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

android.api = 31
android.min_api = 24
android.ndk = 25b
android.sdk_api_version = 31
android.archs = arm64-v8a
android.accept_sdk_license = True

log_level = 2
