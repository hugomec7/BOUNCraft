# BOUNCraft — rules for agents and contributors

BOUNCraft is a ScriptUI panel for [EffectCraft](https://github.com/storytold/effectcraft) that adds
Overshoot and Bounce Back expressions. Made by Hugo Mec ([@hugoeditor_](https://x.com/hugoeditor_))
for the EffectCraft community.

## What's here

| Path | What |
|---|---|
| `BOUNCraft.jsx` | The panel. One self-contained file: the logo PNG is embedded in it. |
| `tools/logo.py` | Makes the logo and embeds the panel's copy into `BOUNCraft.jsx`. |
| `tools/zip-README.txt` | The `README.txt` that goes in the release zip. |
| `images/` | README images. |

One version is current (2.1 today). Older ones live only in their releases.

## Rules

1. **Never write "After Effects" or "Adobe"** in issues, pull requests, release notes, the README or
   code comments. Say something like "the original BOUNCr script" or "the other app" instead.
2. **Never change how the controls are named.** The expressions find them by name, so a change
   breaks every layer already bounced:
   - Since 2.2 every bounced property has its own controls, named `<property> - <value>`:
     `Scale - Amplitude`, `Scale - Frequency`, `Scale - Decay`, `Scale - Floor` (only when Floor is
     on), `Scale - Elasticity`, `Scale - Gravity`, `Scale - Max Bounces`. A property outside the
     layer's Transform has its group's name in front (`Transform Scale Height - Amplitude`).
   - Up to 2.1 a layer had one shared set: `Overshoot - On`, `Overshoot - Amplitude`,
     `Overshoot - Frequency`, `Overshoot - Decay`, `Overshoot - Floor`, `Bounce - On`,
     `Bounce - Elasticity`, `Bounce - Gravity`, `Bounce - Max Bounces`. The script no longer adds
     them but must keep reading them (From Layer, Bake, Remove).
   - With **Values in the expression** on, there are no controls: the values are the `var` lines
     under `// Change the values here:` at the top of the expression. Keep that line and those
     variable names (`amplitude`, `frequency`, `decay`, `floorOn`, `elasticity`, `gravity`,
     `maxBounces`): From Layer reads them back.
   - The first line of every expression, `// BOUNCraft - Overshoot` or `// BOUNCraft - Bounce Back`:
     Bake and Remove find BOUNCraft's expressions by it.
3. **No plug-in.** 2.0 shipped an optional effect plug-in (ids `com.hugomec.bouncraft.overshoot` /
   `com.hugomec.bouncraft.bounce`); it confused people and was dropped in 2.1. The script no longer
   adds those effects, but keep the code that reads them, so layers made with the plug-in still work
   with From Layer, Bake and Remove. Don't bring the plug-in back.
4. **Simple first.** The panel opens with Property, Type, Preset and Bounce It only; everything else sits
   behind **Advanced**. New options go in Advanced.
5. **English only**: the panel, the README, the release notes and the zip's `README.txt`.
6. **Keep the README short.** Simple words, few lines, something people actually read. The
   **INSTALL** section is text only, under a big heading, so it's easy to find while scrolling.
7. **Written from scratch.** BOUNCraft shares no code with BOUNCr. The bounce maths follow Dan
   Ebberts' public inertial bounce and bounce-back expressions (credited in the README). Don't copy
   code, images or text from BOUNCr.
8. **Test in EffectCraft before a release**, on a real comp: the simple panel and Advanced; Overshoot
   and Bounce Back on Position (also one axis), Scale, Rotation and Selected; presets (built-in,
   Save, Del); From Layer; Bake; Remove; the panel docked and floating. Say what you tested and what
   you couldn't.
9. **Screenshots are PNG at full quality**, taken in EffectCraft by Hugo. No JPEG, no re-encoded
   pastes.
10. **Commits are Hugo's.** Author `Hugo Mec <hugomec7@users.noreply.github.com>`, and no
    `Co-Authored-By` or other agent lines in commit messages or pull requests.
11. **Ask before publishing** a release, deleting a release or tag, or changing the repository's
    settings.

## How to

**Check the script.** No build is needed to run it. A quick syntax check:
`node -e "new Function(require('fs').readFileSync('BOUNCraft.jsx','utf8'))"`.
Then install it in EffectCraft (**File > Scripts > Install ScriptUI Panel...**) or run it as a
floating window (**File > Scripts > Run Script File...**). A docked panel only reloads the file when
EffectCraft restarts.

**EffectCraft quirks the script relies on.**
- `alert()` only prints to the console: messages go to the panel's status line.
- An image control needs an explicit `preferredSize`.
- A docked panel takes its dock's size; a fixed width there adds scroll bars. Docked panels may show
  scroll bars anyway (storytold/effectcraft#2796); that's EffectCraft's, not the script's.
- `prompt()` returns its default: name things with an edit text in the panel instead.
- Arrow characters render tiny in the UI font: the Advanced arrow is drawn in the button's `onDraw`.
- A hidden control (`visible = false`) takes no room after `layout.layout(true)`.

**Change the version.** Update `VERSION` in `BOUNCraft.jsx` and the header comment, then the logo:

    python3 tools/logo.py --fonts FONT_DIR --version 2.2 --embed

The fonts aren't in the repository (Eurostile is commercial). FONT_DIR must hold
`Eurostile MN Extended Bold.ttf` (Eurostile MN, Bold), `eurostile.TTF` (Eurostile, Regular) and
`JetBrainsMono[wght].ttf` (JetBrains Mono, free on Google Fonts).

**Make a release.** Tag `vX.Y` on `main`. Attach one file, `BOUNCraft-X.Y.zip`, holding
`BOUNCraft.jsx` and `README.txt` (from `tools/zip-README.txt`, with the version updated) at the top
level of the zip. Script sites list BOUNCraft with the steps "download the ZIP, unzip it, install it
from the Scripts menu, open it", so the zip must stay that simple.

Release notes: what's new in a few lines, then always a **HOW TO INSTALL** section (the same steps as
the README's INSTALL).
