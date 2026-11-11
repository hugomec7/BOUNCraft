"""Builds the BOUNCraft effect plug-ins: two tiny WebAssembly modules (ABI 1) for EffectCraft.

Each module only describes an effect (its manifest) and leaves the pixels as they are: the
effect holds the values the BOUNCraft expressions read. No toolchain is needed: this script
writes the WebAssembly binary itself.

    python3 plugin/build_plugin.py   ->  plugin/BOUNCraft Overshoot.wasm, plugin/BOUNCraft Bounce Back.wasm
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
VERSION = "2.0.0"
AUTHOR = "Hugo Mec (@hugoeditor_)"

EFFECTS = [
    {
        "file": "BOUNCraft Overshoot.wasm",
        "manifest": {
            "api": 1,
            "id": "com.hugomec.bouncraft.overshoot",
            "name": "BOUNCraft Overshoot",
            "category": "Expression Controls",
            "version": VERSION,
            "author": AUTHOR,
            "description": "Holds the values of a BOUNCraft Overshoot. Leaves the image as it is.",
            "params": [
                {"id": "on", "name": "On", "type": "checkbox", "default": True},
                {"id": "amplitude", "name": "Amplitude", "type": "slider", "default": 50, "min": 0, "max": 1000, "sliderMax": 200, "decimals": 0},
                {"id": "frequency", "name": "Frequency", "type": "slider", "default": 2, "min": 0, "max": 100, "sliderMax": 10, "decimals": 1},
                {"id": "decay", "name": "Decay", "type": "slider", "default": 4, "min": 0, "max": 100, "sliderMax": 20, "decimals": 1},
                {"id": "floor", "name": "Floor", "type": "checkbox", "default": False},
            ],
        },
    },
    {
        "file": "BOUNCraft Bounce Back.wasm",
        "manifest": {
            "api": 1,
            "id": "com.hugomec.bouncraft.bounce",
            "name": "BOUNCraft Bounce Back",
            "category": "Expression Controls",
            "version": VERSION,
            "author": AUTHOR,
            "description": "Holds the values of a BOUNCraft Bounce Back. Leaves the image as it is.",
            "params": [
                {"id": "on", "name": "On", "type": "checkbox", "default": True},
                {"id": "elasticity", "name": "Elasticity", "type": "slider", "default": 50, "min": 0, "max": 100, "decimals": 0},
                {"id": "gravity", "name": "Gravity", "type": "slider", "default": 50, "min": 0, "max": 10000, "sliderMax": 200, "decimals": 0},
                {"id": "max_bounces", "name": "Max Bounces", "type": "slider", "default": 10, "min": 0, "max": 100, "sliderMax": 20, "decimals": 0},
            ],
        },
    },
]

MANIFEST_AT = 16      # the manifest's address in memory
BUFFER_AT = 65536     # the frame buffer handed to the host (page 1 on)


def uleb(n):
    out = bytearray()
    while True:
        b = n & 0x7F
        n >>= 7
        if n:
            out.append(b | 0x80)
        else:
            out.append(b)
            return bytes(out)


def sleb(n):
    out = bytearray()
    while True:
        b = n & 0x7F
        n >>= 7
        if (n == 0 and not b & 0x40) or (n == -1 and b & 0x40):
            out.append(b)
            return bytes(out)
        out.append(b | 0x80)


def vec(items):
    return uleb(len(items)) + b"".join(items)


def name(s):
    b = s.encode()
    return uleb(len(b)) + b


def section(sid, body):
    return bytes([sid]) + uleb(len(body)) + body


I32, F64 = 0x7F, 0x7C


def functype(params, results):
    return b"\x60" + vec([bytes([p]) for p in params]) + vec([bytes([r]) for r in results])


def i32_const(n):
    return b"\x41" + sleb(n)


def body(code, locals_=()):
    loc = vec([uleb(c) + bytes([t]) for c, t in locals_])
    b = loc + code + b"\x0b"
    return uleb(len(b)) + b


def module(manifest_json):
    data = manifest_json.encode("utf-8")
    assert MANIFEST_AT + len(data) < BUFFER_AT
    types = [
        functype([], [I32]),                                        # 0: () -> i32
        functype([I32], [I32]),                                     # 1: (i32) -> i32
        functype([I32, I32, I32, I32, I32, F64, F64], [I32]),      # 2: ec_render
    ]
    funcs = [0, 0, 0, 1, 2]
    # ec_alloc(bytes): grow memory so that [BUFFER_AT, BUFFER_AT + bytes) fits, return BUFFER_AT.
    #   need = (BUFFER_AT + bytes + 65535) >>u 16
    #   if need > memory.size: memory.grow(need - memory.size) (failure: the host's write fails)
    alloc = (
        b"\x20\x00" + i32_const(BUFFER_AT + 65535) + b"\x6a"   # local.get 0; i32.const; i32.add
        + i32_const(16) + b"\x76"                            # i32.shr_u
        + b"\x22\x01"                                        # local.tee 1 (need)
        + b"\x3f\x00"                                        # memory.size
        + b"\x4b"                                            # i32.gt_u
        + b"\x04\x40"                                        # if (no result)
        + b"\x20\x01" + b"\x3f\x00" + b"\x6b"                # need - memory.size
        + b"\x40\x00" + b"\x1a"                              # memory.grow; drop
        + b"\x0b"                                            # end if
        + i32_const(BUFFER_AT)
    )
    codes = [
        body(i32_const(1)),                 # ec_api_version
        body(i32_const(MANIFEST_AT)),       # ec_manifest_ptr
        body(i32_const(len(data))),         # ec_manifest_len
        body(alloc, [(1, I32)]),            # ec_alloc
        body(i32_const(0)),                 # ec_render: the pixels stay as they are
    ]
    exports = [
        name("memory") + b"\x02" + uleb(0),
        name("ec_api_version") + b"\x00" + uleb(0),
        name("ec_manifest_ptr") + b"\x00" + uleb(1),
        name("ec_manifest_len") + b"\x00" + uleb(2),
        name("ec_alloc") + b"\x00" + uleb(3),
        name("ec_render") + b"\x00" + uleb(4),
    ]
    out = b"\x00asm\x01\x00\x00\x00"
    out += section(1, vec(types))
    out += section(3, vec([uleb(f) for f in funcs]))
    out += section(5, vec([b"\x00" + uleb(2)]))   # memory: 2 pages to start, no maximum
    out += section(7, vec(exports))
    out += section(10, vec(codes))
    out += section(11, vec([b"\x00" + i32_const(MANIFEST_AT) + b"\x0b" + uleb(len(data)) + data]))
    return out


if __name__ == "__main__":
    for e in EFFECTS:
        wasm = module(json.dumps(e["manifest"], separators=(",", ":")))
        path = os.path.join(HERE, e["file"])
        with open(path, "wb") as f:
            f.write(wasm)
        print(e["file"], len(wasm), "bytes")
