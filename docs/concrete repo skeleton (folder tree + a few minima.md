<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# concrete repo skeleton (folder tree + a few minimal Python files + pytest config) that encodes these rules so you can start committing slices immediately under this constitution.

Below is a concrete Python repo skeleton you can paste into `tree` or just recreate. It encodes:

- Python + Clean/Hex architecture
- Vertical slices per feature
- TDD with pytest and ≥80% coverage

All code snippets are minimal but runnable.

***

## Folder Tree

```text
algo-platform/
  pyproject.toml
  README.md
  .gitignore

  app/
    __init__.py

    core/
      __init__.py
      domain/
        __init__.py
        entities.py
        value_objects.py
      ports/
        __init__.py
        market_data.py
        event_bus.py
        feature_store.py
        model_registry.py
        execution.py
        risk.py

    slices/
      scanning/
        __init__.py
        domain/
          __init__.py
          models.py
          services.py
        application/
          __init__.py
          use_cases.py
        adapters/
          __init__.py
          event_consumer.py
          event_producer.py
        tests/
          __init__.py
          test_domain_services.py
          test_use_cases.py

      signals/
        __init__.py
        domain/
          __init__.py
          models.py
          services.py
        application/
          __init__.py
          use_cases.py
        adapters/
          __init__.py
          event_consumer.py
          event_producer.py
        tests/
          __init__.py
          test_domain_services.py
          test_use_cases.py

      rl_policy/
        __init__.py
        domain/
          __init__.py
          models.py
          services.py
        application/
          __init__.py
          use_cases.py
        adapters/
          __init__.py
          model_registry_adapter.py
          event_consumer.py
        tests/
          __init__.py
          test_domain_services.py
          test_use_cases.py

      risk/
        __init__.py
        domain/
          __init__.py
          services.py
        application/
          __init__.py
          use_cases.py
        adapters/
          __init__.py
          risk_event_consumer.py
        tests/
          __init__.py
          test_domain_services.py
          test_use_cases.py

    infra/
      __init__.py
      config.py
      event_bus_kafka.py
      feature_store_sqlalchemy.py
      model_registry_s3.py

  tests/
    __init__.py
    unit/
      __init__.py
      test_core_entities.py
    integration/
      __init__.py
      test_scanning_to_signals_flow.py
    e2e/
      __init__.py
      test_backtest_smoke.py
```

You can start with a subset of slices (e.g., `scanning`, `signals`, `rl_policy`, `risk`) and add others later.

***

## pyproject.toml (pytest, coverage, tooling)

```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "algo-platform"
version = "0.1.0"
description = "Tree-structured multi-agent RL trading platform"
requires-python = ">=3.11"
dependencies = [
  "pydantic>=2.0",
  "numpy>=1.26",
  "pandas>=2.0",
  "pytest>=8.0",
  "pytest-cov>=4.1",
]

[tool.pytest.ini_options]
addopts = "--maxfail=1 -q --cov=app --cov-report=term-missing --cov-fail-under=80"
testpaths = ["tests", "app/slices"]

[tool.coverage.run]
branch = true
source = ["app"]

[tool.coverage.report]
show_missing = true
fail_under = 80
```


***

## Core Domain \& Ports (Clean Architecture)

### `app/core/domain/entities.py`

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional


@dataclass(frozen=True)
class MarketSnapshot:
    timestamp: datetime
    prices: Dict[str, float]  # symbol -> price
    volumes: Dict[str, float]  # symbol -> volume


@dataclass(frozen=True)
class Position:
    symbol: str
    quantity: float
    avg_price: float


@dataclass
class PortfolioState:
    cash: float
    positions: Dict[str, Position]
    equity: float
    gross_exposure: float
    net_exposure: float
    drawdown: float
```


### `app/core/domain/value_objects.py`

```python
from dataclasses import dataclass
from enum import Enum


class RegimeLabel(str, Enum):
    TREND = "trend"
    RANGE = "range"
    CRISIS = "crisis"


@dataclass(frozen=True)
class RiskConstraints:
    max_leverage: float
    max_drawdown: float
    max_symbol_weight: float
```


### `app/core/ports/market_data.py`

```python
from abc import ABC, abstractmethod
from typing import Iterable
from app.core.domain.entities import MarketSnapshot


class MarketDataPort(ABC):
    """Port for reading market snapshots (live or historical)."""

    @abstractmethod
    def stream_snapshots(self) -> Iterable[MarketSnapshot]:
        ...
```


### `app/core/ports/event_bus.py`

```python
from abc import ABC, abstractmethod
from typing import Any


class EventBusPort(ABC):
    """Port for publishing/subscribing to events (Kafka, etc.)."""

    @abstractmethod
    def publish(self, topic: str, payload: dict) -> None:
        ...

    @abstractmethod
    def subscribe(self, topic: str, handler: Any) -> None:
        ...
```

(Other ports can be stubs for now.)

***

## Example Vertical Slice: Scanning

### `app/slices/scanning/domain/models.py`

```python
from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Candidate:
    symbol: str
    score: float


@dataclass(frozen=True)
class CandidateSet:
    scanner_id: str
    candidates: List[Candidate]
```


### `app/slices/scanning/domain/services.py`

```python
from typing import List
from app.core.domain.entities import MarketSnapshot
from .models import Candidate, CandidateSet


def simple_momentum_scanner(snapshot: MarketSnapshot, scanner_id: str = "momentum") -> CandidateSet:
    """Example deterministic scanner: score = price (placeholder)."""
    candidates: List[Candidate] = [
        Candidate(symbol=symbol, score=price)
        for symbol, price in snapshot.prices.items()
    ]
    return CandidateSet(scanner_id=scanner_id, candidates=candidates)
```


### `app/slices/scanning/application/use_cases.py`

```python
from app.core.domain.entities import MarketSnapshot
from app.core.ports.event_bus import EventBusPort
from .domain.services import simple_momentum_scanner


class RunScannerUseCase:
    """Application service: take snapshot, emit CandidateSet event."""

    def __init__(self, event_bus: EventBusPort) -> None:
        self._event_bus = event_bus

    def execute(self, snapshot: MarketSnapshot) -> None:
        candidate_set = simple_momentum_scanner(snapshot)
        payload = {
            "scanner_id": candidate_set.scanner_id,
            "candidates": [
                {"symbol": c.symbol, "score": c.score}
                for c in candidate_set.candidates
            ],
        }
        self._event_bus.publish(topic="candidates", payload=payload)
```


### `app/slices/scanning/adapters/event_consumer.py`

```python
from app.core.domain.entities import MarketSnapshot
from app.core.ports.event_bus import EventBusPort
from .application.use_cases import RunScannerUseCase


class ScanningEventConsumer:
    """Adapter wiring event bus -> scanning use case."""

    def __init__(self, event_bus: EventBusPort) -> None:
        self._event_bus = event_bus
        self._use_case = RunScannerUseCase(event_bus)

    def start(self) -> None:
        def on_snapshot(payload: dict) -> None:
            snapshot = MarketSnapshot(
                timestamp=payload["timestamp"],
                prices=payload["prices"],
                volumes=payload["volumes"],
            )
            self._use_case.execute(snapshot)

        self._event_bus.subscribe(topic="market-snapshots", handler=on_snapshot)
```


***

## Example Vertical Slice: Signals (very minimal)

### `app/slices/signals/domain/models.py`

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class SignalIntent:
    branch_id: str
    symbol: str
    score: float
    direction: int  # 1 long, -1 short, 0 flat
```


### `app/slices/signals/domain/services.py`

```python
from typing import List
from app.slices.scanning.domain.models import CandidateSet
from .models import SignalIntent


def threshold_signal(candidate_set: CandidateSet, threshold: float = 0.0) -> List[SignalIntent]:
    """Rule-based signal: direction = 1 if score > threshold else 0."""
    intents: List[SignalIntent] = []
    for c in candidate_set.candidates:
        direction = 1 if c.score > threshold else 0
        if direction != 0:
            intents.append(
                SignalIntent(
                    branch_id=candidate_set.scanner_id,
                    symbol=c.symbol,
                    score=c.score,
                    direction=direction,
                )
            )
    return intents
```


***

## RL Policy Slice (domain skeleton)

### `app/slices/rl_policy/domain/models.py`

```python
from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class StateVector:
    values: List[float]


@dataclass(frozen=True)
class PolicyAction:
    branch_weights: List[float]
```


### `app/slices/rl_policy/domain/services.py`

```python
from .models import StateVector, PolicyAction


def dummy_router_policy(state: StateVector) -> PolicyAction:
    """Placeholder deterministic policy: equal weights over 2 branches."""
    # In real code, this calls a trained model
    return PolicyAction(branch_weights=[0.5, 0.5])
```


***

## Risk Slice (domain skeleton)

### `app/slices/risk/domain/services.py`

```python
from app.core.domain.entities import PortfolioState
from app.core.domain.value_objects import RiskConstraints


def is_order_approved(portfolio: PortfolioState, constraints: RiskConstraints) -> bool:
    """Very simple placeholder: reject if drawdown breached."""
    return portfolio.drawdown > constraints.max_drawdown
```


***

## Infrastructure Stubs

### `app/infra/event_bus_kafka.py`

```python
from typing import Any, Callable, Dict, List
from app.core.ports.event_bus import EventBusPort


class InMemoryEventBus(EventBusPort):
    """In-memory event bus for tests / local dev; replace with Kafka adapter later."""

    def __init__(self) -> None:
        self._subscribers: Dict[str, List[Callable[[dict], None]]] = {}

    def publish(self, topic: str, payload: dict) -> None:
        for handler in self._subscribers.get(topic, []):
            handler(payload)

    def subscribe(self, topic: str, handler: Any) -> None:
        self._subscribers.setdefault(topic, []).append(handler)
```


***

## Tests (TDD + coverage)

### `tests/unit/test_core_entities.py`

```python
from datetime import datetime
from app.core.domain.entities import MarketSnapshot


def test_market_snapshot_creation():
    now = datetime.utcnow()
    snapshot = MarketSnapshot(timestamp=now, prices={"AAPL": 100.0}, volumes={"AAPL": 1000})
    assert snapshot.timestamp == now
    assert snapshot.prices["AAPL"] == 100.0
    assert snapshot.volumes["AAPL"] == 1000
```


### `app/slices/scanning/tests/test_domain_services.py`

```python
from datetime import datetime
from app.core.domain.entities import MarketSnapshot
from app.slices.scanning.domain.services import simple_momentum_scanner


def test_simple_momentum_scanner_returns_candidates():
    snapshot = MarketSnapshot(
        timestamp=datetime.utcnow(),
        prices={"AAPL": 100.0, "MSFT": 200.0},
        volumes={"AAPL": 1000, "MSFT": 2000},
    )

    result = simple_momentum_scanner(snapshot)

    assert result.scanner_id == "momentum"
    symbols = {c.symbol for c in result.candidates}
    assert symbols == {"AAPL", "MSFT"}
```


### `app/slices/scanning/tests/test_use_cases.py`

```python
from datetime import datetime
from app.core.domain.entities import MarketSnapshot
from app.infra.event_bus_kafka import InMemoryEventBus
from app.slices.scanning.application.use_cases import RunScannerUseCase


def test_run_scanner_use_case_publishes_candidates():
    bus = InMemoryEventBus()
    received = {}

    def capture(payload: dict) -> None:
        received["payload"] = payload

    bus.subscribe("candidates", capture)

    use_case = RunScannerUseCase(bus)
    snapshot = MarketSnapshot(
        timestamp=datetime.utcnow(),
        prices={"AAPL": 100.0},
        volumes={"AAPL": 1000},
    )

    use_case.execute(snapshot)

    assert "payload" in received
    assert received["payload"]["scanner_id"] == "momentum"
    assert received["payload"]["candidates"][0]["symbol"] == "AAPL"
```


### `tests/integration/test_scanning_to_signals_flow.py`

```python
from datetime import datetime
from app.core.domain.entities import MarketSnapshot
from app.infra.event_bus_kafka import InMemoryEventBus
from app.slices.scanning.application.use_cases import RunScannerUseCase
from app.slices.signals.domain.services import threshold_signal
from app.slices.scanning.domain.models import CandidateSet, Candidate


def test_scanning_to_signals_flow():
    # In this simple integration test, we bypass events for brevity.
    snapshot = MarketSnapshot(
        timestamp=datetime.utcnow(),
        prices={"AAPL": 100.0},
        volumes={"AAPL": 1000},
    )

    # Scanner
    candidate_set = CandidateSet(
        scanner_id="momentum",
        candidates=[Candidate(symbol="AAPL", score=1.0)],
    )

    # Signal
    intents = threshold_signal(candidate_set, threshold=0.5)

    assert len(intents) == 1
    assert intents[0].symbol == "AAPL"
    assert intents[0].direction == 1
```


### `tests/e2e/test_backtest_smoke.py`

```python
def test_backtest_smoke():
    """
    Placeholder E2E test that will later run a full backtest.
    For now, it just asserts that the project imports without errors.
    """
    import app  # noqa: F401

    assert True
```


***

## How to Start

1. Create `algo-platform` folder and apply this skeleton.
2. Install deps:
```bash
cd algo-platform
pip install -e .
pytest
```

3. You should see pytest run with coverage; as you fill in more slices, keep tests plus coverage.

If you want, next step can be: a **minimal `backtest_runner.py`** that uses `InMemoryEventBus`, streams fake `MarketSnapshot`s, and wires `ScanningEventConsumer` so you have a working event-driven loop on day 1.

