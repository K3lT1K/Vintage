# Сборка и проверка Vintage Solo

## Скачать и установить

1. Войдите в GitHub и скачайте [APK в ZIP](https://github.com/K3lT1K/Vintage/actions/runs/34304628301/artifacts/10086347649).
2. Распакуйте архив и откройте `vintage-solo.apk`; подтвердите установку/обновление. В архиве также находятся SHA256SUMS и verification.txt.
3. Включите авиарежим и запустите Vintage Solo. На первом запуске дождитесь экрана Preparing offline resources; на эмуляторе распаковка занимала около 30 секунд, на телефоне время может отличаться.
4. Выберите YOUR DECK и BOT DECK, нажмите Start game. Controls открывает справку. Проверьте несколько ходов, сворачивание и возвращение, затем попробуйте закончить партию.

Подписано отладочным ключом upstream uber-apk-signer. Package forge.vintage.solo; min SDK 26; target SDK 35. На эмуляторе Android 16 API36 запуск и возврат после сворачивания проверены. Физический OnePlus 13 / OxygenOS 16 ожидает повторной проверки пользователем. Меню этой сборки на английском.

Если Android не принимает обновление, сообщите точный текст ошибки. Если снова происходит вылет, пришлите короткое видео и укажите: до экрана распаковки, после него или после Start game. Полная партия и бот пока не проверены. Восстановление партии после уничтожения процесса не реализовано.

## Повторить GitHub Actions

Откройте [workflow](https://github.com/K3lT1K/Vintage/actions/workflows/vintage-android.yml) → Run workflow → main → Run workflow. После зелёного результата откройте запуск → Artifacts → vintage-solo-apk. `vintage-solo-diagnostics` содержит логи; `vintage-solo-source` — полные восстановленные исходники.

Workflow также запускается при push в main/codex/vintage-apk. Для правок только документации используйте `[skip ci]`, чтобы не пересобирать игру.

## Воспроизвести локально на Linux

Нужны Git, JDK17, Python3.11+, curl, tar, unzip и Xvfb при отсутствии дисплея. Скрипт bootstrap не использует apt/sudo.

```bash
git clone https://github.com/K3lT1K/Vintage.git project
git clone https://github.com/Card-Forge/forge.git forge
cd forge
git checkout ce5b0dbf17733847929e990c77274893223e1fa6
git apply --check ../project/vintage-solo.patch
git apply ../project/vintage-solo.patch
cp -a ../project/fixes/. .
python3 ../project/build_fixes.py
# После ознакомления и согласия с условиями Android SDK:
ACCEPT_ANDROID_SDK_LICENSES=yes bash tools/vintage-solo/bootstrap.sh
source .vintage-tools/env.sh
xvfb-run -a bash tools/vintage-solo/build.sh
python3 tools/vintage-solo/check_apk.py
```

Результат: `dist/vintage-solo/vintage-solo.apk`. При использовании полного исходного архива уже применены patch и build_fixes; повторно их применять не нужно.

Зафиксированы Maven 3.8.1, Android CLI 11076708, Android platform35/build-tools35.0.0, Forge Android Maven plugin4.6.2. Upstream timestamps/транзитивные зависимости не гарантируют побитовой воспроизводимости.

## Что проверяет CI

- 18 локальных assertions, синтаксические проверки и состав 3×60 карт.
- Полный Maven install и Android verify, с Checkstyle и ошибками pipeline, которые не маскируются tee.
- apksigner verify; package/launcher; DEX и LibGDX native code.
- ZIP CRC; соответствие вложенного resource ZIP сгенерированному архиву; наличие всех ожидаемых ресурсов.

- Отдельный job startup устанавливает именно собранный APK на эмулятор API36 x86_64, отключает Wi-Fi/данные, наблюдает процесс 180 секунд, проверяет resumed Main, нажимает HOME и возвращает приложение. Сохраняет logcat, dumpsys и скриншоты.

Оба jobs успешны в [run 34304628301](https://github.com/K3lT1K/Vintage/actions/runs/34304628301); подписи меню визуально проверены по скриншоту. Тест не нажимает Start game и не проводит партии. Исходный немодифицированный APK отдельно не собран.
