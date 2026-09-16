#!/usr/bin/env python3
"""Allow `python -m kitten_pomo` and the ~/.local/bin symlink target."""

import sys
from pathlib import Path

# When executed as a script via symlink, ensure the package parent is importable.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from kitten_pomo.app import main

if __name__ == "__main__":
    main()
