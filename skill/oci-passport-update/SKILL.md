---
name: oci-passport-update
description: Guide an OCI (Overseas Citizen of India) cardholder through linking a new foreign passport on ociservices.gov.in, and prepare their photo, signature and passport scans to the portal's specs.
---

# OCI passport update

Use when someone has a new (e.g. US) passport and must update their OCI record, or asks to prepare OCI photos, signatures or document scans. Covers one person or a family (one portal account per person).

## 1. Confirm the situation (ask only what you can't see)
- Whose OCI, and how many people? One folder per person (e.g. `D:\OCI\<Name>\`).
- How they got OCI: **Indian origin** (OCI card says place of birth INDIA) vs **foreign spouse** (Section 7A(1)(d)). Only spouse-category holders need the Declaration and spouse passport/OCI copies. Marital status alone does not matter.
- New passport issue date: within 3 months it's free; later there's a US $25 late fee. Check the portal banner for any waiver (one ran through 31 Dec 2026).
- If the user says a drive is full, write nothing there. Ask where outputs should go.

## 2. Prepare files (Claude does this)
Look at every image first: build a contact sheet and view it. Phone EXIF orientation is unreliable; passports and OCI booklets shot landscape usually need a 90° rotation. Verify visually after rotating.

| Output | Spec | How |
|---|---|---|
| `<name>Photo_OCIready.jpg` | JPEG, square 600×600, under 200 KB (portal max 500 KB), head crown-to-chin about 64% of frame, about 10% space above the hair, face centered | Grid-overlay the photo, read crown/chin/center as fractions, crop square |
| `<name>Signature_OCIready.jpg` | JPEG 600×200 (3:1), white paper, dark ink | Divide by a heavily blurred background to flatten lighting, stretch contrast, crop the ink box padded to 3:1. Exclude the paper edge and shadows |
| `<name>NewPassport_OCIready.pdf` | **PDF**, under 1000 KB (aim under 900), about 2000 px long side | Rotate upright, crop the open spread (photo page fully visible, MRZ readable), JPEG q≈88 → PDF |

`scripts/oci_prep.py` (in the kit) implements all three, plus `preview`. If face detection isn't available, place the crop by eye using a grid.

Rules:
- Never modify originals; write to an `OCI_Ready` subfolder with an `_OCIready` suffix.
- **After writing, pull the output back and look at it.** Saves can silently fail; a stale file caused a wrong upload once.
- Flag photo problems: open mouth, glasses glare, head above 69% or below 50% of frame, dark background, or a photo taken more than 30 days ago. Ask for a retake rather than hiding them.

## 3. Portal walkthrough (ociservices.gov.in only; warn about look-alike paid sites)
1. **User Register**: name and DOB exactly as on the **new** passport. Separate email per person (the e-OCI goes to the email linked to the OCI). The user types email, mobile, CAPTCHA, OTP and password.
2. **User Profile**: **new** passport number, issue and expiry dates.
3. Navigate with the site's menus. **Do not type URLs directly** (it ends the session): Online Registration ▸ OCI Miscellaneous Services ▸ Apply Online.
4. Lookup: **old** passport number (the one linked to the OCI), OCI number, DOB. "Record Not Found" means a mismatch; check against the OCI card.
5. Select **Passport Particulars Updation** (Gratis), then Save and Continue.
6. Photo/Sign Upload → the two JPEGs from `OCI_Ready` (not the originals, which are over 500 KB).
7. Document Upload → **Copy of New passport** (PDF) only, for Indian-origin applicants. Set the dropdown back to "Select Document" and Submit to move on.
8. Verify Information: read every field back to the user. The user clicks Final Submission.
9. Save the application ID (a passport update ends in `U<yy>`, e.g. `U26`).

Limits: 5 re-uploads and 5 views per document. The user types all ID numbers, passwords, OTPs and the CAPTCHA, and clicks the final submit.

## 4. After submission
Offer reminders to check **Track your Application** in about 2–3 weeks and to download the e-OCI. If stuck, email the issuing consulate with the application ID.

See `LEARNINGS.md` in the kit for sources and the full list of pitfalls.
