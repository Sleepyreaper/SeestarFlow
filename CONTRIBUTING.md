# Contributing

Issues and pull requests are welcome for new FITS layouts, safer quality metrics,
portable Siril recipes, documentation, and reproducible benchmarks.

Please:

- never commit raw astronomy data, generated images, account information, license
  files, activation codes, or machine-specific absolute paths;
- use synthetic FITS fixtures in automated tests;
- describe the telescope, camera, filter, exposure, and software versions when
  reporting an image-processing problem;
- include before/after measurements for changes to quality thresholds;
- run `python -m pytest` before submitting.

By contributing, you agree that your contribution is licensed under the MIT
License.
