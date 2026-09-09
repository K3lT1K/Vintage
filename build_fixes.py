"""Source-only corrections from actual build logs. Run after applying the saved patch."""
from pathlib import Path
unused = {
    "forge-gui-mobile/src/forge/screens/home/HomeScreen.java": [
        "com.badlogic.gdx.Gdx", "forge.game.GameType", "forge.gui.FThreads",
        "forge.screens.achievements.AchievementsScreen", "forge.screens.online.OnlineMenu.OnlineScreen",
        "forge.screens.planarconquest.ConquestMenu", "forge.screens.quest.QuestMenu",
        "forge.screens.settings.SettingsScreen"],
    "forge-gui-mobile/src/forge/Forge.java": ["forge.screens.home.NewGameMenu"],
}
for name, imports in unused.items():
    p = Path(name)
    text = p.read_text()
    for entry in imports:
        old = "import " + entry + ";\n"
        assert text.count(old) == 1, (name, entry)
        text = text.replace(old, "")
    p.write_text(text)

# Startup fix: keep Main initialization synchronous; Launcher installs assets first.
p = Path("forge-gui-android/src/forge/app/Main.java")
text = p.read_text()
old = "        final HWInfo vintageHardware = new HWInfo(device, os, getChipset);\n        // Unpack before Forge tries loading its skin; keep startup I/O off the Android UI thread.\n        new Thread(() -> {\n            try {\n                String resourceVersion;\n                try (InputStream version = getAssets().open(\"vintage-res.version\")) {\n                    resourceVersion = new java.io.BufferedReader(new java.io.InputStreamReader(version, StandardCharsets.UTF_8)).readLine();\n                }\n                forge.util.VintageResources.install(getAssets().open(\"vintage-res.zip\"),\n                        new java.io.File(getFilesDir(), \"VintageSolo\"), resourceVersion);\n                runOnUiThread(() -> initForge(Gadapter, vintageHardware, true, isTabletDevice(getContext())));\n            } catch (Exception error) {\n                runOnUiThread(() -> new android.app.AlertDialog.Builder(this)\n                        .setTitle(\"Vintage Solo: resources\")\n                        .setMessage(\"Cannot install bundled resources: \" + error.getMessage())\n                        .setPositiveButton(\"Close\", (dialog, which) -> finish()).show());\n            }\n        }, \"Vintage resource install\").start();\n"
assert text.count(old) == 1, "Expected original asynchronous Main bootstrap"
text = text.replace(old, "        initForge(Gadapter, new HWInfo(device, os, getChipset), permissiongranted, isTabletDevice(getContext()));\n")
p.write_text(text)

# The bundled skin does not render Russian menu labels in the Android screenshot.
# Use the supported English labels for this limited distribution.
translations = {
    "ВАША КОЛОДА": "YOUR DECK",
    "КОЛОДА СОПЕРНИКА": "BOT DECK",
    "Автопередача без действий": "Auto-pass with no actions",
    "Текстовые карты": "Text cards",
    "Начать партию": "Start game",
    "Управление": "Controls",
    "Долгое нажатие — увеличить карту. Нажмите на зону, чтобы посмотреть её.": "Long-press to zoom a card. Tap a zone to inspect it.",
    "Выбирайте атакующих и блокирующих на поле. Кнопки подсказки передают приоритет.": "Select attackers and blockers on the battlefield. Use the prompt buttons to pass priority.",
    "Меню уступки позволяет вернуть ручной контроль. После партии доступен журнал и его копирование.": "Use the yield menu for manual control. The game log can be viewed and copied after a match.",
    "Специализированный бот пока проходит проверку; превосходство над Forge не подтверждено.": "The specialist bot is experimental; improved strength has not been verified.",
    "Отсутствует файл колоды: ": "Missing deck file: ",
    "Колода должна содержать ровно 60 карт: ": "Deck must contain exactly 60 cards: ",
    "Недопустимая колода Vintage: ": "Invalid Vintage deck: ",
    "Проверьте ограничения формата": "Check format restrictions",
    "Подготовка стола": "Preparing game",
    "Не удалось начать партию": "Could not start game",
    "Ошибка колоды": "Deck error",
    "Давление и инициатива": "Pressure and initiative",
    "Артефакты и ограничения": "Artifacts and disruption",
    "Контроль и большие существа": "Control and large creatures"
}
for name in ("forge-gui-mobile/src/forge/screens/vintage/VintageSoloScreen.java",
             "forge-core/src/main/java/forge/deck/VintageSolo.java"):
    p = Path(name)
    text = p.read_text()
    for old, new in translations.items():
        text = text.replace(old, new)
    assert not any(0x0400 <= ord(char) <= 0x04ff for char in text), (name, "Untranslated Cyrillic")
    p.write_text(text)

# Visible pacing is installed only for actual matches opened by VintageSoloScreen.
p = Path("forge-gui-mobile/src/forge/screens/vintage/VintageSoloScreen.java")
text = p.read_text()
old = "                        HostedMatch match = GuiBase.getInterface().hostMatch();"
new = old + "\n                        match.setStartGameHook(() -> match.getGame().subscribeToEvents(\n" + \
      "                                new forge.gamemodes.match.VintageGamePacing(match.getGame())));"
assert text.count(old) == 1, "Expected Vintage Solo match launch"
p.write_text(text.replace(old, new))
