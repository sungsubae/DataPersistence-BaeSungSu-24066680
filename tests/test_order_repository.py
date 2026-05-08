import pytest
from data_persistence.models.order import Order, VALID_STATUSES
from data_persistence.repositories.order_repository import OrderRepository
from data_persistence.storage.json_storage import JsonStorage


@pytest.fixture
def repo(tmp_path):
    return OrderRepository(JsonStorage(tmp_path / "orders.json"))


@pytest.fixture
def order():
    return Order(customer_name="삼성전자", sample_id="sample-001", quantity=100)


class TestOrderRepository:
    def test_create_returns_same_entity(self, repo, order):
        assert repo.create(order) is order

    def test_default_status_is_pending(self, order):
        assert order.status == "PENDING"

    def test_read_returns_none_for_missing(self, repo):
        assert repo.read("missing") is None

    def test_read_restores_all_fields(self, repo, order):
        repo.create(order)
        found = repo.read(order.id)
        assert found.customer_name == order.customer_name
        assert found.sample_id == order.sample_id
        assert found.quantity == order.quantity
        assert found.status == order.status

    def test_update_status(self, repo, order):
        repo.create(order)
        order.status = "PROCESSING"
        repo.update(order)
        assert repo.read(order.id).status == "PROCESSING"

    def test_update_raises_for_unknown_id(self, repo, order):
        with pytest.raises(KeyError):
            repo.update(order)

    def test_delete(self, repo, order):
        repo.create(order)
        assert repo.delete(order.id) is True
        assert repo.read(order.id) is None

    def test_delete_returns_false_for_missing(self, repo):
        assert repo.delete("ghost") is False

    def test_list_all(self, repo):
        for i in range(3):
            repo.create(Order(customer_name=f"고객{i}", sample_id="s-001", quantity=i + 1))
        assert len(repo.list_all()) == 3

    def test_all_valid_statuses_accepted(self):
        for status in VALID_STATUSES:
            o = Order(customer_name="고객", sample_id="s-001", quantity=1, status=status)
            assert o.status == status

    def test_invalid_status_raises(self):
        with pytest.raises(ValueError):
            Order(customer_name="고객", sample_id="s-001", quantity=1, status="SHIPPED")

    def test_zero_quantity_raises(self):
        with pytest.raises(ValueError):
            Order(customer_name="고객", sample_id="s-001", quantity=0)

    def test_negative_quantity_raises(self):
        with pytest.raises(ValueError):
            Order(customer_name="고객", sample_id="s-001", quantity=-5)

    def test_persistence_across_instances(self, tmp_path):
        path = tmp_path / "orders.json"
        o = Order(customer_name="SK하이닉스", sample_id="s-999", quantity=50)
        OrderRepository(JsonStorage(path)).create(o)
        found = OrderRepository(JsonStorage(path)).read(o.id)
        assert found.customer_name == "SK하이닉스"
