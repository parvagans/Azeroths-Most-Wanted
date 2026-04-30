import shutil
import uuid
from pathlib import Path


_WORKSPACE_TEMP_ROOT = Path(__file__).resolve().parents[1] / ".codex-temp" / "test-temp"
_WORKSPACE_TEMP_ROOT.mkdir(parents=True, exist_ok=True)


class _WorkspaceTempDir:
    def __init__(self, path: Path):
        self._path = path
        self.name = str(path)

    def cleanup(self):
        if self._path.exists():
            shutil.rmtree(self._path, ignore_errors=True)


def workspace_temp_dir():
    temp_path = _WORKSPACE_TEMP_ROOT / f"tmp-{uuid.uuid4().hex}"
    temp_path.mkdir(parents=True, exist_ok=False)
    return _WorkspaceTempDir(temp_path)
