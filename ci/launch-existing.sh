#!/usr/bin/env bash
set -euo pipefail
mkdir -p startup
adb shell getprop > startup/device.txt
unzip -l apk/vintage-solo.apk > startup/apk-files.txt
adb install -r apk/vintage-solo.apk | tee startup/install.txt
adb logcat -c
adb shell am start -W -n forge.vintage.solo/forge.app.Launcher | tee startup/launch.txt
for i in $(seq 1 30); do
  sleep 5
  adb logcat -d > startup/logcat.txt
  if ! adb shell pidof forge.vintage.solo > startup/pid.txt; then
    cat startup/logcat.txt
    exit 1
  fi
done
adb shell dumpsys activity activities > startup/activities.txt
adb exec-out screencap -p > startup/screen.png
cat startup/logcat.txt
