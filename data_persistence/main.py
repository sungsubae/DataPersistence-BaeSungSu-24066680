from pathlib import Path

from .models.sample import Sample
from .models.order import Order
from .models.inventory import Inventory
from .storage.json_storage import JsonStorage
from .repositories.sample_repository import SampleRepository
from .repositories.order_repository import OrderRepository
from .repositories.inventory_repository import InventoryRepository

DATA_DIR = Path(__file__).parent.parent / "data"


def main():
    sample_repo = SampleRepository(JsonStorage(DATA_DIR / "samples.json"))
    order_repo = OrderRepository(JsonStorage(DATA_DIR / "orders.json"))
    inventory_repo = InventoryRepository(JsonStorage(DATA_DIR / "inventory.json"))

    print("=== 반도체 시료 생산주문관리 — 데이터 영속성 PoC ===\n")

    sample = Sample(name="NAND-256GB", type="NAND", spec="3D V-NAND 256GB", unit="EA")
    sample_repo.create(sample)
    print(f"[CREATE] 시료: {sample.name}  id={sample.id[:8]}…")

    order = Order(customer_name="삼성전자", sample_id=sample.id, quantity=100)
    order_repo.create(order)
    print(f"[CREATE] 주문: {order.customer_name}  수량={order.quantity}  상태={order.status}")

    inventory = Inventory(sample_id=sample.id, quantity=500, location="A-1-01")
    inventory_repo.create(inventory)
    print(f"[CREATE] 재고: {inventory.quantity}{sample.unit}  위치={inventory.location}")

    found = sample_repo.read(sample.id)
    print(f"\n[READ]   시료 조회: {found.name}")

    order.status = "PROCESSING"
    order_repo.update(order)
    print(f"[UPDATE] 주문 상태 변경 → {order.status}")

    print(f"\n[LIST]   시료 {len(sample_repo.list_all())}건 / "
          f"주문 {len(order_repo.list_all())}건 / "
          f"재고 {len(inventory_repo.list_all())}건")

    print("\n완료. data/ 디렉토리에서 JSON 파일을 확인하세요.")


if __name__ == "__main__":
    main()
