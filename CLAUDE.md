# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 프로젝트 개요

S-Semi 반도체 회사의 **반도체 시료 생산주문관리 시스템** 개발을 위한 4개 PoC 중 **2번째 PoC — 데이터 영속성 처리**다.

전체 PoC 구성:
1. MVC 스켈레톤 코드
2. **데이터 영속성 처리 (현재 프로젝트)**
3. 데이터 모니터링 Tool
4. Dummy 데이터 생성 Tool

이 프로젝트는 PoC #2만 구현한다. 다른 PoC 기능(모니터링, Dummy 생성, MVC UI)은 이 레포에서 개발하지 않는다.

## 핵심 제약사항

- **PoC 간 독립성**: 각 PoC는 서로 의존하지 않는다. `Interface`(ABC)를 활용해 결합도를 낮추고, 다른 PoC에서 import 가능한 모듈 구조로 설계한다.
- **콘솔 기반**: UI는 콘솔 출력만 사용한다.
- **JSON 저장소**: 데이터베이스 없이 JSON 파일로 영속성을 구현한다.
- **현재 PoC 범위만 개발**: 다른 PoC 내용(MVC View/Controller, 모니터링 화면, Dummy 생성기)을 이 프로젝트에 추가하지 않는다.

## 환경 설정

Python 3.14.3, 가상환경은 `.venv`에 위치한다.

```bash
# Windows — 가상환경 활성화
.venv\Scripts\activate

# 패키지 설치 (이미 설치됨)
# colorama, pytest, pytest-cov, Pygments
```

## 주요 명령어

```bash
# 전체 테스트 실행
.venv\Scripts\pytest

# 단일 테스트 파일 실행
.venv\Scripts\pytest tests/test_repository.py

# 커버리지 포함 테스트
.venv\Scripts\pytest --cov=data_persistence --cov-report=term-missing

# 메인 실행
.venv\Scripts\python data_persistence/main.py
```

## 디렉토리 구조

```
DataPersistence-BaeSungSu-24066680/
├── data_persistence/           # PoC #2 패키지 루트 (다른 PoC에서 import할 단위)
│   ├── __init__.py
│   ├── interfaces/             # ABC 인터페이스 정의 (PoC 독립성 보장)
│   │   ├── __init__.py
│   │   └── repository.py       # IRepository[T] — CRUD 계약 정의
│   ├── models/                 # 도메인 모델 (dataclass)
│   │   ├── __init__.py
│   │   ├── sample.py           # 시료(Sample) 모델
│   │   ├── order.py            # 주문(Order) 모델
│   │   └── inventory.py        # 재고(Inventory) 모델
│   ├── repositories/           # IRepository 구현체 (JSON 파일 기반)
│   │   ├── __init__.py
│   │   ├── base_repository.py  # JsonRepository[T] 공통 구현
│   │   ├── sample_repository.py
│   │   ├── order_repository.py
│   │   └── inventory_repository.py
│   ├── storage/                # JSON 파일 I/O 저수준 레이어
│   │   ├── __init__.py
│   │   └── json_storage.py     # 파일 읽기/쓰기, 잠금 처리
│   └── main.py                 # 동작 확인용 콘솔 데모
├── tests/
│   ├── __init__.py
│   └── test_*.py
├── data/                       # JSON 데이터 파일 저장 디렉토리 (gitignore 권장)
├── .venv/
├── .gitignore
└── CLAUDE.md
```

## 아키텍처 흐름

```
[다른 PoC / main.py]
        │
        ▼
  IRepository[T]          ← interfaces/repository.py (ABC)
        │ implements
        ▼
 JsonRepository[T]         ← repositories/base_repository.py
        │ uses
        ▼
  JsonStorage              ← storage/json_storage.py (파일 R/W)
        │ reads/writes
        ▼
   data/*.json
```

- `IRepository[T]`는 `create / read / update / delete / list_all` 메서드를 추상 정의한다.
- `JsonRepository[T]`가 이를 구현하며, 모든 엔티티별 repository가 이를 상속한다.
- `JsonStorage`는 파일 경로 관리와 원자적 쓰기를 담당한다.
- 모델은 `dataclass` + `__post_init__` 유효성 검사를 사용하고, JSON 직렬화는 `dataclasses.asdict` / `dacite` 또는 커스텀 `from_dict`로 처리한다.

## 도메인 모델 핵심 필드

| 모델 | 주요 필드 |
|------|-----------|
| Sample (시료) | id, name, type, spec, unit |
| Order (주문) | id, customer, sample_id, quantity, status, created_at |
| Inventory (재고) | id, sample_id, quantity, location, updated_at |

## 다른 PoC에서 import 방법

```python
# PoC #3, #4 등에서 사용할 때
from data_persistence.interfaces.repository import IRepository
from data_persistence.repositories.order_repository import OrderRepository
from data_persistence.models.order import Order
```

`data_persistence/` 폴더를 패키지로 유지하면 상위 프로젝트에서 `sys.path`에 이 PoC 루트를 추가하거나 `pip install -e .`로 설치해 사용할 수 있다.
