# HANDOFF — 2026-09-10

## Current verified build

- Repository: https://github.com/K3lT1K/Vintage
- Build commit: `bf59a65e167e4a04fc496a59f34c0431e04c79c0`.
- Successful build AND Android startup: https://github.com/K3lT1K/Vintage/actions/runs/34469122372
- Signed APK: https://github.com/K3lT1K/Vintage/actions/runs/34469122372/artifacts/10149070267
- Complete restored Forge sources: https://github.com/K3lT1K/Vintage/actions/runs/34469122372/artifacts/10148783056
- Android screenshots/logcat: https://github.com/K3lT1K/Vintage/actions/runs/34469122372/artifacts/10149302081
- Pinned upstream Forge: `ce5b0dbf17733847929e990c77274893223e1fa6`.
- APK package `forge.vintage.solo`, launcher `forge.app.Launcher`, main activity `forge.app.Main`.
- Debug signed using upstream uber-apk-signer key; signature, launcher, DEX, native libraries, ZIP CRC and complete offline resource hash/file inventory passed.

## Implemented

Four selectable 60-card decks for either player, including mirrors: Initiative, Workshop, Oath, Doomsday. Doomsday is SingPanMan's 2026-08-23 Vintage Challenge list, main deck only:
https://www.mtggoldfish.com/deck/download/7923523

VintageCardRules is invoked from AiController.canPlaySa. Forge retains timing, restrictions, targets, costs and actual payment. Gaea's Blessing targets self and recycles useful cards; Probe cantrips against empty hands but avoids empty library/draw locks; Trap targets legal hostile spells, can exile multiple spells, and refuses empty or low-value uses. Normal Forge remains fallback. Generic unsupported-card warnings for these three are filtered only for specialist players; card scripts and ordinary Forge AI warnings remain unchanged.

Doomsday has its own mulligan/mana priorities, legal search selections and ordering callback in PlayerControllerAi. Conservative pass-turn pile: Recall, Lotus, Oracle, Force, Ponder. Public locks, life after halving, blue land and known missing roles are checked. No concealed opposing hand or library order is read by these policies. Post-pile fetch activations and cycling are held. Only this pile is implemented; Demonic Consultation is deliberately not cast by the bot. Doomsday/Consultation warnings remain. This is not a verified strong Doomsday pilot.

Landscape card table: lands left; creatures centrally; noncreature artifacts/enchantments right; attached auras/equipment stay with host. Fan hand below; compact life/zone HUD; optional phase stops under gear; Game/Players/Log under gear, separate stack fan. Pacing retained: 1000 ms after bot land/spell, 500 ms per bot step/phase, off UI thread.

Floating mana blocks implicit no-action/phase-skip passes on an empty stack, with existing manual mana-loss confirmation enabled. Normal rules for clearing mana between steps/phases remain. The original phone report was not reproduced as an engine subtraction bug.

Russian text covers all 84 distinct deck cards plus reverse face and support tokens/effects; original English names retained. Custom translations, not claimed official. Bundled Roboto supports Cyrillic. Downloaded printed images can be English; translated rule text remains available in the client.

Картинки колод gathers exact PaperCard printings from ALL FOUR lists, removes duplicates, includes back faces and needed token images. Explicit-list GuiDownloadFilteredCardImages path does not enumerate all printings, synchronize sets or download bulk metadata. Existing files skipped; compact background progress/cancel dialog. Cache persists for offline use. Text-card mode remains usable without images.

## Actually checked

- 20 local assertions; syntax parsing of 31 Java files.
- Four decks: 60 cards each; scripts present, counts/B&R checked against pinned Forge data. This is not a separate current WotC legality audit.
- Russian coverage and Oracle mana-symbol preservation.
- Full compilation and Checkstyle.
- 11 real Forge tests: 5 mana/Russian tests; 5 card-policy/effect tests; 1 image-plan/cache test. Final run: 0 failures, 0 errors, 0 skips; no headless status-widget exception.
- Image test constructs a small exact-printing queue (<=100 files in its two-token fixture), verifies no bulk/ZIP URL and skips an existing file; it does NOT download remote images.
- Android 16 API36 x86_64 emulator: clean install, offline first launch, 180-second survival, HOME/resume, game entry and gear menu; no detected FATAL/ANR.
- Visually reviewed first-launch, match-4 and match-settings screenshots: download button, actual seven-card fan, opponent land left, noncreature artifact right, open gear menu. Bot actions progressed between captures.

## Not checked / limitations

- Physical OnePlus 13 / OxygenOS 16 on this build.
- Actual image transfer from Scryfall/CardForge on the phone; optional illustrations require internet once.
- Completed automated full games: **0**. All 16 ordered deck pairings / first-player swaps remain to be run.
- Specialist vs baseline win-rate comparison: **not run**. No claim of higher human win rate.
- All combat/stack interactions, all Doomsday piles, tutor/protection variations and long-game stability.
- Precise pacing on physical phone; recovery of a game after process death (not implemented).

## Reproduction and continuation

See BUILD.md for exact commands. Restore in order:
1. Checkout pinned upstream Forge.
2. Apply `vintage-solo.patch`.
3. Copy `fixes/` overlay.
4. Run `build_fixes.py`, which applies `presentation.patch` LAST.
5. Run bootstrap.sh, build.sh and check_apk.py.

Do not apply patches again to the complete source artifact. Tools pinned by bootstrap: Maven 3.8.1, Android CLI 11076708, platform35/build-tools35.0.0, Forge Android Maven plugin4.6.2, JDK17. Main test command:
`mvn -B -pl forge-gui-desktop -am '-Dtest=Vintage*RegressionTest' -DfailIfNoTests=false -Dsurefire.failIfNoSpecifiedTests=false test`

Current startup smoke taps the relocated confirmation at x92%, y88%, then gear at x98%, y3%. Earlier runs survived but remained on a modal due wrong coordinates; only the final screenshot review above establishes game entry.

Earlier CI issues fixed: overloaded Card::getName method reference, unused test import, Iterable target access, actual stack-zone setup in Trap test, and UI progress callback in a deliberately headless image-plan test. No test gates were disabled.

Next useful work: user phone verification and image download; finish full games with all four decks and both first-player assignments, measure bot comparisons, extend Doomsday lines based on reproducible failures. Batch changes; don't push each small edit. Root HANDOFF is newer than the historical source-artifact snapshot written before CI completed.
