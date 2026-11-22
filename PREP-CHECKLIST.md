# OCI Passport Update: Prep Checklist (per person)

Make one folder per person, e.g. `D:\OCI\Mom\`. Take phone photos straight on, in daylight, no flash glare.

## Collect before you start
- [ ] OCI number (top right of the OCI booklet's photo page, starts with "A")
- [ ] **Old** passport number (the one the OCI was issued against)
- [ ] **New** passport: number, issue date, expiry date
- [ ] Date of birth exactly as on the OCI (DD/MM/YYYY)
- [ ] A working email **for this person only** (the e-OCI goes here) + a phone for the OTP
- [ ] Which consulate issued the OCI (the update goes to that one)

## Photos to take (save into the person's folder)
| File name | What to photograph | Tips |
|---|---|---|
| `Photo.jpg` | The person, head and shoulders | Plain light wall, about 4 ft away, camera at eye level, **mouth closed**, no glasses glare, taken in the last 30 days |
| `Signature.jpg` | Signature in black pen on white paper | Fill the frame, no shadows, paper flat |
| `NewPassport.jpg` | New passport, opened to the photo page | Whole spread visible, no glare on the photo or MRZ lines |
| `OldPassport.jpg` | Old passport photo page | Optional; keep for your records |
| `OCICard.jpg` | OCI booklet photo/particulars page | Optional; keep for your records |

## Then ask Claude
> "Prepare the OCI files in D:\OCI\Mom"

Claude will check orientation, crop, resize, and compress everything into `D:\OCI\Mom\OCI_Ready\`:
- `Photo_OCIready.jpg`: square, under 200 KB
- `Signature_OCIready.jpg`: 3:1
- `NewPassport_OCIready.pdf`: **PDF**, under 1 MB

## On the portal you'll type yourself
Passport and OCI numbers, the CAPTCHA, your password, the OTP, and the final Submit click.
