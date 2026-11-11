# BOUNCraft — rules for agents and contributors

BOUNCraft is a ScriptUI panel for [EffectCraft](https://github.com/storytold/effectcraft) that adds
Overshoot and Bounce Back expressions, with an optional effect plug-in. Made by Hugo Mec
([@hugoeditor_](https://x.com/hugoeditor_)) for the EffectCraft Discord community.

## What's here

| Path | What |
|---|---|
| `BOUNCraft.jsx` | The panel (version 2). One self-contained file: the logo PNG is embedded in it. |
| `plugin/build_plugin.py` | Writes the two effect plug-ins, `BOUNCraft Overshoot.wasm` and `BOUNCraft Bounce Back.wasm` (no toolchain needed). |
| `plugin/*.wasm` | The built plug-ins. They only hold values; they leave the image as it is. |
| `tools/logo.py` | Makes the logo and embeds the panel's copy into `BOUNCraft.jsx`. |
| `images/` | README images. `images/v2/` is version 2; the rest is version 1.1. |

Version 1.1 lives only in its release (tag `v1.1`); `main` holds version 2.

## Rules

1. **Never write "After Effects" or "Adobe"** in issues, pull requests, release notes, the README or
   code comments. Say something like "the original BOUNCr script" or "the other app" instead.
2. **Never rename the controls or the plug-in's parameters.** The expressions find them by name, so
   renaming breaks every layer already bounced, including layers made with 1.1:
   - Slider / Checkbox Controls: `Overshoot - On`, `Overshoot - Amplitude`, `Overshoot - Frequency`,
     `Overshoot - Decay`, `Overshoot - Floor`, `Bounce - On`, `Bounce - Elasticity`,
     `Bounce - Gravity`, `Bounce - Max Bounces`.
   - Plug-in effects: ids `com.hugomec.bouncraft.overshoot` / `com.hugomec.bouncraft.bounce`, names
     `BOUNCraft Overshoot` / `BOUNCraft Bounce Back`, parameters `On`, `Amplitude`, `Frequency`,
     `Decay`, `Floor` / `On`, `Elasticity`, `Gravity`, `Max Bounces`.
   - The first line of every expression, `// BOUNCraft - Overshoot` or `// BOUNCraft - Bounce Back`:
     Bake and Remove find BOUNCraft's expressions by it.
3. **The panel is in English only.** The README is in English and Portuguese: change both.
4. **Two versions stay available.** 1.1 (simple) and 2 (preview, presets, axis, Bake, Remove, plug-in).
   The README has a section for each, in both languages, and the main image (`images/hero.png`)
   shows both panels. Don't remove 1.1's section, images or release.
5. **Written from scratch.** BOUNCraft shares no code with BOUNCr. The bounce maths follow Dan Ebberts'
   public inertial bounce and bounce-back expressions (credited in the README). Don't copy code,
   images or text from BOUNCr.
6. **Test in EffectCraft before a release**, on a real comp: Overshoot and Bounce Back on Position
   (also one axis), Scale, Rotation and Selected (an effect's property); presets (built-in, Save,
   Del); From Layer; Bake; Remove; the panel docked and floating; with and without the plug-in.
   Say what you tested and what you couldn't.
7. **Screenshots are PNG at full quality**, taken in EffectCraft by Hugo. No JPEG, no re-encoded
   pastes.
8. **Ask before publishing** a release, deleting a release or tag, or changing the repository's
   settings.

## How to

**Check the script.** No build is needed to run it. A quick syntax check:
`node -e "new Function(require('fs').readFileSync('BOUNCraft.jsx','utf8'))"`.
Then install it in EffectCraft (**File ▸ Scripts ▸ Install ScriptUI Panel…**) or run it as a
floating window (**File ▸ Scripts ▸ Run Script File…**).

**EffectCraft quirks the script relies on.**
- `alert()` only prints to the console: messages go to the panel's status line.
- An image control needs an explicit `preferredSize`.
- A docked panel takes its dock's size; a fixed width there adds scroll bars. Docked panels may show
  scroll bars anyway (storytold/effectcraft#2796); that's EffectCraft's, not the script's.
- `prompt()` returns its default: name things with an edit text in the panel instead.
- Expressions can read a switched-off effect, so the plug-in effect is added switched off (no render
  cost).

**Change the version.** Update `VERSION` in `BOUNCraft.jsx` and the header comment, then the logo:

    python3 tools/logo.py --fonts FONT_DIR --version 2.1 --embed

The fonts aren't in the repository (Eurostile is commercial). FONT_DIR must hold
`Eurostile MN Extended Bold.ttf` (Eurostile MN, Bold), `eurostile.TTF` (Eurostile, Regular) and
`JetBrainsMono[wght].ttf` (JetBrains Mono, free on Google Fonts). If the plug-in changes, also set
`VERSION` in `plugin/build_plugin.py` and run `python3 plugin/build_plugin.py`.

**Make a release.** Tag `vX.Y` on `main`. Attach:
- `BOUNCraft.jsx` (the script);
- `BOUNCraft-X.Y-Plugin.zip`: a folder named `BOUNCraft` holding `BOUNCraft.jsx`, both `.wasm` files
  and a short `LEIA-ME_README.txt` (EN + PT install steps). EffectCraft installs it with
  **Effect ▸ Install Effect Plug-in Bundle (Folder)…**.

Release notes in English, then a Portuguese paragraph, with a link to the README.

## Commits and pull requests

Short messages that say what changed for the user. Keep the README, the release notes and the panel
in step with each other.
