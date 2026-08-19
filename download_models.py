from __future__ import annotations

import shutil
from dataclasses import dataclass
from fnmatch import fnmatchcase
from pathlib import Path

from huggingface_hub import HfApi, snapshot_download
from huggingface_hub._local_folder import get_local_download_paths


MODEL_REPOSITORY = "MonsterMMORPG/SECourses_SUPIR"
MODEL_REVISION = "403ab632a2dea328b1b93d8d16f70930de22708b"
MAX_WORKERS = 4
GIB = 1024**3
SAFETY_MARGIN_BYTES = 2 * GIB
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


@dataclass(frozen=True)
class ModelFile:
    path: str
    size: int
    etag: str


@dataclass(frozen=True)
class DownloadPlan:
    total_bytes: int
    remaining_bytes: int
    partial_bytes: int
    required_free_bytes: int
    completed_files: int
    pending_files: int


def is_required_path(path: str) -> bool:
    return any(fnmatchcase(path, pattern) for pattern in ALLOW_PATTERNS)


def get_required_files() -> list[ModelFile]:
    info = HfApi().model_info(
        repo_id=MODEL_REPOSITORY,
        revision=MODEL_REVISION,
        files_metadata=True,
        token=False,
    )
    files = []
    for sibling in info.siblings:
        if not is_required_path(sibling.rfilename):
            continue
        if sibling.size is None:
            raise SystemExit(f"Missing size metadata for {sibling.rfilename}.")
        etag = sibling.lfs.sha256 if sibling.lfs else sibling.blob_id
        if not etag:
            raise SystemExit(f"Missing checksum metadata for {sibling.rfilename}.")
        files.append(ModelFile(sibling.rfilename, int(sibling.size), etag))

    if not files:
        raise SystemExit("The pinned model revision contains no required files.")
    return files


def build_download_plan(target: Path, files: list[ModelFile]) -> DownloadPlan:
    total_bytes = sum(file.size for file in files)
    remaining_bytes = 0
    partial_bytes = 0
    largest_pending_file = 0
    completed_files = 0

    for file in files:
        destination = target.joinpath(*file.path.split("/"))
        if destination.exists():
            if not destination.is_file() or destination.stat().st_size != file.size:
                raise SystemExit(
                    f"Downloaded file has an unexpected size: {destination}. "
                    "Move or delete it, then retry the model download."
                )
            completed_files += 1
            continue

        paths = get_local_download_paths(target, file.path)
        incomplete = paths.incomplete_path(file.etag)
        partial_size = incomplete.stat().st_size if incomplete.is_file() else 0
        if partial_size > file.size:
            raise SystemExit(
                f"Partial download is larger than expected: {incomplete}. "
                "Move or delete it, then retry the model download."
            )

        partial_bytes += partial_size
        remaining_bytes += file.size - partial_size
        largest_pending_file = max(largest_pending_file, file.size)

    pending_files = len(files) - completed_files
    required_free_bytes = 0
    if pending_files:
        # huggingface_hub 0.36 checks free space against the complete size of
        # each pending file, even when an .incomplete file can be resumed.
        required_free_bytes = (
            max(remaining_bytes, largest_pending_file) + SAFETY_MARGIN_BYTES
        )

    return DownloadPlan(
        total_bytes=total_bytes,
        remaining_bytes=remaining_bytes,
        partial_bytes=partial_bytes,
        required_free_bytes=required_free_bytes,
        completed_files=completed_files,
        pending_files=pending_files,
    )


def ensure_disk_space(
    target: Path, plan: DownloadPlan, free_bytes: int | None = None
) -> None:
    available = shutil.disk_usage(target).free if free_bytes is None else free_bytes
    if available < plan.required_free_bytes:
        raise SystemExit(
            f"Not enough free disk space: {available / GIB:.1f} GiB available; "
            f"{plan.required_free_bytes / GIB:.1f} GiB currently required. "
            "Completed files and resumable partial data were included in this estimate."
        )


def main() -> None:
    launcher_root = Path(__file__).resolve().parent
    target = launcher_root / "app" / "models"
    target.mkdir(parents=True, exist_ok=True)

    files = get_required_files()
    plan = build_download_plan(target, files)
    ensure_disk_space(target, plan)

    print(f"Downloading required model set to {target}")
    print(f"Pinned model revision: {MODEL_REVISION}")
    print(
        f"Progress: {plan.completed_files}/{len(files)} files complete; "
        f"{plan.partial_bytes / GIB:.2f} GiB preserved in resumable partial files; "
        f"{plan.remaining_bytes / GIB:.2f} GiB remaining."
    )
    snapshot_download(
        repo_id=MODEL_REPOSITORY,
        revision=MODEL_REVISION,
        local_dir=target,
        allow_patterns=ALLOW_PATTERNS,
        max_workers=MAX_WORKERS,
        force_download=False,
        token=False,
    )
    print("Required models are ready.")


if __name__ == "__main__":
    main()
