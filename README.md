# OCI Passport Update Helper 🇮🇳

**Got a new US (or other foreign) passport? Your OCI must be linked to it.**
This free kit gets your photo, signature and passport scan into the exact formats the Indian government portal (https://ociservices.gov.in) accepts, then walks you through the screens.

It was built from a real family run-through in Nov 2026: three applications (me and my two senior parents) done in one morning with Claude, including every mistake we made along the way, so you don't repeat them.

> ⏰ **Deadline worth knowing:** the US $25 late fee is **waived until 31 Dec 2026**. If your new passport is more than 3 months old, update before then.

---

## Choose your way

### 🟢 Option 1: Double-click (no coding)
1. Click the green **Code** button above → **Download ZIP** → unzip it anywhere.
2. Open the `MyFiles` folder and make one folder per person (e.g. `Mom`, `Dad`, `Me`).
3. Put three phone photos in each person's folder, named:
   - `Photo.jpg` (face, plain light wall, mouth closed, taken in the last 30 days)
   - `Signature.jpg` (black pen on white paper)
   - `NewPassport.jpg` (new passport opened to the photo page)
4. Double-click **`RUN-ME.bat`** (Windows) or **`run-me-mac.command`** (Mac; the first time, right-click → Open).
   - If Python isn't installed, the script opens the download page for you. Tick **"Add python.exe to PATH"** when installing.
5. Open each person's `OCI_Ready` folder and look at `_CHECK_ME.jpg`. Then upload:
   - `Photo_OCIready.jpg` and `Signature_OCIready.jpg` at **Photo/Sign Upload**
   - `NewPassport_OCIready.pdf` at **Document Upload → Copy of New passport**

🔒 Everything runs on your own computer. Nothing is uploaded anywhere.

### 🤖 Option 2: With Claude (easiest if you have it)
Add the skill in `skill/oci-passport-update/SKILL.md` to Claude, then say:
> *"Prepare the OCI files in my Mom folder and walk me through the portal."*

Claude checks the photos, fixes sideways scans, crops and compresses everything, and guides you screen by screen. You type the passport numbers, the CAPTCHA and the final Submit yourself.

### ⌨️ Option 3: Command line
```bash
pip install -r requirements.txt
python scripts/oci_prep.py auto MyFiles            # one-click mode
python scripts/oci_prep.py photo Mom/Photo.jpg --crown 0.31 --chin 0.565 --cx 0.48   # manual fine-tuning
python scripts/oci_prep.py doc   Mom/NewPassport.jpg --rotate 90 --box 0 0.1 0.96 0.86
```

---

## The 5 things that trip everyone up
1. **Documents must be PDF** (under 1 MB). Only the photo and signature are JPG.
2. **New vs old passport:** your *profile* takes the **new** passport; the *Miscellaneous Services lookup* takes the **old** one, the one your OCI is linked to.
3. **Ignore "Declaration" and the spouse documents** unless your OCI was granted *through marriage*. If your OCI card says place of birth INDIA, you only upload **Copy of New passport**.
4. **One email per person.** Your parents need separate portal accounts, and the e-OCI goes to that email.
5. **Use only ociservices.gov.in.** Look-alike sites charge for what is free.

Full walkthrough and sources: [`LEARNINGS.md`](LEARNINGS.md) · Before you start: [`PREP-CHECKLIST.md`](PREP-CHECKLIST.md)

## What's inside
| File | Purpose |
|---|---|
| `RUN-ME.bat` / `run-me-mac.command` | Double-click launchers |
| `MyFiles/` | Where you drop your photos (never uploaded to GitHub) |
| `scripts/oci_prep.py` | The image tool: auto-rotate, face-centered crop, signature cleanup, PDF conversion |
| `skill/oci-passport-update/SKILL.md` | Claude skill |
| `LEARNINGS.md`, `PREP-CHECKLIST.md` | Guides |

## Contributing
Did the portal change? Did your consulate ask for something different? Please [open an issue](../../issues). Real-world reports keep this useful.

*Not legal advice, and not affiliated with the Government of India. Rules change; confirm with the portal and your consulate.*
