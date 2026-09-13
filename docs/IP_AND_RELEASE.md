# Provenance, IP, privacy, and release workflow

This is operational guidance, not legal advice. The goal is to make authorship,
capture history, editing, and published versions easy to demonstrate.

## What establishes the chain

For every keeper retain:

1. untouched FITS subframes;
2. SHA-256 manifest created at ingest;
3. session note with capture choices and interruptions;
4. quality report and approved-frame list;
5. linear integrated FITS;
6. recipes or command log;
7. layered PSD with meaningful layer names;
8. dated release exports and release manifest;
9. two independent backups, one physically or logically off-site.

The U.S. Copyright Office states that the author and initial owner is generally
the person who takes the photograph. Its group options allow up to 750 eligible
published or unpublished photographs per application, with strict same-author,
same-claimant, title-list, and publication-status requirements. See the
[Copyright Office photographer overview](https://copyright.gov/engage/photographers/)
and [GRUPH requirements](https://www.copyright.gov/eco/help/group/gruph.html).

## Before public posting

- Decide whether the work belongs in an unpublished registration batch before
  release. Publication is a legal classification; ask an IP attorney if the
  commercial release plan makes the answer consequential.
- Use a public location label such as `North Atlanta backyard`, not a street
  address or precise coordinates.
- Remove GPS and device-network identifiers from web exports.
- Put copyright, creator/brand, contact URL, target, capture date, equipment,
  integration, and a short processing disclosure in IPTC/XMP metadata.
- Keep the high-resolution unwatermarked print master private.
- Export a restrained watermarked proof for untrusted channels. A watermark is
  deterrence and branding, not proof by itself.
- Record each publication URL, date/time, filename, size, and SHA-256 in the
  release manifest.

Configure `creator`, `copyright_notice`, and `public_contact` once in the ignored
local `config.toml`. Ingest copies those public fields into private session
manifests. Record an exact export before or immediately after publication:

```powershell
python -m seestarflow release `
  --file "D:/Astro/M27/releases/M27-portfolio-v01.jpg" `
  --target M27 `
  --variant portfolio `
  --destination "https://example.com/gallery/m27"
```

The default ledger is `library/release-manifest.jsonl`. It records the precise
file hash; re-exporting later produces a different fingerprint and should be a
new release record.

## Photoshop Content Credentials

Adobe's current instructions say to open **Window > Content Credentials
(Beta)**, enable Content Credentials, and optionally enable them for new and
saved documents so edit history is captured from the beginning. See
[Adobe's Content Credentials instructions](https://helpx.adobe.com/photoshop/desktop/save-and-export/metadata-content-credentials/use-content-credentials.html).

Use credentials as an additional transparency layer, not as the only archive.
Metadata can be stripped by social platforms; the private manifest and original
files remain the source of truth.

Suggested processing disclosure:

> Captured by the artist with a Seestar S50 Pro. Registered and integrated in
> Siril; gradient corrected in GraXpert; astronomy-specific deconvolution,
> denoising, and optional star separation with RC Astro; tone and color finished
> in Siril and Adobe Photoshop. No generative content or replacement sky.

## Release variants

| Variant | Purpose | Suggested format |
| --- | --- | --- |
| Archive master | Long-term editable source | Layered PSD, 16-bit, embedded working profile |
| Print master | Lab/printer handoff | 16-bit TIFF, output-sized, lab-requested profile, no watermark |
| Portfolio | High-quality online display | JPEG, sRGB, long edge 3000–4000 px, modest watermark if desired |
| Social proof | Discovery and sharing | JPEG, sRGB, platform-sized, visible but tasteful watermark |
| Registration deposit | Copyright submission | Exact format/naming required by the current Copyright Office instructions |

Do not overwrite a release. Increment `v01`, `v02`, and so on, and record which
one is authoritative.
