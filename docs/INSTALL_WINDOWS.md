# Windows installation

## 1. Install the free stack

Install:

1. Python 3.11 or newer.
2. Siril 1.4 or newer, including `siril-cli.exe`.
3. GraXpert, plus its background-extraction and denoising models.
4. Git.

Clone and create an isolated Python environment:

```powershell
git clone https://github.com/Sleepyreaper/SeestarFlow.git
cd SeestarFlow
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
Copy-Item config.example.toml config.toml
```

Edit `config.toml`. Forward slashes in Windows TOML paths avoid escaping issues:

```toml
[paths]
library = "D:/Astrophotography/SeestarLibrary"

[tools]
siril = "C:/Program Files/Siril/bin/siril-cli.exe"
graxpert = "C:/Program Files/GraXpert/GraXpert.exe"
rc_astro = ""
pixinsight = ""
```

Verify discovery:

```powershell
python -m seestarflow doctor
python -m pytest
```

## 2. Add the optional paid stack

Install PixInsight normally and activate its license. Then install the RC Astro
modules through their supported PixInsight or standalone installation path.
Configure `rc_astro` and `pixinsight` in `config.toml`, and run:

```powershell
python -m seestarflow doctor
rc-astro license
```

The standalone premium command expects RC Astro's CLI. PixInsight is currently
used as the interactive or scripted finishing environment; SeestarFlow records
the common linear handoff so PixInsight work can be reproduced separately.

## 3. Storage planning

Individual FITS data can consume tens of gigabytes per night. Put `library` on a
drive with substantial free space. Ingest deliberately copies raw data to make
the archive independent of the camera or transfer folder. Products add another
temporary multiple during registration and integration.

Do not erase the telescope until:

- ingest completed;
- file counts match expectations;
- hashes were written to `manifest.json`;
- several archived FITS files open successfully;
- a second backup exists for irreplaceable sessions.

## Troubleshooting

- If `doctor` returns `null` for a tool, correct its absolute path or add it to
  `PATH`.
- If PowerShell blocks environment activation, use the venv's Python executable
  directly instead of weakening system-wide execution policy.
- If GraXpert returns immediately without output, open it once, install the
  required models, then verify the CLI syntax supported by that release.
- If RC Astro asks to verify a license, allow its supported application to reach
  the licensing service; never commit account or activation data.
- Use `--dry-run` to distinguish a SeestarFlow path problem from an external-tool
  problem.
