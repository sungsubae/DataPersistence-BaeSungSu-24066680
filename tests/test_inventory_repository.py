import pytest
from data_persistence.models.inventory import Inventory
from data_persistence.repositories.inventory_repository import InventoryRepository
from data_persistence.storage.json_storage import JsonStorage


@pytest.fixture
def repo(tmp_path):
    return InventoryRepository(JsonStorage(tmp_path / "inventory.json"))


@pytest.fixture
def inventory():
    return Inventory(sample_id="sample-001", quantity=500, location="A-1-01")


class TestInventoryRepository:
    def test_create_returns_same_entity(self, repo, inventory):
        assert repo.create(inventory) is inventory

    def test_read_restores_all_fields(self, repo, inventory):
        repo.create(inventory)
        found = repo.read(inventory.id)
        assert found.sample_id == inventory.sample_id
        assert found.quantity == inventory.quantity
        assert found.location == inventory.location

    def test_read_returns_none_for_missing(self, repo):
        assert repo.read("no-such-id") is None

    def test_update_quantity(self, repo, inventory):
        repo.create(inventory)
        inventory.quantity = 300
        repo.update(inventory)
        assert repo.read(inventory.id).quantity == 300

    def test_update_location(self, repo, inventory):
        repo.create(inventory)
        inventory.location = "B-2-05"
        repo.update(inventory)
        assert repo.read(inventory.id).location == "B-2-05"

    def test_update_raises_for_unknown_id(self, repo, inventory):
        with pytest.raises(KeyError):
            repo.update(inventory)

    def test_delete(self, repo, inventory):
        repo.create(inventory)
        assert repo.delete(inventory.id) is True
        assert repo.read(inventory.id) is None

    def test_delete_returns_false_for_missing(self, repo):
        assert repo.delete("phantom") is False

    def test_list_all(self, repo):
        for i in range(4):
            repo.create(Inventory(sample_id=f"s-{i:03d}", quantity=i * 100, location=f"A-{i}"))
        assert len(repo.list_all()) == 4

    def test_zero_quantity_is_valid(self):
        inv = Inventory(sample_id="s-001", quantity=0, location="A-1")
        assert inv.quantity == 0

    def test_negative_quantity_raises(self):
        with pytest.raises(ValueError):
            Inventory(sample_id="s-001", quantity=-1, location="A-1")

    def test_persistence_across_instances(self, tmp_path):
        path = tmp_path / "inventory.json"
        inv = Inventory(sample_id="s-persist", quantity=999, location="Z-9-99")
        InventoryRepository(JsonStorage(path)).create(inv)
        found = InventoryRepository(JsonStorage(path)).read(inv.id)
        assert found.quantity == 999
