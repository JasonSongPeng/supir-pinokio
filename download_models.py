from __future__ import annotations

import shutil
from pathlib import Path

from huggingface_hub import snapshot_download


MODEL_REPOSITORY = "MonsterMMORPG/SECourses_SUPIR"
MODEL_REVISION = "403ab632a2dea328b1b93d8d16f70930de22708b"
MINIMUM_FREE_GIB = 55
ALLOW_PATTERNS = [
    "v0F.ckpt",
    "v0Q.ckpt",
    "open_clip_pytorch_model.bin",
    "detection_Resnet50_Final.pth",
    "llava-v1.5-7b/*",
    "clip-vit-large-patch14-336/*",
    "clip-vit-large-patch14/*",
    "checkpoints/Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors",
]


def main() -> None:
    launcher_root = Path(__file__).resolve().parent
    target = launcher_root / "app" / "models"
    target.mkdir(parents=True, exist_ok=True)

    free_gib = shutil.disk_usage(target).free / (1024**3)
    if free_gib < MINIMUM_FREE_GIB:
        raise SystemExit(
            f"Not enough free disk space: {free_gib:.1f} GiB available; "
            f"at least {MINIMUM_FREE_GIB} GiB is required."
        )

    print(f"Downloading required model set to {target}")
    print(f"Pinned model revision: {MODEL_REVISION}")
    snapshot_download(
        repo_id=MODEL_REPOSITORY,
        revision=MODEL_REVISION,
        local_dir=target,
        allow_patterns=ALLOW_PATTERNS,
        max_workers=4,
        token=False,
    )
    print("Required models are ready.")


if __name__ == "__main__":
    main()
