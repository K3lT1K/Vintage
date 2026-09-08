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
