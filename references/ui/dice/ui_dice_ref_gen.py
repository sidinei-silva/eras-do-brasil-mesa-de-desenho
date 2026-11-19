"""Gera d4, d6, d8, d10, d12 de dano (32 px) no padrão do d20 v2.

Geometria -> linhas (Bresenham) -> faces (cor pela posição da face vs. luz cima-esquerda)
-> números 3x5 -> brilho. Escreve .aseprite direto (formato documentado), sem Lua.
"""
import json, math, struct, sys, zlib
from pathlib import Path

W = H = 48
CX, CY = 24, 23.5
OUT = Path(sys.argv[1])

K = (0x1A, 0x15, 0x15)
DARK, MID, MIDL, LIGHT = (0x3D, 0x26, 0x1C), (0x7C, 0x5A, 0x3A), (0xA8, 0x70, 0x3E), (0xB8, 0x99, 0x76)
FRONT = MIDL
NUM = (0xF0, 0xE2, 0xB6)
SHINE = (0xD8, 0xB6, 0x7A)
GUIDE = (0xC0, 0x70, 0xF0)

PALETTE = """1A1515 2A1814 5A3426 8C5236 A8683F D39A6C E3B288 F4D3AE 0E2125 223C34 3D7A3C 86B04F
3D261C 7C5A3A A8703E B89976 D8B67A F0E2B6 26262F 4B4A55 7B7880 B3ACA2 0E2236 1B4A68 2E7F8E 78C2B8
3A4150 7F8896 DADDD6 2C1840 6E2C94 C070F0 6E1C22 C9402E F2C14E 7E575E""".split()

GLYPH = {
    "0": ["AAA", "A.A", "A.A", "A.A", "AAA"],
    "1": [".A.", "AA.", ".A.", ".A.", "AAA"],
    "2": ["AAA", "..A", "AAA", "A..", "AAA"],
    "3": ["AAA", "..A", "AAA", "..A", "AAA"],
    "4": ["A.A", "A.A", "AAA", "..A", "..A"],
    "5": ["AAA", "A..", "AAA", "..A", "AAA"],
    "6": ["AAA", "A..", "AAA", "A.A", "AAA"],
    "7": ["AAA", "..A", "..A", "..A", "..A"],
    "8": ["AAA", "A.A", "AAA", "A.A", "AAA"],
    "9": ["AAA", "A.A", "AAA", "..A", "AAA"],
}


def poly_regular(n, r, cx, cy, a0):
    return [(cx + r * math.cos(math.radians(a0 + 360 * i / n)), cy + r * math.sin(math.radians(a0 + 360 * i / n))) for i in range(n)]


def d12():
    o = poly_regular(10, 15.5, 24, 23.5, -90)
    f = poly_regular(5, 7.5, 24, 24.5, -90)
    pts = {f"o{i}": p for i, p in enumerate(o)} | {f"f{i}": p for i, p in enumerate(f)}
    faces = [("front", [f"f{i}" for i in range(5)])]
    for k in range(5):
        faces.append((f"n{k}", [f"f{k}", f"o{2*k}", f"o{(2*k+1)%10}", f"o{(2*k+2)%10}", f"f{(k+1)%5}"]))
    return pts, faces


DICE = {
    "d4": ({"T": (24, 8), "L": (9, 36), "F": (28, 39), "R": (39, 31)},
           [("front", ["T", "L", "F"]), ("right", ["T", "F", "R"])],
           [("right", "3")]),
    "d6": ({"a": (9, 17), "b": (30, 17), "c": (30, 39), "d": (9, 39), "e": (17, 9), "g": (38, 9), "h": (38, 31)},
           [("front", ["a", "b", "c", "d"]), ("top", ["a", "e", "g", "b"]), ("right", ["b", "g", "h", "c"])],
           [("top", "2"), ("right", "3")]),
    "d8": ({"T": (24, 8), "UR": (37, 16), "LR": (37, 31), "B": (24, 39), "LL": (11, 31), "UL": (11, 16)},
           [("front", ["T", "LR", "LL"]), ("left", ["T", "LL", "UL"]), ("right", ["T", "UR", "LR"]), ("bottom", ["LL", "LR", "B"])],
           [("left", "3"), ("right", "5"), ("bottom", "7")]),
    "d10": ({"T": (24, 8), "L": (9, 21), "LB": (9, 27), "B": (24, 39), "RB": (39, 27), "R": (39, 21),
             "FL": (16, 23), "FC": (24, 30), "FR": (32, 23)},
            [("front", ["T", "FL", "FC", "FR"]), ("ul", ["T", "L", "FL"]), ("ur", ["T", "FR", "R"]),
             ("ll", ["L", "LB", "B", "FC", "FL"]), ("lr", ["FC", "B", "RB", "R", "FR"])],
            [("ll", "3"), ("lr", "7")]),
    "d12": (*d12(), [("n0", "5"), ("n4", "9"), ("n1", "3"), ("n2", "7"), ("n3", "11")]),
}


def rot(p, deg, s):
    a = math.radians(deg)
    x, y = p[0] - CX, p[1] - CY
    return (CX + s * (x * math.cos(a) - y * math.sin(a)), CY + s * (x * math.sin(a) + y * math.cos(a)))


def line(p, q):
    x0, y0, x1, y1 = *p, *q
    dx, dy = abs(x1 - x0), -abs(y1 - y0)
    sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
    err, out = dx + dy, []
    while True:
        out.append((x0, y0))
        if (x0, y0) == (x1, y1):
            return out
        e2 = 2 * err
        if e2 >= dy:
            err += dy; x0 += sx
        if e2 <= dx:
            err += dx; y0 += sy


def inside(pt, poly):
    x, y, c = *pt, False
    for i in range(len(poly)):
        (x1, y1), (x2, y2) = poly[i], poly[i - 1]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            c = not c
    return c


def seg_dist(p, a, b):
    ax, ay, bx, by = *a, *b
    t = max(0, min(1, ((p[0] - ax) * (bx - ax) + (p[1] - ay) * (by - ay)) / ((bx - ax) ** 2 + (by - ay) ** 2 or 1)))
    return math.hypot(p[0] - ax - t * (bx - ax), p[1] - ay - t * (by - ay))


def shade(cent):
    dx, dy = cent[0] - CX, cent[1] - CY
    ang = math.degrees(math.acos(max(-1, min(1, (-dx - dy) / (math.sqrt(2) * math.hypot(dx, dy))))))
    return LIGHT if ang <= 60 else MIDL if ang <= 105 else MID if ang <= 157 else DARK


def render(name, deg, s, with_marks):
    pts, faces, numbers = DICE[name]
    P = {k: (round(v[0]), round(v[1])) for k, v in ((k, rot(v, deg, s)) for k, v in pts.items())}
    polys = {fn: [P[v] for v in vs] for fn, vs in faces}
    edges = set()
    for vs in polys.values():
        for i in range(len(vs)):
            edges.add(tuple(sorted((vs[i], vs[i - 1]))))
    lines = set()
    for a, b in edges:
        # desenha sempre do ponto de cima (menor y) para manter os degraus iguais nas duas metades
        a, b = sorted((a, b), key=lambda p: (p[1], p[0]))
        lines.update(line(a, b))
    color = {}
    for fn, poly in polys.items():
        cx = sum(p[0] for p in poly) / len(poly); cy = sum(p[1] for p in poly) / len(poly)
        color[fn] = FRONT if fn == "front" else shade((cx, cy))
    faces_px, owner = {}, {}
    for y in range(H):
        for x in range(W):
            c = (x + 0.5 - 0.5, y)  # centro do pixel em coordenadas de vértice
            hit = [fn for fn, poly in polys.items() if inside(c, poly)]
            if not hit and (x, y) in lines:
                # pixel em cima da linha: a cor vem da face mais próxima do centro (continua por baixo da linha)
                for off in ((0.3, 0.3), (-0.3, 0.3), (0.3, -0.3), (-0.3, -0.3), (0, 0.4), (0.4, 0), (0, -0.4), (-0.4, 0)):
                    q = (CX + (c[0] - CX) * 0.9 + off[0], CY + (c[1] - CY) * 0.9 + off[1])
                    hit = [fn for fn, poly in polys.items() if inside(q, poly)]
                    if hit:
                        break
            if hit:
                faces_px[(x, y)] = color[hit[0]]
                owner[(x, y)] = hit[0]
    lines_px = {p: K for p in lines}
    nums, shine, report = {}, {}, []
    if with_marks:
        for fn, txt in numbers:
            poly = polys[fn]
            gw = 4 * len(txt) - 1
            best = None
            cx = sum(p[0] for p in poly) / len(poly); cy = sum(p[1] for p in poly) / len(poly)
            for oy in range(-10, 11):
                for ox in range(-10, 11):
                    x0, y0 = round(cx - gw / 2 + 0.5) + ox, round(cy - 2.5 + 0.5) + oy
                    gp = [(x0 + 4 * ci + i, y0 + j) for ci, ch in enumerate(txt) for j, row in enumerate(GLYPH[ch]) for i, c in enumerate(row) if c == 'A']
                    # glifo inteiro na face e 1 px de folga reta (diagonal pode encostar)
                    box = gp + [(x + dx, y + dy) for x, y in gp for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))]
                    if all(owner.get(p) == fn and p not in lines for p in box):
                        d = ox * ox + oy * oy
                        if best is None or d < best[0]:
                            best = (d, x0, y0)
            if not best:
                report.append(f"{name}: '{txt}' não coube na face {fn}")
                continue
            _, x0, y0 = best
            report.append(f"{name}: '{txt}' na face {fn} em ({x0},{y0})")
            for ci, ch in enumerate(txt):
                for j, row in enumerate(GLYPH[ch]):
                    for i, c in enumerate(row):
                        if c == "A":
                            nums[(x0 + 4 * ci + i, y0 + j)] = NUM
        # brilho: 3 px logo dentro da borda de fora mais voltada para cima-esquerda
        outer = [e for e in edges if sum(1 for poly in polys.values()
                                         for i in range(len(poly)) if tuple(sorted((poly[i], poly[i - 1]))) == e) == 1]
        def facing(e):
            mx, my = (e[0][0] + e[1][0]) / 2 - CX, (e[0][1] + e[1][1]) / 2 - CY
            return (-mx - my) / math.hypot(mx, my)
        e = max(outer, key=facing)
        a, b = sorted(e, key=lambda p: (p[1], p[0]))
        seg = line(a, b)
        cand = []
        for (x, y) in seg:
            for dx, dy in ((1, 0), (0, 1), (1, 1)):
                q = (x + dx, y + dy)
                if q in faces_px and q not in lines and q not in cand and q not in nums:
                    cand.append(q); break
        mid = len(cand) // 2
        for q in cand[max(0, mid - 1): mid + 2]:
            shine[q] = SHINE
        # 2 px sob o vértice de cima da frente
        top = min(polys["front"], key=lambda p: (p[1], abs(p[0] - CX)))
        for q in ((top[0], top[1] + 2), (top[0], top[1] + 3)):
            if owner.get(q) == "front" and q not in lines:
                shine[q] = SHINE
    return {"faces": faces_px, "linhas": lines_px, "numeros": nums, "brilho": shine}, color, report


# ---------- escrita .aseprite ----------
def s_str(t):
    b = t.encode(); return struct.pack("<H", len(b)) + b


def chunk(t, data):
    return struct.pack("<IH", len(data) + 6, t) + data


def cel(li, px):
    if not px:
        return None
    xs = [p[0] for p in px]; ys = [p[1] for p in px]
    x0, y0, x1, y1 = min(xs), min(ys), max(xs), max(ys)
    w, h = x1 - x0 + 1, y1 - y0 + 1
    raw = bytearray(w * h * 4)
    for (x, y), c in px.items():
        i = ((y - y0) * w + (x - x0)) * 4
        raw[i:i + 4] = bytes((*c, 255))
    data = struct.pack("<HhhBHh5x", li, x0, y0, 255, 2, 0) + struct.pack("<HH", w, h) + zlib.compress(bytes(raw))
    return chunk(0x2005, data)


LAYERS = ["faces", "linhas", "numeros", "brilho", "guia"]


def write_ase(path, frames):
    guide = {}
    for i in range(8, 40):
        for p in ((i, 8), (i, 39), (8, i), (39, i)):
            guide[p] = GUIDE
    blob = b""
    for fi, layers in enumerate(frames):
        chunks = []
        if fi == 0:
            for name in LAYERS:
                flags = 2 | (0 if name == "guia" else 1)
                chunks.append(chunk(0x2004, struct.pack("<HHHHHHB3x", flags, 0, 0, 0, 0, 0, 255) + s_str(name)))
            pal = struct.pack("<III8x", len(PALETTE), 0, len(PALETTE) - 1)
            for hx in PALETTE:
                pal += struct.pack("<H4B", 0, *bytes.fromhex(hx), 255)
            chunks.append(chunk(0x2019, pal))
            tags = [("idle", 0, 0), ("spin", 1, len(frames) - 1)]
            t = struct.pack("<H8x", len(tags))
            for n, a, b in tags:
                t += struct.pack("<HHBH6x3Bx", a, b, 0, 0, 0, 0, 0) + s_str(n)
            chunks.append(chunk(0x2018, t))
        layers = dict(layers, guia=guide)
        for li, name in enumerate(LAYERS):
            c = cel(li, layers.get(name))
            if c:
                chunks.append(c)
        body = b"".join(chunks)
        blob += struct.pack("<IHHH2xI", len(body) + 16, 0xF1FA, len(chunks), 80, len(chunks)) + body
    header = struct.pack("<IHHHHHIHIIB3xHBBhhHH84x", 128 + len(blob), 0xA5E0, len(frames), W, H, 32, 1, 80, 0, 0, 0, 0, 1, 1, 0, 0, 16, 16)
    assert len(header) == 128
    path.write_bytes(header + blob)


OUT.mkdir(parents=True, exist_ok=True)
summary = {}
for name in DICE:
    frames, colors = [], []
    for deg, s, marks in ((0, 1, True), (0, 1, False), (20, 1, False), (40, 0.97, False)):
        layers, color, rep = render(name, deg, s, marks)
        frames.append(layers); colors.append({k: "#%02X%02X%02X" % v for k, v in color.items()})
        if marks:
            print("\n".join(rep))
    write_ase(OUT / f"ui_{name}_ref.aseprite", frames)
    summary[name] = colors[1:]
print(json.dumps(summary, indent=0))
