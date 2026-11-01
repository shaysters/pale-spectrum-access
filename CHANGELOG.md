# Changelog

## 1.0.0 - 2026-10-31

First public release.

### Added
- Speech through Prism: NVDA, JAWS and other screen readers, or Windows' voice.
- Reads dialogue, narration, choices (with whose choice it is), chapter titles and every menu.
- Keyboard navigation for the main menu, story picker, game menu, save and load, preferences, yes/no prompts, extras, credits, gallery and progress map.
- Spoken descriptions for all 103 gallery pictures and the names of all 26 endings.
- A line that is only "..." is read as "ellipsis", so you know someone said nothing.
- F1 opens the accessibility settings list, in the story and in menus. It has "Read voice acted lines" and shows which speech output is in use.
- q opens the in-scene buttons during the story: Rewind, Skip and Game menu.
- When a prompt or menu closes, the mod says what you were on before it: the current line in the story, or the selected item in a menu.
- When the main menu has been read, the mod tells you if a newer version is out. Run the installer to update.
- A standalone installer, PaleSpectrumAccessInstaller.exe, that finds your Steam copy of the game and installs, updates and uninstalls the mod.

### Changed
- Voice acted lines are not read by default; v turns this on or off.
- The mod no longer replaces any of the game's screens. It reads the game's own screens, including the credits and the gallery, while the game runs.

### Fixed
- The quit prompt from Alt+F4 during the story could not be used, because the keys went to the dialogue underneath.
- Pressing h a second time crashed the game. h now hides the text window, and h, Enter or Space shows it again.
- After Alt+Tab or Alt+F4, a stuck Alt key could stop every key from working. The mod now clears modifier keys that aren't actually held.
