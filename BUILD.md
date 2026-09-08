# Сборка и проверка Vintage Solo

## Скачать и установить

1. Войдите в GitHub и откройте [пакет APK](https://github.com/K3lT1K/Vintage/actions/runs/34211369106/artifacts/10050272318).
2. Распакуйте ZIP: внутри `vintage-solo.apk`, `SHA256SUMS` и `verification.txt`.
3. Откройте APK на Android. При запросе разрешите установку этому файловому менеджеру/браузеру.

Подписано отладочным ключом upstream uber-apk-signer. Package `forge.vintage.solo`, min SDK 26 (Android 8). Android 11+ и 4 ГБ RAM рекомендуются исходным Forge; совместимость конкретного телефона пока не проверена.

## Короткая проверка на телефоне

1. Включите авиарежим **до первого запуска**, откройте Vintage Solo. При первом запуске распаковывается большой набор ресурсов.
2. Выберите свои Initiative и Oath для бота, начните партию. Проверьте текст карт, жизни, стек и зоны.
3. Сделайте несколько ходов, проверьте долгое нажатие и ручную передачу приоритета.
4. Сверните приложение на 20 секунд, вернитесь и доиграйте до результата.
5. Откройте журнал: должны быть записи `[Vintage AI]`. Наличие записей ещё не доказывает силу бота.

При проблеме пришлите модель телефона, Android, точное действие перед сбоем и скриншот/журнал. Особенно различайте: не устанавливается; не запускается; застревает загрузка; зависает конкретное игровое действие.

Восстановление после уничтожения процесса не реализовано. Его не следует путать со сворачиванием.

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

Эти проверки успешны в [run 34211369106](https://github.com/K3lT1K/Vintage/actions/runs/34211369106). Они не запускают приложение и не проводят партии. Исходный немодифицированный APK отдельно не собран.
