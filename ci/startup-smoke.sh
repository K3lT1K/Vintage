#!/usr/bin/env bash
set -euo pipefail
mkdir -p startup
capture() {
  adb logcat -d > startup/logcat.txt || true
  adb shell dumpsys activity activities > startup/activities.txt || true
  adb exec-out screencap -p > startup/screen.png || true
}
trap capture EXIT
adb shell getprop > startup/device.txt
adb install -r apk/vintage-solo.apk | tee startup/install.txt
adb shell svc wifi disable
adb shell svc data disable
adb logcat -c
adb shell am start -W -n forge.vintage.solo/forge.app.Launcher | tee startup/launch.txt
for i in $(seq 1 36); do
  sleep 5
  if ! adb shell pidof forge.vintage.solo > startup/pid.txt; then
    capture
    cat startup/logcat.txt
    exit 1
  fi
done
capture
grep -E '(topResumedActivity=|mResumedActivity:|ResumedActivity:).*forge.vintage.solo/forge.app.Main' startup/activities.txt
adb exec-out screencap -p > startup/first-launch.png
adb shell input keyevent KEYCODE_HOME
sleep 10
adb shell am start -W -n forge.vintage.solo/forge.app.Launcher
sleep 15
adb shell pidof forge.vintage.solo
capture
grep -E '(topResumedActivity=|mResumedActivity:|ResumedActivity:).*forge.vintage.solo/forge.app.Main' startup/activities.txt
if grep -E 'FATAL EXCEPTION|Fatal signal|ANR in forge.vintage.solo' startup/logcat.txt; then exit 1; fi
echo 'Offline startup process survival and resumed Main after background: PASS'
echo 'Rendered menu, physical OnePlus, full game and bot behavior require separate verification.'

# Capture actual match controls after dismissing opening prompts. These are
# visual evidence only: surviving taps does not establish a completed game.
read -r SCREEN_W SCREEN_H < <(python3 -c 'import struct; print(*struct.unpack(">II", open("startup/first-launch.png","rb").read()[16:24]))')
adb shell input tap "$((SCREEN_W / 2))" "$((SCREEN_H * 86 / 100))"
sleep 25
adb exec-out screencap -p > startup/match-opening.png
adb shell input tap "$((SCREEN_W * 8 / 100))" "$((SCREEN_H * 88 / 100))"
sleep 4
for n in 1 2 3 4; do
  adb shell input tap "$((SCREEN_W * 92 / 100))" "$((SCREEN_H * 94 / 100))"
  sleep 4
  adb exec-out screencap -p > "startup/match-$n.png"
done
adb shell input tap "$((SCREEN_W * 98 / 100))" "$((SCREEN_H * 3 / 100))"
sleep 3
adb exec-out screencap -p > startup/match-settings.png
adb shell pidof forge.vintage.solo
capture
if grep -E 'FATAL EXCEPTION|Fatal signal|ANR in forge.vintage.solo' startup/logcat.txt; then exit 1; fi
