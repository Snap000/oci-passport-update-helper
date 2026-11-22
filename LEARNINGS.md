# OCI Passport Update: What We Learned (Nov 2026)

Field notes from updating three OCI records (one adult + two seniors, all US citizens of Indian origin, New York consulate) on https://ociservices.gov.in. Rules change, so check the portal before relying on this.

## The rule
- **Every new foreign passport must be linked to your OCI.** In 2026 this applies at every age; the old 20/50 age rules are gone, and physical OCI re-issue is discontinued.
- It's free if done **within 3 months** of the new passport's issue date. After that it's US $25 late fee (about $47 through VFS in the US).
- **The late fee is waived through 31 Dec 2026** (portal banner). If your passport is older than 3 months, file before then.
- No new card is issued. The record is updated and you can download a free **e-OCI**.

## Portal flow (what you actually click)
1. **User Register** (one account per person, one email per person). Name and DOB must match the **current (new)** passport.
2. Verify the email OTP, then set a password (8+ characters, upper, lower, number, special).
3. **User Profile**: enter the **NEW** passport (number, issue and expiry dates, issue place). The expiry picker only allows dates at least 6 months away, so an expired old passport will not work here.
4. Dashboard → **Online Registration ▸ OCI Miscellaneous Services ▸ Apply Online**.
5. Lookup screen: **OLD passport number** (the one the OCI is currently linked to) + **OCI number** + DOB.
6. Choose **Passport Particulars Updation** (Gratis). *Not* Personal Particulars, and never Surrender.
7. Registration form (new passport details) → **Photo/Sign Upload** → **Document Upload** → **Verify Information** → **Final Submission**.
8. Save the acknowledgment. The application ID for a passport update **ends in `U26`** (for 2026).

## File specs (what the portal accepts)
| Item | Format | Size | Shape |
|---|---|---|---|
| Photo | JPEG | under 500 KB (aim under 200) | square, 200–900 px, head 50–69% of frame, light background, taken under 30 days ago, neutral face, mouth closed |
| Signature | JPEG | small | 3:1 (e.g. 600×200), dark ink on white |
| Documents | **PDF only** | **under 1000 KB** | portrait, readable MRZ |

Only **one document** is needed for an Indian-origin applicant: **Copy of New passport**.

## Mistakes we made (so you don't)
1. **Documents uploaded as JPG.** The portal requires **PDF**. Only the photo and signature are JPEG.
2. **"Do I need my spouse's passport and OCI?" No,** unless your OCI was granted *through marriage* (Section 7A(1)(d), a foreign-origin spouse). The dropdown shows spouse documents and a "Declaration" to everyone; ignore them if your OCI card says place of birth INDIA or you qualified by origin. Being married, or separated, doesn't change this.
3. **Old vs new passport:** the profile takes the **new** passport; the Miscellaneous lookup takes the **old** one. Mixing them up gives "Record Not Found" or blocked dates.
4. **Typing a URL directly logged the user out.** Navigate with the site's menus only.
5. **Picked the original 1.5 MB photo instead of the processed one.** Keep processed files in a separate `OCI_Ready` folder with a clear suffix.
6. **A re-done photo didn't save the first time.** Always re-open the output file and look at it after saving.
7. **Phone photos are often sideways** even when they look right in a gallery (EXIF orientation). Normalize orientation, then check visually; passports and OCI booklets photographed landscape usually need a 90° turn.
8. **Upload limits:** 5 re-uploads and 5 views per document. Don't burn them.
9. **Separate email for each parent.** The e-OCI is delivered only to the email linked to that OCI. If the original 2010-era email still works, prefer it.

## Timeline
Decision is officially ~15 days after acknowledgment; real-world US timelines are often several weeks. Track it via **Track your Application**. If it's stuck, email the consulate with the application ID.

## Sources
- OCI portal and Misc FAQs: https://ociservices.gov.in/onlineOCI/miscFAQs
- CGI Chicago update page: https://www.cgichicago.gov.in/page/oci-card-updation-reissuance-of-oci-cards-discontinued/
- Rupeeflo guide (US, 2026): https://www.rupeeflo.com/resources/how-to-link-oci-with-new-us-passport-(2026)
- Immihelp 2026 rule changes: https://www.immihelp.com/india-oci-rule-changes-2026/

*Not legal advice. Confirm anything unusual with your consulate.*
