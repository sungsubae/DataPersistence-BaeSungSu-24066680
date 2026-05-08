import json
from pathlib import Path


class JsonStorage:
    def __init__(self, file_path: str | Path):
        self._path = Path(file_path)
        self._path.parent.mkdir(parents=True, exist_ok=True)
        if not self._path.exists():
            self.write_all([])

    def read_all(self) -> list[dict]:
        with open(self._path, "r", encoding="utf-8") as f:
            return json.load(f)

    def write_all(self, records: list[dict]) -> None:
        # 원자적 쓰기: tmp 파일에 먼저 쓴 뒤 교체하여 파일 손상 방지
        tmp = self._path.with_suffix(".tmp")
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(records, f, ensure_ascii=False, indent=2)
        tmp.replace(self._path)

    @property
    def file_path(self) -> Path:
        return self._path
