import pytest
from data_persistence.storage.json_storage import JsonStorage


class TestJsonStorage:
    def test_creates_file_on_init(self, tmp_path):
        path = tmp_path / "new.json"
        assert not path.exists()
        JsonStorage(path)
        assert path.exists()

    def test_initial_read_returns_empty_list(self, tmp_path):
        storage = JsonStorage(tmp_path / "test.json")
        assert storage.read_all() == []

    def test_write_and_read_roundtrip(self, tmp_path):
        storage = JsonStorage(tmp_path / "test.json")
        records = [{"id": "abc", "name": "NAND-A"}]
        storage.write_all(records)
        assert storage.read_all() == records

    def test_write_overwrites_previous(self, tmp_path):
        storage = JsonStorage(tmp_path / "test.json")
        storage.write_all([{"id": "1"}])
        storage.write_all([{"id": "2"}])
        assert storage.read_all() == [{"id": "2"}]

    def test_write_multiple_records(self, tmp_path):
        storage = JsonStorage(tmp_path / "test.json")
        records = [{"id": str(i)} for i in range(5)]
        storage.write_all(records)
        assert len(storage.read_all()) == 5

    def test_creates_parent_directories(self, tmp_path):
        path = tmp_path / "nested" / "sub" / "test.json"
        JsonStorage(path)
        assert path.exists()

    def test_file_path_property(self, tmp_path):
        path = tmp_path / "test.json"
        storage = JsonStorage(path)
        assert storage.file_path == path

    def test_korean_characters_preserved(self, tmp_path):
        storage = JsonStorage(tmp_path / "test.json")
        storage.write_all([{"name": "반도체 시료"}])
        assert storage.read_all()[0]["name"] == "반도체 시료"

    def test_no_tmp_file_after_write(self, tmp_path):
        path = tmp_path / "test.json"
        storage = JsonStorage(path)
        storage.write_all([{"id": "1"}])
        assert not path.with_suffix(".tmp").exists()

    def test_accepts_string_path(self, tmp_path):
        storage = JsonStorage(str(tmp_path / "test.json"))
        assert storage.read_all() == []
