[app]
title = Video Downloader
package.name = videodownloader
package.domain = org.downloader
source.include_exts = py,png,jpg,kv,atlas
source.dir = .
version = 1.0

# সঠিক রিকোয়ারমেন্টস (এখানে python3 এর সাথে কোনো ==3.10 দেওয়া যাবে না)
requirements = python3, kivy, requests, certifi, urllib3, idna, charset-normalizer

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
