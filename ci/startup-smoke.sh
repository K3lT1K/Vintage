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
