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
