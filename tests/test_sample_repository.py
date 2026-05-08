import pytest
from data_persistence.models.sample import Sample
from data_persistence.repositories.sample_repository import SampleRepository
from data_persistence.storage.json_storage import JsonStorage


@pytest.fixture
def repo(tmp_path):
    return SampleRepository(JsonStorage(tmp_path / "samples.json"))


@pytest.fixture
def sample():
    return Sample(name="NAND-256GB", type="NAND", spec="3D V-NAND 256GB", unit="EA")


class TestSampleRepository:
    def test_create_returns_same_entity(self, repo, sample):
        assert repo.create(sample) is sample

    def test_create_persists_to_file(self, repo, sample):
        repo.create(sample)
        assert repo.read(sample.id) is not None

    def test_read_returns_none_for_missing_id(self, repo):
        assert repo.read("does-not-exist") is None

    def test_read_restores_all_fields(self, repo, sample):
        repo.create(sample)
        found = repo.read(sample.id)
        assert found.id == sample.id
        assert found.name == sample.name
        assert found.type == sample.type
        assert found.spec == sample.spec
        assert found.unit == sample.unit

    def test_update_changes_field(self, repo, sample):
        repo.create(sample)
        sample.spec = "3D V-NAND 512GB"
        repo.update(sample)
        assert repo.read(sample.id).spec == "3D V-NAND 512GB"

    def test_update_raises_for_unknown_id(self, repo, sample):
        with pytest.raises(KeyError):
            repo.update(sample)

    def test_delete_returns_true(self, repo, sample):
        repo.create(sample)
        assert repo.delete(sample.id) is True

    def test_delete_removes_entity(self, repo, sample):
        repo.create(sample)
        repo.delete(sample.id)
        assert repo.read(sample.id) is None

    def test_delete_returns_false_for_missing(self, repo):
        assert repo.delete("ghost-id") is False

    def test_list_all_empty_initially(self, repo):
        assert repo.list_all() == []

    def test_list_all_returns_every_record(self, repo):
        for i in range(3):
            repo.create(Sample(name=f"S-{i}", type="NAND", spec="spec", unit="EA"))
        assert len(repo.list_all()) == 3

    def test_persistence_across_instances(self, tmp_path):
        path = tmp_path / "samples.json"
        s = Sample(name="Persist", type="DRAM", spec="LPDDR5", unit="EA")
        SampleRepository(JsonStorage(path)).create(s)
        found = SampleRepository(JsonStorage(path)).read(s.id)
        assert found is not None
        assert found.name == "Persist"

    def test_model_rejects_empty_name(self):
        with pytest.raises(ValueError):
            Sample(name="   ", type="NAND", spec="spec", unit="EA")

    def test_model_rejects_empty_type(self):
        with pytest.raises(ValueError):
            Sample(name="S-1", type="  ", spec="spec", unit="EA")
