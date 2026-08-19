# Third-party notices

This repository contains only an independent Pinokio launcher. It does not
redistribute SUPIR source code, model weights, generated images, or a Python
environment.

During installation, the launcher downloads third-party components directly
from their publishers:

- SUPIR v100 source from `FurkanGozukara/SUPIR`, pinned to commit
  `63b53ddb1773062ef64a4c192707f69d66b24953`.
- Runtime model files from `MonsterMMORPG/SECourses_SUPIR`, pinned to revision
  `403ab632a2dea328b1b93d8d16f70930de22708b`.
- Python packages from PyPI and the official PyTorch wheel index.
- Triton for Windows from the `woct0rdho/triton-windows` GitHub release.

The MIT license in this repository applies only to the launcher files written
for this repository. SUPIR's repository states that its Gradio application is
rights-reserved. Model files and other dependencies remain under their own
terms. Users are responsible for reviewing and complying with those terms.
