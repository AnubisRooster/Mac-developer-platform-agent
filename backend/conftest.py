"""Root conftest — ensure backend/ is the only import path for project packages."""

import os
import sys
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = BACKEND_ROOT.parent

# Force backend/ to be the ONLY source for project packages.
# Remove ALL paths that could resolve to the old root-level packages.
_remove = set()
for p in sys.path:
    resolved = Path(p).resolve() if p else None
    if resolved and resolved == PROJECT_ROOT.resolve():
        _remove.add(p)
for p in _remove:
    while p in sys.path:
        sys.path.remove(p)

# Ensure backend/ is first
backend_str = str(BACKEND_ROOT)
while backend_str in sys.path:
    sys.path.remove(backend_str)
sys.path.insert(0, backend_str)

# Purge any previously-cached project modules that came from the old location
_project_packages = (
    "agent", "database", "events", "integrations",
    "security", "tools", "webhooks", "workflows",
)
for mod_name in list(sys.modules.keys()):
    if any(mod_name == pkg or mod_name.startswith(pkg + ".") for pkg in _project_packages):
        del sys.modules[mod_name]
