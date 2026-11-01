# Pale Spectrum Access

Pale Spectrum Access is a mod that makes Pale Spectrum - Part Two of the Book of Gray Magic, the visual novel by Ithaqua Labs, playable with a screen reader. It reads dialogue, narration, choices and every menu, makes everything usable from the keyboard, and describes every picture in the gallery.

It works with NVDA, JAWS and other Windows screen readers, and falls back to Windows' built-in voices if no screen reader is running. You play with the keyboard.

- Join the Discord to chat, get help or report problems: <https://discord.gg/KNDXhztGGK>
- Support shaysters on Ko-fi: <https://ko-fi.com/shaysters>

Version 1.0.0. See [CHANGELOG.md](CHANGELOG.md) for what has changed.

## Requirements

- Pale Spectrum - Part Two of the Book of Gray Magic for Windows, from Steam or itch.io:
  - Steam: <https://store.steampowered.com/app/554180/>
  - itch.io: <https://ithaqualabs.itch.io/pale-spectrum-game>
- A screen reader such as NVDA or JAWS (optional; without one, the mod uses Windows' built-in speech).

The mod has been tested with the Steam version (game version 1.1). The itch.io and DRM-free versions should work too, but they haven't been tested yet.

## Installing

1. Close the game if it's running.
2. Download **PaleSpectrumAccessInstaller.exe** from the [latest release](https://github.com/shaysters/pale-spectrum-access/releases/latest). It needs 64-bit Windows 10 or later.
3. Run it. Windows SmartScreen may warn that the app is unrecognized, because the installer is not code-signed. Choose **More info**, then **Run anyway**.
4. The installer finds your Steam copy of the game by itself. For an itch.io or DRM-free copy, or if it can't find the game, use the Browse button next to the game folder and choose the folder that contains `Pale Spectrum.exe`.
5. Choose **Install**.
6. Start your screen reader, then start the game. The mod starts speaking at the main menu.

### Updating and uninstalling

Keep the installer. Run it again to update to the newest version, repair the mod, or uninstall it. Close the game first. The installer says on its first page when an update is available, and the mod tells you too, once the main menu has been read.

### Installing by hand

1. Download **PaleSpectrumAccess.zip** from the [latest release](https://github.com/shaysters/pale-spectrum-access/releases/latest).
2. Open the game folder, the one that contains `Pale Spectrum.exe`. On a default Steam install that's:

   ```
   C:\Program Files (x86)\Steam\steamapps\common\Pale Spectrum - Part Two of the Book of Gray Magic
   ```

   For itch.io or DRM-free copies, use the folder you installed the game to.
3. Extract the zip into that folder. `prism.dll` and the `prism_licenses` folder go next to `Pale Spectrum.exe`, and the three `.rpy` files go into the `game` subfolder.
4. Start your screen reader, then start the game.

No game files are replaced, and your saves are not affected.

To uninstall a manual install, delete `prism.dll` and the `prism_licenses` folder from the game folder, and every file starting with `zz_ps_a11y_` from the `game` subfolder (the `.rpy` files and the `.rpyc` files the game makes from them).

## Keys

| Key | Where | What it does |
|---|---|---|
| Enter or Space | Story | Continue to the next line. |
| r | Story | Repeat the last line. |
| Up and Down | Story | Read back through earlier lines. |
| Page Up and Page Down | Story | Roll back or forward. |
| Hold Ctrl | Story | Skip through lines you've already read. |
| Tab | Story | Turn skipping on or off. |
| q | Story | Open the in-scene buttons: Rewind, Skip and Game menu. |
| v | Story | Turn reading of voice acted lines on or off. |
| h | Story | Hide the text window. h, Enter or Space shows it again. |
| Escape | Story | Open the game menu: save, load, settings, quit. |
| Up and Down | Menus and choices | Move between options. |
| Left and Right | Menus | Change a setting, or turn the page in save slots, the gallery and the credits. |
| Enter or Space | Menus and choices | Select. |
| Home and End | Menus and choices | Jump to the first or last option. |
| Delete | Save and load | Delete the selected save. |
| r | Menus | Repeat the selected option. |
| Escape | Menus | Go back. |
| F1 | Everywhere | Open the accessibility settings. |
| f | Story | Switch between fullscreen and windowed. |
| s | Story | Take a screenshot. |

Notes:

- When a choice appears you hear whose decision it is, for example "Belinda's choice", then the options.
- When a prompt or menu closes, the mod says what you were on before it opened.
- A line that is only "..." is read as "ellipsis", so you know someone said nothing.

## Settings

Press F1 in the story or in any menu. Up and Down choose a setting, Left, Right or Enter change it, and Escape closes the list. Settings are saved automatically.

- **Read voice acted lines** (off by default): when off, lines that have voice acting aren't read, so the screen reader doesn't talk over the actors. Narration is always read, and r repeats any line.
- **Speech output**: says whether Prism found NVDA, JAWS or another screen reader, or is using Windows' voice.

## Extras

- **Credits:** every credit line can be read with Up and Down.
- **Gallery:** each unlocked picture has a spoken description. Enter views a set, Enter or Right goes to the next picture, Left to the previous one, and Escape goes back.
- **Progress map:** lists the endings you have found, by name.

## Troubleshooting

The mod keeps a log next to `Pale Spectrum.exe`:

```
a11y_log.txt
```

It says which speech output Prism found and records any errors. If something goes wrong, include the log when you report it.

- **No speech at all:** make sure `prism.dll` is next to `Pale Spectrum.exe` and the `zz_ps_a11y_` files are in the `game` subfolder, then start the game again.
- **Keys stop working after Alt+Tab:** the mod clears a stuck Alt key by itself within a moment. If keys still don't respond, press and release Alt once.

To report a problem or suggest something, open an issue on the [GitHub page](https://github.com/shaysters/pale-spectrum-access/issues).

## Credits

This mod was developed by [Shaysters](https://github.com/shaysters), with code and picture descriptions written by Claude (Anthropic).

The installer is built with [Loadstone](https://github.com/bradjrenshaw/loadstone) by [Bradley Renshaw](https://github.com/bradjrenshaw).

Speech is provided by [Prism](https://github.com/ethindp/prism) by Ethin Probst, under the MPL-2.0 license. Its license and the licenses of the libraries it uses are in the `prism_licenses` folder.

Pale Spectrum is made by Ithaqua Labs. This mod isn't affiliated with or endorsed by Ithaqua Labs.

## For developers

Release instructions are in [DEVELOPING.md](DEVELOPING.md).
