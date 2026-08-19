# SUPIR v100 for Pinokio

An independent Pinokio launcher for the SUPIR v100 Gradio application.

This repository contains launcher code only. SUPIR source code and model files
are downloaded directly from their upstream repositories during installation.

## Install

1. Open Pinokio.
2. Choose the option to download an app from a URL.
3. Enter `https://github.com/JasonSongPeng/supir-pinokio`.
4. Run **Install Dependencies**.
5. Run **Download Required Models**. The selected model set is approximately
   48.31 GiB; keep at least 65 GiB free for models and temporary data.
6. Start with **Balanced (FP16/BF16)** or **Low VRAM (FP8)**.

Downloads are resumable. Re-running the model download verifies existing files
and retrieves only missing content.

## Compatibility

- Windows 10/11 with an NVIDIA GPU: supported and based on the verified local
  environment.
- Linux with an NVIDIA GPU: included, but not yet hardware-verified by the
  launcher author.
- macOS, AMD GPUs, and CPU-only systems: not supported by this launcher because
  this SUPIR build depends on CUDA-specific packages.

The verified Windows dependency set is Python 3.10, PyTorch 2.5.1 with CUDA
12.4, xformers 0.0.28.post3, Triton 3.1, Gradio 4.19.0, and Transformers
4.38.2. A recent NVIDIA driver is required. At least 12 GiB VRAM is recommended;
the FP8 mode is intended for lower-VRAM cards.

## Security and privacy

- No API key, token, cookie, or account is required.
- The Web UI listens on `127.0.0.1` only.
- Gradio sharing is not enabled.
- Hugging Face and Gradio telemetry are disabled by the launcher.
- Source and model revisions are pinned for reproducibility.
- Local environment files, models, outputs, logs, and common private-key file
  types are excluded from Git.

Do not put credentials in launcher files. If a future private download requires
authentication, keep the credential in Pinokio's local environment settings,
never in this repository.

## Version policy

The launcher intentionally installs SUPIR commit
`63b53ddb1773062ef64a4c192707f69d66b24953`, matching v100. Updating this
launcher does not silently move SUPIR to a newer upstream revision.

## Licensing

Launcher files in this repository use the MIT License. SUPIR and all downloaded
models and dependencies retain their own licenses and terms. See
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) before use or redistribution.
