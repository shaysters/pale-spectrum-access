# Pale Spectrum Access: developer notes

A drop-in Ren'Py mod for Pale Spectrum (Ren'Py 6.99.12, 32-bit Python 2.7). There is nothing to compile: the game loads the `.rpy` files in `game` and builds its own `.rpyc` files from them.

The mod contains nothing from the game. It never replaces the game's screens: one mod screen, `ps_a11y_global`, sits above them, works out which game screen is showing, and drives it from the keyboard. Text such as the credits and the gallery buttons is read from the shown screen while the game runs.

## Files

| Path | Purpose |
|---|---|
| `game/zz_ps_a11y_core.rpy` | Speech (Prism through ctypes), dialogue reading, story hotkeys, the keyboard menu engine (`a11y_nav`), the update check and the version number (`A11Y_VERSION`). |
| `game/zz_ps_a11y_screens.rpy` | `ps_a11y_global` and the menu items for each game screen, plus the F1 settings and q in-scene button pop-ups. |
| `game/zz_ps_a11y_descriptions.rpy` | Gallery picture titles and descriptions, and ending names, written for the mod. |
| `prism.dll` | Prism, 32-bit. It must sit next to `Pale Spectrum.exe`. |
| `prism_licenses/` | Prism's license and the licenses of the libraries it uses. |

To test, copy the files into a copy of the game folder as described in the README, so your real saves and settings aren't touched, and start the game. The mod writes `a11y_log.txt` next to `Pale Spectrum.exe`.

Things to know:

- This Python has no SSL support, so the update check runs Windows' own `curl.exe` in the background.
- The game's stdlib ships only as `.pyo` files; run the game's Python with `-O`.
- String literals in `.rpy` code are unicode, so check `isinstance(x, basestring)`, not `str`.

## Packaging and releasing

Build the release zip into `dist\PaleSpectrumAccess.zip`:

```
powershell -ExecutionPolicy Bypass -File scripts\package-release.ps1
```

To publish a release:

1. Update `A11Y_VERSION` in `zz_ps_a11y_core.rpy`, the version in the README, `changes-latest.md` and `CHANGELOG.md`.
2. Build the zip.
3. Create a draft GitHub release with the zip attached:

   ```
   gh release create vX.Y.Z --draft --notes-file changes-latest.md dist\PaleSpectrumAccess.zip
   ```

4. Run the **Release** workflow from the Actions tab with the same tag. It builds the installer, writes `loadstone-release.json`, and publishes the release.

The installer's package files are in `loadstone-packages`, and its settings are in `installer\profile.json`. The installer reads the package files straight from this repository, so changes to them reach players a few minutes after they're pushed.
