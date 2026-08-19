from __future__ import annotations

from pathlib import Path


def main() -> None:
    source = Path(__file__).resolve().parent / "app" / "gradio_demo.py"
    old = "parser.add_argument(\"--open_browser\", action='store_true', default=True,"
    new = "parser.add_argument(\"--open_browser\", action='store_true', default=False,"

    text = source.read_text(encoding="utf-8")
    if new in text:
        print("SUPIR browser behavior is already configured for Pinokio.")
        return
    if old not in text:
        raise SystemExit(
            "The pinned SUPIR source no longer matches the expected browser setting."
        )

    source.write_text(text.replace(old, new, 1), encoding="utf-8", newline="\n")
    print("Disabled SUPIR's extra browser popup; Pinokio will expose the Web UI.")


if __name__ == "__main__":
    main()
