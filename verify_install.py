from __future__ import annotations

from pathlib import Path

import gradio
import torch
import transformers


REQUIRED_FILES = [
    "app/models/v0F.ckpt",
    "app/models/v0Q.ckpt",
    "app/models/open_clip_pytorch_model.bin",
    "app/models/detection_Resnet50_Final.pth",
    "app/models/llava-v1.5-7b/config.json",
    "app/models/clip-vit-large-patch14/config.json",
    "app/models/clip-vit-large-patch14-336/config.json",
    "app/models/checkpoints/Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors",
]


def main() -> None:
    root = Path(__file__).resolve().parent
    missing = [path for path in REQUIRED_FILES if not (root / path).is_file()]
    if missing:
        joined = "\n".join(f"- {path}" for path in missing)
        raise SystemExit(f"Missing required model files:\n{joined}")

    if not torch.cuda.is_available():
        raise SystemExit("PyTorch cannot access an NVIDIA CUDA GPU.")

    print(f"PyTorch: {torch.__version__}")
    print(f"CUDA runtime: {torch.version.cuda}")
    print(f"GPU: {torch.cuda.get_device_name(0)}")
    print(f"Gradio: {gradio.__version__}")
    print(f"Transformers: {transformers.__version__}")
    print("SUPIR installation verification passed.")


if __name__ == "__main__":
    main()
