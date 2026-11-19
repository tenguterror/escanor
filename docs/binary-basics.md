# Binary Basics — Tengu's Reference Sheet

Everything learned so far about reading binary files, using the real E46 Bihoku replay as the example.
Kept by Baus; add to it as new concepts come up.

---

## 1. Hex: counting in sixteens

Decimal has 10 digits per place (0–9). **Hex has 16:**

```
hex:      0 1 2 3 4 5 6 7 8 9  a  b  c  d  e  f  10
decimal:  0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15  16
```

Think of an odometer whose wheels roll over after `f` instead of after `9`.

**Reading a two-digit hex number:** the left digit is the **sixteens** place, the right digit is the **ones** place.

| Hex | Math | Decimal |
|---|---|---|
| `0a` | 0×16 + 10 | 10 |
| `10` | 1×16 + 0 | 16 |
| `17` | 1×16 + 7 | 23 |
| `2e` | 2×16 + 14 | 46 |
| `ff` | 15×16 + 15 | 255 (the biggest value one byte can hold) |

- **One byte = two hex digits**, always. Small values get a leading zero: decimal 10 is `0a`, not `a0`. (`a0` is 160.)
- Watch the direction. "Hex 10 in decimal" (= 16) is the opposite question from "decimal 10 in hex" (= `a`).

---

## 2. Little-endian vs big-endian

A 4-byte number is stored as 4 pieces. **Byte order** decides which piece comes first.

| | Rule | 16 is stored as | 23 is stored as |
|---|---|---|---|
| **Little-endian** | smallest piece first | `10 00 00 00` | `17 00 00 00` |
| Big-endian | biggest piece first | `00 00 00 10` | `00 00 00 17` |

- Assetto Corsa replays (and almost every PC) use **little-endian**.
- Read with the wrong order and you get a huge, believable, **wrong** number **with no error**. Proven Nov 18: `10 00 00 00` read as big-endian gave **268,435,456**. That's why the parser must check that values make sense.

---

## 3. Looking at a file with `xxd`

```bash
xxd "/path/to/replay.acreplay" | head -2
```

```
00000000: 1000 0000 0000 0000 0000 2e40 1700 0000  ...........@....
00000010: 736f 6c5f 3033 5f73 6361 7474 6572 6564  sol_03_scattered
```

- `00000000:` is the **offset** (where this line starts, in hex). Not data. The second line starts at hex `10` = byte 16.
- Then 16 bytes, shown in pairs: `1000 0000` is really 4 separate bytes: `10 00 00 00`.
- On the right is the same bytes as text. `.` means "not printable."

---

## 4. Bytes in Python

| Code | What it does |
|---|---|
| `open(path, "rb")` | Opens in **binary** mode: raw bytes, no text decoding, no line-ending changes |
| `with ... as f:` | Closes the file automatically, even if something crashes |
| `f.read(4)` | Returns a **bytes** object, up to 4 bytes long (can be fewer if the file ends!) |
| `len(data)` | How many bytes you actually got |
| `int.from_bytes(data, byteorder="little")` | Turns bytes into an integer |

Python prints bytes like `b'\x10\x00\x00\x00'`:
- `b'...'` = a bytes object, raw data, not text
- `\x10` = one byte with hex value `10`

---

## 5. The file bookmark

An open file **remembers its position**. Every `.read(n)` starts where the last one ended and moves the bookmark forward by `n`.

```
start            bookmark at byte 0
read 4 bytes  →  bookmark at byte 4
read 8 bytes  →  bookmark at byte 12
read 4 bytes  →  bookmark at byte 16
```

This is how a parser reads a file **field by field, in the order it was written**, instead of grabbing a fixed chunk and hoping everything fits (the v1 bug).

---

## 6. Length-prefixed strings

Text of unknown length is stored as:

```
[ 4-byte length ][ that many bytes of text ]
```

To read one: read the 4-byte length → convert it to a number → read exactly that many bytes → decode them as text.

---

## 7. `.acreplay` header map (v16, what we know so far)

From the real E46 Bihoku replay. ✅ = decoded by Tengu's code; 🔍 = seen but not yet decoded.

| Bytes | Raw (hex) | Meaning | Status |
|---|---|---|---|
| 0–3 | `10 00 00 00` | Version = 16 (4-byte little-endian int) | ✅ step 1 |
| 4–11 | `00 00 00 00 00 00 2e 40` | Unknown, 8 bytes | 🔍 step 5 |
| 12–15 | `17 00 00 00` | Weather name length = 23 | 🔍 step 2 |
| 16–38 | `sol_03_scattered...` | Weather name text (23 bytes) | 🔍 step 2 |
| 39+ | ? | Track name length, then track name (from v1) | 🔍 step 3 |
