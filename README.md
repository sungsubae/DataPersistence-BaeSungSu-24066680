# DataPersistence PoC — 반도체 시료 생산주문관리 시스템

> **S-Semi** 반도체 회사 생산주문관리 시스템 개발을 위한 4개 PoC 중 **#2 데이터 영속성 처리**

---

## 개요

JSON 파일을 저장소로 사용하여 시료(Sample) · 주문(Order) · 재고(Inventory) 데이터의 생성 · 조회 · 수정 · 삭제(CRUD)를 구현한다.

---

## 프로젝트 구조

```
DataPersistence-BaeSungSu-24066680/
├── data_persistence/               # 다른 PoC에서 import할 패키지
│   ├── interfaces/
│   │   └── repository.py           # IRepository[T] — CRUD 추상 계약
│   ├── models/
│   │   ├── sample.py               # 시료 (name, type, spec, unit)
│   │   ├── order.py                # 주문 (customer_name, sample_id, quantity, status)
│   │   └── inventory.py            # 재고 (sample_id, quantity, location)
│   ├── storage/
│   │   └── json_storage.py         # JSON 파일 R/W (원자적 쓰기)
│   ├── repositories/
│   │   ├── base_repository.py      # JsonRepository[T] — IRepository 공통 구현
│   │   ├── sample_repository.py
│   │   ├── order_repository.py
│   │   └── inventory_repository.py
│   └── main.py                     # 동작 확인용 콘솔 데모
├── tests/
│   ├── test_json_storage.py
│   ├── test_sample_repository.py
│   ├── test_order_repository.py
│   └── test_inventory_repository.py
├── data/                           # 런타임 JSON 저장 위치 (git 미추적)
├── pyproject.toml                  # pytest · coverage 설정
└── CLAUDE.md
```

---

## 환경 설정

Python 3.14.3 / 가상환경 `.venv`

```powershell
# 가상환경 활성화
.venv\Scripts\activate
```

추가 패키지 설치는 필요 없다. `pytest`, `pytest-cov`, `colorama` 가 이미 `.venv`에 포함되어 있다.

---

## 테스트 실행

```powershell
# 전체 테스트 + 커버리지 리포트
pytest

# 특정 파일만
pytest tests/test_json_storage.py

# 특정 테스트 하나만
pytest tests/test_order_repository.py::TestOrderRepository::test_update_status

# HTML 커버리지 리포트 열기
start htmlcov\index.html
```

**커버리지 기준**: 80% 미만이면 테스트 suite가 실패 처리된다.

현재 결과: **50 passed · 커버리지 100%**

---

## 동작 확인 (데모)

```powershell
python -m data_persistence.main
```

`data/` 디렉토리에 `samples.json` · `orders.json` · `inventory.json` 이 생성된다.

---

## 아키텍처

```
IRepository[T]          interfaces/repository.py
      │ implements
JsonRepository[T]       repositories/base_repository.py
      │ uses
JsonStorage             storage/json_storage.py   ← 원자적 쓰기 (.tmp → replace)
      │ reads/writes
data/*.json
```

- 모델은 `@dataclass` + `__post_init__` 유효성 검사를 사용한다.
- JSON 직렬화는 `dataclasses.asdict()` / `Model(**dict)` 로 처리한다.
- 각 테스트는 pytest의 `tmp_path` 픽스처로 격리된 임시 파일을 사용하므로 실제 `data/` 를 오염시키지 않는다.

### 주문 상태 전이

```
PENDING → PROCESSING → COMPLETED
                     → CANCELLED
```

---

## 다른 PoC에서 사용하는 방법

```python
import sys
sys.path.append("/path/to/DataPersistence-BaeSungSu-24066680")

from data_persistence import SampleRepository, OrderRepository, InventoryRepository
from data_persistence import JsonStorage, Sample, Order, Inventory

repo = SampleRepository(JsonStorage("data/samples.json"))
sample = Sample(name="NAND-256GB", type="NAND", spec="3D V-NAND", unit="EA")
repo.create(sample)
found = repo.read(sample.id)
```

인터페이스만 의존할 경우:

```python
from data_persistence.interfaces.repository import IRepository
```
