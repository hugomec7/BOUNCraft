/*
 * BOUNCraft 1.0 — inertial bounce for EffectCraft.
 *
 * Adds an Overshoot or Bounce Back expression to Position, Scale, Rotation or the selected
 * properties of the selected layers, plus the controls for it on each layer.
 *
 * Install: File > Scripts > Install ScriptUI Panel..., restart, then Window > BOUNCraft.jsx.
 *
 * Made by Hugo Mec (@hugoeditor_ — https://x.com/hugoeditor_).
 * The bounce maths follow Dan Ebberts' inertial bounce and bounce-back expressions
 * (motionscript.com). Written from scratch.
 *
 * License: MIT (see LICENSE).
 */

(function BOUNCraft(thisObj) {
    var NAME = "BOUNCraft";
    var VERSION = "1.0";

    // Controls added to the layer. The expressions find them by these names.
    var TYPES = {
        overshoot: {
            label: "Overshoot",
            controls: [
                { name: "Overshoot - Amplitude", kind: "slider", value: 50 },
                { name: "Overshoot - Frequency", kind: "slider", value: 2 },
                { name: "Overshoot - Decay", kind: "slider", value: 4 },
                { name: "Overshoot - Floor", kind: "checkbox", value: 0 }
            ]
        },
        bounce: {
            label: "Bounce Back",
            controls: [
                { name: "Bounce - Elasticity", kind: "slider", value: 50 },
                { name: "Bounce - Gravity", kind: "slider", value: 50 },
                { name: "Bounce - Max Bounces", kind: "slider", value: 10 }
            ]
        }
    };

    var MATCH = {
        slider: "ADBE Slider Control",
        checkbox: "ADBE Checkbox Control"
    };

    // ---------------------------------------------------------------------------------------
    // Expressions. Both look back to the last keyframe before the current time and keep the
    // motion going from the speed the property had when it reached that keyframe.

    var EXPR_OVERSHOOT = [
        "// " + NAME + " - Overshoot",
        "var amp = effect(\"Overshoot - Amplitude\")(1) / 1000;",
        "var freq = effect(\"Overshoot - Frequency\")(1);",
        "var decay = effect(\"Overshoot - Decay\")(1);",
        "var floorOn = effect(\"Overshoot - Floor\")(1) == 1;",
        "var out = value;",
        "var n = 0;",
        "if (numKeys > 0) {",
        "    n = nearestKey(time).index;",
        "    if (key(n).time > time) n--;",
        "}",
        "if (n > 0) {",
        "    var t = time - key(n).time;",
        "    var v = velocityAtTime(key(n).time - thisComp.frameDuration / 10);",
        "    var wave = Math.sin(freq * t * 2 * Math.PI);",
        "    if (floorOn) wave = -Math.abs(wave);",
        "    out = add(value, mul(v, amp * wave / Math.exp(decay * t)));",
        "}",
        "out;"
    ].join("\n");

    var EXPR_BOUNCE = [
        "// " + NAME + " - Bounce Back",
        "var elasticity = effect(\"Bounce - Elasticity\")(1) / 100;",
        "var gravity = effect(\"Bounce - Gravity\")(1) * 100;",
        "var maxBounces = effect(\"Bounce - Max Bounces\")(1);",
        "var out = value;",
        "var n = 0;",
        "if (numKeys > 0) {",
        "    n = nearestKey(time).index;",
        "    if (key(n).time > time) n--;",
        "}",
        "if (n > 0 && gravity > 0) {",
        "    var t = time - key(n).time;",
        "    var v = mul(velocityAtTime(key(n).time - 0.001), -elasticity);",
        "    var speed = length(v);",
        "    var dir;",
        "    if (typeof value == \"number\") dir = v < 0 ? -1 : 1;",
        "    else dir = speed > 0 ? normalize(v) : mul(v, 0);",
        "    var start = 0;",
        "    var hop = 2 * speed / gravity;",
        "    var end = hop;",
        "    var count = 1;",
        "    while (end < t && count <= maxBounces) {",
        "        speed *= elasticity;",
        "        hop *= elasticity;",
        "        start = end;",
        "        end += hop;",
        "        count++;",
        "    }",
        "    if (count <= maxBounces) {",
        "        var d = t - start;",
        "        out = add(value, mul(dir, d * (speed - gravity * d / 2)));",
        "    }",
        "}",
        "out;"
    ].join("\n");

    function expressionFor(type) {
        return type === "overshoot" ? EXPR_OVERSHOOT : EXPR_BOUNCE;
    }

    // ---------------------------------------------------------------------------------------
    // Helpers

    var CONTROL_NAMES = (function () {
        var all = {};
        for (var t in TYPES) {
            for (var i = 0; i < TYPES[t].controls.length; i++) all[TYPES[t].controls[i].name] = t;
        }
        return all;
    })();

    // Messages show in the panel's status line (some apps only print alert() to a console),
    // and also go to alert().
    var status = null;
    function tell(msg) {
        if (status) {
            try { status.text = msg; } catch (e) {}
        }
        try { alert(msg, NAME); } catch (e) {}
    }

    function findEffect(layer, name) {
        var fx = layer.property("ADBE Effect Parade");
        if (!fx) return null;
        for (var i = 1; i <= fx.numProperties; i++) {
            var e = fx.property(i);
            if (e && e.name === name) return e;
        }
        return null;
    }

    // Adds the controls of `type` to `layer`, keeping the ones already there (and their values).
    function ensureControls(layer, type) {
        var fx = layer.property("ADBE Effect Parade");
        if (!fx) throw new Error("\"" + layer.name + "\" can't take effects");
        var list = TYPES[type].controls;
        for (var i = 0; i < list.length; i++) {
            var c = list[i];
            if (findEffect(layer, c.name)) continue;
            var e = fx.addProperty(MATCH[c.kind]);
            e.name = c.name;
            e.property(1).setValue(c.value);
        }
    }

    // Is a control of `type` still used by an expression on this layer?
    function typeInUse(layer, type) {
        var names = TYPES[type].controls;
        var found = false;
        function walk(group, depth) {
            if (found || !group || depth > 6) return;
            for (var i = 1; i <= group.numProperties; i++) {
                var p = group.property(i);
                if (!p) continue;
                if (p.propertyType === PropertyType.PROPERTY) {
                    var src = "";
                    try { src = p.expressionEnabled ? p.expression : ""; } catch (e) { src = ""; }
                    if (!src) continue;
                    for (var k = 0; k < names.length; k++) {
                        if (src.indexOf("\"" + names[k].name + "\"") !== -1) { found = true; return; }
                    }
                } else {
                    walk(p, depth + 1);
                }
            }
        }
        walk(layer.property("ADBE Transform Group"), 1);
        walk(layer.property("ADBE Effect Parade"), 1);
        return found;
    }

    // Removes the controls of `type` from `layer` when no expression uses them any more,
    // so re-applying with the other type doesn't leave unused controls behind.
    function removeIfUnused(layer, type) {
        if (typeInUse(layer, type)) return;
        var list = TYPES[type].controls;
        for (var i = 0; i < list.length; i++) {
            var e = findEffect(layer, list[i].name);
            if (e) e.remove();
        }
    }

    // The layer property that a Property menu entry names.
    function transformProperty(layer, which) {
        var tr = layer.property("ADBE Transform Group");
        if (!tr) return [];
        if (which === "rotation") return [tr.property("ADBE Rotate Z")];
        if (which === "scale") return [tr.property("ADBE Scale")];
        var pos = tr.property("ADBE Position");
        if (pos && pos.dimensionsSeparated) {
            var out = [];
            var sep = ["ADBE Position_0", "ADBE Position_1", "ADBE Position_2"];
            for (var i = 0; i < sep.length; i++) {
                var s = tr.property(sep[i]);
                if (s && (i < 2 || layer.threeDLayer)) out.push(s);
            }
            return out;
        }
        return [pos];
    }

    function isOwnControl(prop) {
        var g = prop.parentProperty;
        return !!(g && g.isEffect && CONTROL_NAMES.hasOwnProperty(g.name));
    }

    // [{layer, prop}] to work on.
    function targets(comp, which) {
        var out = [];
        if (which === "selected") {
            var sel = comp.selectedProperties;
            for (var i = 0; i < sel.length; i++) {
                var p = sel[i];
                if (p.propertyType !== PropertyType.PROPERTY) continue;
                if (isOwnControl(p)) continue;
                out.push({ layer: p.propertyGroup(p.propertyDepth), prop: p });
            }
            return out;
        }
        var layers = comp.selectedLayers;
        for (var j = 0; j < layers.length; j++) {
            var props = transformProperty(layers[j], which);
            for (var k = 0; k < props.length; k++) {
                if (props[k]) out.push({ layer: layers[j], prop: props[k] });
            }
        }
        return out;
    }

    function bounce(which, type) {
        var comp = app.project.activeItem;
        if (!comp || !(comp instanceof CompItem)) {
            tell("Open a composition first.");
            return;
        }
        var list = targets(comp, which);
        if (list.length === 0) {
            tell(which === "selected"
                ? "Select one or more properties (Position, Scale, Rotation, an effect's property...)."
                : "Select one or more layers.");
            return;
        }
        var other = type === "overshoot" ? "bounce" : "overshoot";
        var done = 0;
        var skipped = [];
        var touched = [];
        app.beginUndoGroup(NAME + ": " + TYPES[type].label);
        try {
            for (var i = 0; i < list.length; i++) {
                var layer = list[i].layer;
                var prop = list[i].prop;
                if (!prop.canSetExpression) {
                    skipped.push(layer.name + " > " + prop.name);
                    continue;
                }
                ensureControls(layer, type);
                prop.expression = expressionFor(type);
                prop.expressionEnabled = true;
                done++;
                var seen = false;
                for (var t = 0; t < touched.length; t++) if (touched[t] === layer) seen = true;
                if (!seen) touched.push(layer);
            }
            for (var l = 0; l < touched.length; l++) removeIfUnused(touched[l], other);
        } catch (err) {
            tell("Something went wrong: " + err.message);
        } finally {
            app.endUndoGroup();
        }
        var report = TYPES[type].label + " added to " + done + " propert" + (done === 1 ? "y" : "ies") + ".";
        if (skipped.length) report += "\nThese can't take an expression:\n" + skipped.join("\n");
        if (skipped.length) tell(report);
        else if (status) status.text = report;
    }

    // ---------------------------------------------------------------------------------------
    // Panel

    function build(host) {
        var win = (host instanceof Panel)
            ? host
            : new Window("palette", NAME + " " + VERSION, undefined, { resizeable: true });
        win.orientation = "column";
        win.alignChildren = ["fill", "top"];
        win.spacing = 8;
        win.margins = 10;

        var title = win.add("statictext", undefined, NAME + " " + VERSION);
        title.alignment = ["center", "top"];

        var row1 = win.add("group");
        row1.orientation = "row";
        row1.add("statictext", undefined, "Property");
        var prop = row1.add("dropdownlist", undefined, ["Position", "Scale", "Rotation", "Selected"]);
        prop.selection = 1;
        prop.alignment = ["fill", "center"];

        var row2 = win.add("group");
        row2.orientation = "row";
        row2.add("statictext", undefined, "Type");
        var kind = row2.add("dropdownlist", undefined, ["Overshoot", "Bounce Back"]);
        kind.selection = 0;
        kind.alignment = ["fill", "center"];

        var go = win.add("button", undefined, "Bounce It");

        status = win.add("statictext", undefined, "Select layers, then Bounce It.", { multiline: true });
        status.alignment = ["fill", "top"];

        var keys = ["position", "scale", "rotation", "selected"];
        go.onClick = function () {
            try {
                bounce(keys[prop.selection.index], kind.selection.index === 0 ? "overshoot" : "bounce");
            } catch (err) {
                tell("Error: " + (err && err.message ? err.message : err));
            }
        };

        win.onResizing = win.onResize = function () { this.layout.resize(); };
        if (win instanceof Window) {
            win.center();
            win.show();
        } else {
            win.layout.layout(true);
        }
        return win;
    }

    build(thisObj);
})(this);
