# BOUNCraft effect plug-ins

Two EffectCraft effect plug-ins, **BOUNCraft Overshoot** and **BOUNCraft Bounce Back**. Each one
only holds the values the BOUNCraft expressions read (On, Amplitude, Frequency, Decay, Floor /
On, Elasticity, Gravity, Max Bounces) and leaves the image as it is.

They're tiny WebAssembly modules (ABI 1). `build_plugin.py` writes them, no toolchain needed:

    python3 plugin/build_plugin.py

The release's `BOUNCraft-2.0-Plugin.zip` is a bundle folder with both `.wasm` files and
`BOUNCraft.jsx`, for **Effect ▸ Install Effect Plug-in Bundle (Folder)…**.
