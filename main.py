#!/usr/bin/env python3
"""news-image-20261122 entrypoint (Python 3.13, standard library only).

The image is the entry.png beside this file: a newspaper front page
drawn for Sunday 22 November 2026 by render_image.py in this repo.
This program copies it to /output/entry.png (or MAKEFUN_OUTPUT_DIR
when set, for local runs). No network, no randomness: every run
writes the same bytes.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    src = os.path.join(HERE, "entry.png")
    if not os.path.isfile(src):
        raise SystemExit("entry.png missing next to main.py")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
