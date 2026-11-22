#!/usr/bin/env python3
"""
oci_prep.py - prepare phone photos for the OCI "Passport Particulars Updation"
(Miscellaneous Services) on https://ociservices.gov.in

Portal rules this script targets (verified Nov 2026):
  Photo      : JPEG, square, 200x200 .. 900x900 px, < 500 KB (we aim < 200 KB),
               head (crown->chin) ~50-69% of frame, light background, taken < 30 days ago
  Signature  : JPEG, aspect 3:1, 200x67 .. 900x300 px, small file
  Documents  : PDF only, < 1000 KB each (we aim < 900 KB)

Usage examples (folder per person, e.g. D:\\OCI\\Mom):
  python oci_prep.py photo  Mom/Photo.jpg  --crown 0.31 --chin 0.565 --cx 0.475
  python oci_prep.py sign   Mom/Signature.jpg --box 0.15 0.40 0.80 0.53
  python oci_prep.py doc    Mom/NewPassport.jpg --rotate 90 --box 0.0 0.1 0.96 0.86
  python oci_prep.py preview Mom/            (makes a contact sheet to eyeball orientation)

All --box / --crown / --chin / --cx values are FRACTIONS (0-1) of the image AFTER
EXIF orientation and --rotate are applied. Outputs go to <folder>/OCI_Ready/
as <name>_OCIready.jpg / .pdf. Originals are never modified.
Easiest: python oci_prep.py auto MyFiles   (or double-click RUN-ME.bat on Windows)
Requires: pip install -r requirements.txt
"""
import argparse, io, os, sys
from PIL import Image, ImageOps, ImageDraw

def load(path, rotate=0):
    im = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    return im.rotate(rotate, expand=True) if rotate else im   # +90 = counter-clockwise

def out_path(src, ext):
    d = os.path.join(os.path.dirname(os.path.abspath(src)), "OCI_Ready")
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, os.path.splitext(os.path.basename(src))[0] + "_OCIready" + ext)

def jpeg_under(im, max_kb, q=92):
    while True:
        b = io.BytesIO(); im.save(b, "JPEG", quality=q, optimize=True)
        if b.tell() <= max_kb * 1024 or q <= 40: return b.getvalue(), q
        q -= 4

def frac_box(im, a, b, c, d):
    W, H = im.size
    return (int(a * W), int(b * H), int(c * W), int(d * H))

def cmd_photo(a):
    im = load(a.file, a.rotate); W, H = im.size
    head = (a.chin - a.crown) * H
    side = min(int(head / a.head_ratio), W, H)
    left = int(min(max(a.cx * W - side / 2, 0), W - side))
    top = int(min(max(a.crown * H - a.top_margin * side, 0), H - side))
    sq = im.crop((left, top, left + side, top + side)).resize((600, 600), Image.LANCZOS)
    data, q = jpeg_under(sq, 195)
    p = out_path(a.file, ".jpg"); open(p, "wb").write(data)
    print(f"{p}  600x600  {len(data)//1024} KB  head={100*head/side:.0f}% of frame (target 50-69%)")

def cmd_sign(a):
    import numpy as np, cv2
    g = np.array(load(a.file, a.rotate).convert("L")).astype(float)
    bg = cv2.GaussianBlur(g, (0, 0), 40)                  # flatten uneven lighting
    n = np.clip(g / np.maximum(bg, 1) * 255, 0, 255)
    n = np.clip((n - 110) * 255 / (225 - 110), 0, 255).astype("uint8")   # white paper, dark ink
    im = Image.fromarray(n)
    x0, y0, x1, y1 = frac_box(im, *a.box)
    w = x1 - x0; h = y1 - y0; cy = (y0 + y1) / 2; cx = (x0 + x1) / 2
    if w / h > 3: h = w / 3
    else: w = h * 3                                       # force 3:1
    box = (int(cx - w/2), int(cy - h/2), int(cx + w/2), int(cy + h/2))
    out = im.crop(box).resize((600, 200), Image.LANCZOS).convert("RGB")
    data, q = jpeg_under(out, 100)
    p = out_path(a.file, ".jpg"); open(p, "wb").write(data)
    print(f"{p}  600x200  {len(data)//1024} KB")

def cmd_doc(a):
    im = load(a.file, a.rotate)
    if a.box: im = im.crop(frac_box(im, *a.box))
    im.thumbnail((2000, 2000), Image.LANCZOS)
    q = 88
    while True:
        j = io.BytesIO(); im.save(j, "JPEG", quality=q, optimize=True)
        pdf = io.BytesIO(); Image.open(j).save(pdf, "PDF", resolution=200)
        if pdf.tell() < 900 * 1024 or q < 40: break
        q -= 6
    p = out_path(a.file, ".pdf"); open(p, "wb").write(pdf.getvalue())
    print(f"{p}  {im.size[0]}x{im.size[1]}  {pdf.tell()//1024} KB (limit 1000 KB)")

def cmd_preview(a):
    files = sorted(f for f in os.listdir(a.folder) if f.lower().endswith((".jpg", ".jpeg", ".png")))
    T = 360; sheet = Image.new("RGB", (T * min(len(files), 5), (T + 20) * ((len(files) + 4) // 5)), "white")
    d = ImageDraw.Draw(sheet)
    for i, f in enumerate(files):
        im = load(os.path.join(a.folder, f)); im.thumbnail((T - 6, T - 6))
        x, y = (i % 5) * T, (i // 5) * (T + 20)
        sheet.paste(im, (x + 3, y + 20)); d.text((x + 3, y + 3), f, fill="black")
    p = os.path.join(a.folder, "_preview.jpg"); sheet.save(p); print(p)


# ---------------------------------------------------------------- AUTO MODE
# For non-developers: put files in a folder (one subfolder per person) and run
#   python oci_prep.py auto MyFiles
# File type is guessed from the file name:
#   photo / selfie / face  -> passport-style photo (JPEG)
#   sign                   -> signature (JPEG, 3:1)
#   anything else          -> document (PDF)
def _faces(im):
    import numpy as np, cv2
    casc = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    g = np.array(im.convert("L")); s = 800 / max(g.shape)
    small = cv2.resize(g, None, fx=s, fy=s)
    f = casc.detectMultiScale(small, 1.1, 6, minSize=(60, 60))
    return [(x / s, y / s, w / s, h / s) for x, y, w, h in f]

def auto_photo(path):
    base = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    for r in (0, 90, 270, 180):                     # fix sideways phone photos
        im = base.rotate(r, expand=True) if r else base
        f = _faces(im)
        if f: break
    if not f:
        return f"!! No face found in {os.path.basename(path)}. Retake: face the camera, plain light wall, good light."
    x, y, w, h = max(f, key=lambda b: b[2] * b[3])
    W, H = im.size
    crown, chin, cx = y - 0.45 * h, y + 1.05 * h, x + w / 2
    head = chin - crown
    side = int(min(head / 0.64, W, H))
    left = int(min(max(cx - side / 2, 0), W - side))
    top = int(min(max(crown - 0.10 * side, 0), H - side))
    sq = im.crop((left, top, left + side, top + side)).resize((600, 600), Image.LANCZOS)
    data, _ = jpeg_under(sq, 195)
    p = out_path(path, ".jpg"); open(p, "wb").write(data)
    pct = 100 * head / side
    note = "" if 50 <= pct <= 69 else "  <-- CHECK: head size outside 50-69%; stand a bit closer/farther and retake"
    return f"OK photo     {os.path.basename(p)}  {len(data)//1024} KB  head {pct:.0f}% of frame{note}"

def auto_sign(path):
    import numpy as np, cv2
    g = np.array(ImageOps.exif_transpose(Image.open(path)).convert("L")).astype(float)
    H, W = g.shape
    bg = cv2.GaussianBlur(g, (0, 0), 40)
    ink = ((bg - g) > 40).astype("uint8")
    ink = cv2.morphologyEx(ink, cv2.MORPH_OPEN, np.ones((3, 3), "uint8"))
    n, lab, st, _ = cv2.connectedComponentsWithStats(ink)
    m = max(4, int(0.01 * min(W, H)))
    keep = [i for i in range(1, n) if st[i, 4] > 0.00002 * W * H
            and st[i, 0] > m and st[i, 1] > m
            and st[i, 0] + st[i, 2] < W - m and st[i, 1] + st[i, 3] < H - m   # ignore paper edges
            and st[i, 2] < 0.9 * W and st[i, 3] < 0.5 * H]
    if not keep:
        return f"!! No signature ink found in {os.path.basename(path)}. Use black pen on white paper, fill the frame."
    x0 = min(st[i, 0] for i in keep); y0 = min(st[i, 1] for i in keep)
    x1 = max(st[i, 0] + st[i, 2] for i in keep); y1 = max(st[i, 1] + st[i, 3] for i in keep)
    pad = 0.08 * (x1 - x0)
    a = argparse.Namespace(file=path, rotate=0,
        box=[max(x0 - pad, 0) / W, max(y0 - pad, 0) / H, min(x1 + pad, W) / W, min(y1 + pad, H) / H])
    import contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf): cmd_sign(a)
    p = out_path(path, ".jpg")
    return f"OK signature {os.path.basename(p)}  {os.path.getsize(p)//1024} KB"

def auto_doc(path):
    a = argparse.Namespace(file=path, rotate=0, box=None)
    import contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf): cmd_doc(a)
    p = out_path(path, ".pdf")
    return f"OK document  {os.path.basename(p)}  {os.path.getsize(p)//1024} KB (PDF)"

def check_sheet(folder):
    d = os.path.join(folder, "OCI_Ready")
    if not os.path.isdir(d): return
    ims = []
    for f in sorted(os.listdir(d)):
        p = os.path.join(d, f)
        if f.endswith("_OCIready.jpg"): ims.append((f, Image.open(p).convert("RGB")))
        elif f.endswith("_OCIready.pdf"):
            src = [s for s in os.listdir(folder) if os.path.splitext(s)[0] + "_OCIready.pdf" == f]
            if src: ims.append((f, ImageOps.exif_transpose(Image.open(os.path.join(folder, src[0]))).convert("RGB")))
    if not ims: return
    T = 300; sheet = Image.new("RGB", (T * len(ims), T + 24), "white"); dr = ImageDraw.Draw(sheet)
    for i, (f, im) in enumerate(ims):
        im.thumbnail((T - 8, T - 8)); sheet.paste(im, (i * T + 4, 22)); dr.text((i * T + 4, 4), f, fill="black")
    sp = os.path.join(d, "_CHECK_ME.jpg"); sheet.save(sp)
    print(f"   Look at {sp} : everything upright? face centered? passport readable?")

def cmd_auto(a):
    root = os.path.abspath(a.folder)
    exts = (".jpg", ".jpeg", ".png")
    people = [root] + [os.path.join(root, d) for d in sorted(os.listdir(root))
                       if os.path.isdir(os.path.join(root, d)) and d != "OCI_Ready"]
    done = 0
    for folder in people:
        files = [f for f in sorted(os.listdir(folder)) if f.lower().endswith(exts) and not f.startswith("_")]
        if not files: continue
        print(f"\n== {os.path.basename(folder)} ==")
        for f in files:
            p = os.path.join(folder, f); n = f.lower()
            try:
                if any(k in n for k in ("photo", "selfie", "face", "pic")): msg = auto_photo(p)
                elif "sign" in n: msg = auto_sign(p)
                else: msg = auto_doc(p)
            except Exception as e:
                msg = f"!! Could not process {f}: {e}"
            print("  " + msg); done += 1
        check_sheet(folder)
    if not done:
        print("No photos found. Put your .jpg files in the MyFiles folder (one subfolder per person).")
    print("\nNext: upload photo + signature (JPG) and the passport PDF from each OCI_Ready folder.")
    print("Documents came out sideways? Rotate the ORIGINAL in Windows Photos (Ctrl+R), save, run again.")

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
sp = ap.add_subparsers(dest="cmd", required=True)
for name in ("photo", "sign", "doc"):
    s = sp.add_parser(name); s.add_argument("file"); s.add_argument("--rotate", type=int, default=0)
    if name == "photo":
        s.add_argument("--crown", type=float, required=True, help="top of hair, fraction of height")
        s.add_argument("--chin", type=float, required=True, help="bottom of chin, fraction of height")
        s.add_argument("--cx", type=float, default=0.5, help="face centre, fraction of width")
        s.add_argument("--head-ratio", type=float, default=0.64)
        s.add_argument("--top-margin", type=float, default=0.10)
    if name == "sign": s.add_argument("--box", type=float, nargs=4, required=True)
    if name == "doc": s.add_argument("--box", type=float, nargs=4)
pv = sp.add_parser("preview"); pv.add_argument("folder")
au = sp.add_parser("auto", help="one-click: process every photo in a folder"); au.add_argument("folder")
a = ap.parse_args()
{"photo": cmd_photo, "sign": cmd_sign, "doc": cmd_doc, "preview": cmd_preview, "auto": cmd_auto}[a.cmd](a)
