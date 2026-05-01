# Master Plan — `master-marl`

**A research-grade Multi-Agent Reinforcement Learning codebase for algorithmic trading.**

Compiled 2026-05-01 by synthesizing 34 research-notes documents in `docs/` (≈2,650 unique external references) and a curated fetch of the highest-cited papers, books, and frameworks. Owner: Nelson Vega (Kleio Technology). Personal arc: senior engineer levelling into agentic-AI / quant-ML researcher; 2025 left explicit unfinished work on MARL implementations, full RAG platform, and backtesting infra — this plan closes that loop in 2026.

---

## 0. North Star

Build a **production-discipline, research-grade MARL trading platform** that:

1. Treats agents as **specialized RL policies** (not LLM orchestration units) operating in a simulated and live market environment.
2. Defaults to **CTDE + MAPPO** as the backbone, with QMIX / MADDPG as drop-in alternatives for discrete-cooperative and continuous-mixed regimes respectively.
3. Is built on a **clean / hexagonal vertical-slice** Python codebase (the `algo-platform` skeleton from `docs/concrete repo skeleton`) with ≥80% test coverage and event-bus communication.
4. Ships through a **shadow → advisory → autonomous** progressive-deployment ladder with kill switches, position limits, and circuit breakers from day one.
5. Closes the **sim-to-real gap** explicitly — domain randomization, walk-forward validation, transaction-cost modeling, latency simulation — rather than treating live deployment as an afterthought.

Non-goals: LLM-as-trading-agent paradigms (LangMARL, FLAG-Trader) are tracked but not the primary architecture; agentic-LLM tooling (AutoGen, crewAI, Azure AI Foundry) lives in a sibling research track, not in `app/`.

---

## 1. Repository Architecture

### 1.1 Top-level layout (canonical)

Adopts the `concrete repo skeleton` blueprint with one MARL-specific addition (`research/` for paper reproductions and curriculum exercises):

```
master-marl/
├── app/                                # production codebase (clean architecture)
│   ├── core/
│   │   ├── domain/                     # entities & value objects
│   │   │   ├── entities.py             # MarketSnapshot, Position, PortfolioState
│   │   │   └── value_objects.py        # RegimeLabel, RiskConstraints, SignalIntent, PolicyAction
│   │   └── ports/                      # hexagonal interfaces (no impls)
│   │       ├── market_data.py
│   │       ├── event_bus.py
│   │       ├── feature_store.py
│   │       ├── model_registry.py
│   │       ├── execution.py
│   │       └── risk.py
│   ├── slices/                         # vertical features
│   │   ├── scanning/                   # Layer 1: ingest → CandidateSets
│   │   ├── signals/                    # Layer 2: pattern detection → SignalIntents
│   │   ├── rl_policy/                  # Layer 3: MARL policies → PolicyAction
│   │   ├── risk/                       # Layer 4: shielded action filter
│   │   └── execution/                  # Layer 5: order routing
│   └── infra/                          # adapter implementations
│       ├── config.py
│       ├── event_bus_kafka.py          # InMemoryEventBus for dev/test
│       ├── feature_store_sqlalchemy.py
│       └── model_registry_s3.py
├── research/                           # NEW — research track, separate from app/
│   ├── curriculum/                     # week-by-week Sutton & Barto + MARL Book exercises
│   ├── reproductions/                  # MAPPO, QMIX, MADDPG paper repros
│   ├── envs/                           # custom market envs (PettingZoo-compatible)
│   └── notebooks/
├── tests/{unit, integration, e2e}/
├── docs/                               # existing research notes (preserved)
├── pyproject.toml                      # --cov-fail-under=80
└── MASTER_PLAN.md                      # this file
```

**Design rules** (lifted from the skeleton doc, hardened for MARL):

- Every slice is self-contained: `domain/`, `application/`, `adapters/`, `tests/`. Features ship end-to-end.
- Slices communicate **only** via the `EventBusPort` — never by direct import.
- `InMemoryEventBus` for dev/test; Kafka adapter only in `infra/`.
- The `rl_policy` slice owns training, inference, and policy-versioning; it consumes `SignalIntents` and emits `PolicyAction.branch_weights`.
- The `risk` slice is a **shield** in the formal-verification sense: it sits between `rl_policy` output and `execution` input, with the right to veto. (See §6 — shielded action spaces achieved 98.6% safe-action rates in the cited literature.)

### 1.2 Layered conceptual model

When discussing the system informally, use the **8-layer model** from `docs/Domain Mapping ... Complex Pipelines.md`:

| Layer | Concern | Owner slice |
|---|---|---|
| 0 | Mathematical foundations (MDP, POSG, Dec-POMDP) | — (theory) |
| 1 | Data ingest & feature engineering | `scanning` |
| 2 | Pattern detection & signal generation | `signals` |
| 3 | Policy / algorithm selection | `rl_policy` |
| 4 | Risk shield & constraint enforcement | `risk` |
| 5 | Execution & order routing | `execution` |
| 6 | Inter-agent communication topology | `rl_policy` (training graph) |
| 7 | Observability, monitoring, drift detection | `infra` |

### 1.3 Architecture pattern decision

Five candidate patterns surface across the docs (`docs/Designing a Multi-Agent System for Pattern-Driven.md`). Decision matrix:

| Pattern | When | Verdict |
|---|---|---|
| Hierarchical (master-coordinator + specialists) | Regulated broker-dealer, audit trails | Adopt for the **agent topology inside `rl_policy`** (see §3) |
| Distributed peer + Byzantine consensus | HFT prop, multi-venue | Defer until live multi-venue |
| Pure RL-MAS in simulated LOB | Research lab, adaptive strategies | Adopt for `research/` track |
| Hybrid rule-based + AI | Production with explainability | Adopt for `risk` shield + fallback |
| Microservices / event-bus | Independent scaling, resilience | **Adopt as the platform substrate** |

Net: **Microservices substrate (Pattern 5) + Hierarchical agent topology (Pattern 1) inside the RL slice + Hybrid rule-based shield (Pattern 4) at the risk boundary.**

---

## 2. Algorithm Stack

### 2.1 Default backbone

**MAPPO** (Yu et al. 2022, NeurIPS) with parameter sharing, value normalization, and death masking — the BAIR-blog recipe. Justification: surprising effectiveness (matches/beats QMIX and MADDPG on standard benchmarks), single-algorithm engineering surface, and on-policy training is more stable for the non-stationary regimes that matter in markets.

### 2.2 Drop-in alternatives (same `rl_policy` interface)

| Algorithm | Use when | Reference |
|---|---|---|
| **QMIX** (Rashid 2018) | Cooperative, discrete actions, IGM holds | `oxwhirl/pymarl`, ch. 5 of MARL Book |
| **MADDPG** (Lowe 2017) | Continuous + mixed coop/competitive | `marlbenchmark/off-policy` |
| **IPPO** | Decentralized baseline / sanity check | EPyMARL |
| **HAPPO/HATRPO** | Heterogeneous agents, no parameter sharing | MARLlib |
| **MAVA** | Partial-observability + binary messaging | InstaDeep Mava |

**Counterfactual credit assignment (COMA)** and **value decomposition (VDN/QMIX/QPLEX)** stay in the toolbox but are not the first reach.

### 2.3 Single-agent prerequisites (mastered before MARL training)

DQN, Double/Dueling DQN, REINFORCE, A2C/A3C, TRPO, **PPO**, SAC, DDPG, TD3. Implementations referenced from CleanRL and Stable-Baselines3; reproduction lives in `research/reproductions/single_agent/`.

### 2.4 Frontier methods (tracked, not yet adopted)

LLM+RL (RLVR/GRPO/MAGRPO, DeepSeek-R1 style binary verifiable rewards), DiscoRL (Nature, Oct 2025), Reinforcement Networks (ICLR 2026), SRMT, MarsRL Solver→Verifier→Corrector. Quarterly review against the Berkeley MARL Seminar feed.

---

## 3. Trading-Specific Application Design

### 3.1 Agent role topology (initial)

Three-tier hierarchy inside `rl_policy`:

```
Tier 1  Orchestrator / Allocator        (one)
            │
            ▼
Tier 2  Strategy Coordinators           (per regime: trend / range / crisis)
            │
            ▼
Tier 3  Execution Specialists           (per role)
            ├── Scalper            sub-second alpha
            ├── Market-maker      spread capture, inventory-aware
            ├── Momentum rider    breakout/trend
            └── Hedger            risk-neutralization
```

This compresses the corpus's 4-role taxonomy (`docs/🧠 Domain Analysis...`) and the 7-agent SaaS template (`docs/update laste version`) into a structure suitable for the trading domain. Rationale: **2–3 heterogeneous agents beat monolithic single agents** (corpus consensus), but more agents introduce coordination overhead and emergent failure modes — start small.

### 3.2 Observation space

| Feature group | Source | Notes |
|---|---|---|
| LOB features | venue feed | bid/ask depth, imbalance, microprice |
| OHLCV + technicals | bar aggregator | VWAP, returns, RSI, MACD |
| Cross-asset graph | rolling 5-min correlation | edges for GNN/GAT in Tier-2 critic |
| Portfolio state | `PortfolioState` entity | cash, positions, exposure, drawdown |
| Regime label | upstream regime detector | trend / range / crisis (one-hot) |
| Latency / partial-obs noise | simulator | injected to force robustness |

### 3.3 Action space

- Tier 1: branch weights (continuous simplex over Tier-2 strategies).
- Tier 2: strategy-conditional action priors.
- Tier 3: discrete {long, short, flat} per symbol, optionally with size scaling.

Continuous size scaling at Tier 3 is a flag — start discrete to constrain the search space.

### 3.4 Reward design

**Composite multi-objective reward**, audited per release:

```
R = w_1 · differential_return
  - w_2 · downside_volatility
  - w_3 · transaction_cost
  - w_4 · inventory_variance        (market-maker only)
  - w_5 · drawdown_penalty
  + w_6 · risk-adjusted_return      (Sharpe / Sortino, episode-end)
```

- Differential Sharpe is **not** used as the step-wise reward (corpus flags non-convexity and gaming risk when volatility contributes as 1/x).
- **Turbulence-adjusted gating**: above a threshold (Mahalanobis distance on returns), switch to capital-preservation reward. The corpus reports 60% drawdown reduction in 2020-style crashes.
- Binary verifiable reward (DeepSeek-R1 style) is reserved for the `research/` track curriculum learning, not the production policy.

### 3.5 Environment / simulator

**Primary**: PettingZoo-compatible custom env wrapping a matching engine + LOB replay. Implementation reference: **ABIDES-Gym** (most realistic, supports crisis scenarios) and **FinRL-Meta** (multi-asset, 784+ datasets) for cross-validation.

**Secondary** (research): **JaxMARL-HFT** for 240× CPU speedup once architecture stabilizes.

---

## 4. Training & Evaluation Infrastructure

### 4.1 Framework choice

| Tier | Choice | Why |
|---|---|---|
| **Production** | EPyMARL | Cleanest path to MAPPO/IPPO on Gymnasium-compatible envs |
| **Scale** | MARLlib (Ray/RLlib) | Distributed when `EPyMARL` saturates one node |
| **Reference correctness** | `Lizhi-sjtu/MARL-code-pytorch` | Compact, readable PyTorch impls for porting |

The MARLlib-vs-RLlib-vs-Mava conflict in the corpus resolves as: **EPyMARL first (research velocity), MARLlib second (scale), Mava if JAX speed becomes the bottleneck** (currently it's not — algorithm correctness is).

### 4.2 Training loop

CTDE with:

- **Centralized critic** sees global state (full portfolio + cross-agent inventory + regime label).
- **Decentralized actors** see only their slice's local observation.
- **Distributed prioritized experience replay** with cross-agent normalization.
- **Adversarial / red-team training** runs nightly against perturbed observations.
- **Concept-drift detector** on reward distribution + action success rate → triggers retraining.

### 4.3 Evaluation harness (the discipline gate)

Every policy version runs through, in order:

1. **In-sample** training metrics (Sharpe, max drawdown, hit rate, turnover).
2. **Walk-forward out-of-sample** on at least 3 disjoint windows.
3. **Adversarial validation** (López de Prado): can a classifier distinguish train from test? If yes, distribution drift; investigate before promoting.
4. **Regime-conditional evaluation**: separate Sharpe per {trend, range, crisis} regime.
5. **Transaction-cost stress test**: linear, square-root, and Almgren-Chriss impact models.
6. **Latency stress test**: 0ms, 50ms, 200ms, 1s injected.
7. **Sim-to-real shadow run**: paper trading for ≥4 weeks before any live capital.

Promotion criteria are explicit and stored in `app/slices/rl_policy/promotion_criteria.yml`.

### 4.4 Compute budget

Single RTX 4090 (24GB) is sufficient for the four reference combos in `docs/🧠 Domain Analysis...`. Cloud burst (Ray on AWS or Azure) only when sweeping ≥4 algorithm × env combos in parallel.

---

## 5. Learning Roadmap (8 weeks → 6 months)

### 5.1 Foundations (weeks 1–4)

Sutton & Barto chapters 1–6 + the MARL Book chapters 1–4. Daily exercises into `research/curriculum/week_NN/`. Pair with **DeepMind × UCL RL Course** (Silver / Hasselt) or **Berkeley CS285** (Levine) — pick one and finish it.

Capstone: implement DQN + PPO from scratch in `research/reproductions/single_agent/` against CartPole and LunarLander; reproduce within 5% of published returns.

### 5.2 MARL core (weeks 5–8)

MARL Book chapters 5–8 + IIIA-CSIC MARL course (free YouTube, follows the textbook). Reproductions:

1. IPPO and MAPPO on PettingZoo's `simple_spread`.
2. QMIX on a small SMAC scenario.
3. MADDPG on PettingZoo's `simple_adversary`.

Capstone: port the best one into a PettingZoo-wrapped toy market env (1 asset, 2 agents, no cost model).

### 5.3 Trading domain (months 3–4)

López de Prado *Advances in Financial ML* + Lehalle & Laruelle *Market Microstructure in Practice* + Stanford CME 241. Build:

1. `app/slices/scanning` and `signals` end-to-end on historical data.
2. Walk-forward harness in `research/notebooks/`.
3. Transaction-cost & latency simulator.

### 5.4 Production MARL (months 5–6)

Full hierarchical agent topology in `app/slices/rl_policy` against the simulator. Shielded actions live in `risk`. Shadow-mode deployment with broker-API connector behind a feature flag. Albrecht/Christianos/Schäfer chapters 9–11 for advanced topics (hierarchical, mean-field, offline MARL).

---

## 6. Operational Discipline (production gates)

Lifted from `docs/Best Practices for Implementing Multi-Agent Reinfo.md` and the K8s analyses, hardened for trading:

- **Shielded action spaces** (LTL formal verification): the `risk` slice enforces hard constraints (drawdown, position limits, leverage caps) that the policy cannot override.
- **Progressive deployment ladder**: shadow (no orders) → advisory (orders to trader UI) → autonomous (live, kill-switch armed). Reported in literature: "92% faster user acceptance vs big-bang."
- **Multi-objective monitoring**: P&L, Sharpe, drawdown, hit rate, turnover, slippage, fill ratio, and **policy entropy** as a distribution-drift signal.
- **Kill-switch criteria** (any one trips → autonomous mode → advisory): drawdown > X bps in N minutes, fill ratio < threshold, latency p99 > threshold, action distribution KL > threshold.
- **Position limits & circuit breakers** are **policy-independent** (enforced in `risk`), never trusted to the learned policy.
- **Audit trail**: every order is annotated with `(policy_version, signal_versions, observation_hash, risk_decision)` for regulatory replay.

---

## 7. The Big Open Questions (decisions deferred, but tracked)

1. **Sim-to-real gap** — the corpus calls this the #1 unsolved problem. Mitigation stack: domain randomization + adversarial training + shadow mode. No claim of resolution.
2. **MAPPO vs QMIX final verdict** — corpus is split. Decision: MAPPO is default; revisit per-environment with EPyMARL benchmarks.
3. **CTDE-is-it-centralized-enough** — CADP (2023) argues it isn't. Tracked; not yet a blocker.
4. **Endogeneity / market impact** — multi-agent feedback loops can move markets. Mitigation: position-size caps as % ADV; impact model in cost simulator.
5. **Sample complexity** — 2.5–4.5M env steps ≈ thousands of years of daily data. Forces synthetic-data generation (GANs, ABMs) and transfer learning. Approach: ABIDES-Gym population for synthetic LOB sequences; transfer to real.
6. **LLM-as-agent vs MARL-as-policy** — corpus is split; the master plan picks MARL-as-policy as primary. LLM agents stay in `research/` until evidence demands otherwise.
7. **Reward design** — composite multi-objective is the current default but corpus also champions sparse / binary-verifiable. Evaluate both in `research/reward_ablation.ipynb`.
8. **Regulatory / audit posture** — `risk` slice plus the audit trail above is the working answer. Re-validate once a real broker is in scope.

---

## 8. Curated Reference Catalog

### 8.1 Foundational books (the canonical pair + microstructure)

- Sutton & Barto, *Reinforcement Learning: An Introduction* (2nd ed.) — incompleteideas.net/book/the-book-2nd.html
- Albrecht, Christianos & Schäfer, *Multi-Agent Reinforcement Learning: Foundations and Modern Approaches* (MIT Press 2024) — https://www.marl-book.com (free PDF + codebase + slides)
- Shoham & Leyton-Brown, *Multiagent Systems* (Cambridge, free) — game theory foundations
- Lapan, *Deep RL Hands-On* (3rd ed.)
- López de Prado, *Advances in Financial Machine Learning*
- Lehalle & Laruelle, *Market Microstructure in Practice*

### 8.2 Top-cited papers (verified)

- Huh & Mohapatra (2023) — *Multi-agent RL: A Comprehensive Survey* — https://arxiv.org/abs/2312.10256
- Zhang, Yang, Başar (2019) — *MARL: A Selective Overview of Theories and Algorithms* — https://arxiv.org/abs/1911.10635
- Yu et al. (NeurIPS 2022) — *The Surprising Effectiveness of PPO in Cooperative MARL (MAPPO)* — https://arxiv.org/abs/2103.01955 + BAIR blog http://bair.berkeley.edu/blog/2021/07/14/mappo/
- Liu et al. — *FinRL: Deep RL Framework for Quantitative Finance* — https://arxiv.org/abs/2111.09395
- Sun, Huang, Pompili (2024) — *LLM-based MARL: Current and Future Directions* — https://arxiv.org/abs/2409.03052
- Xiang et al. (2024) — *From Centralized to Self-Supervised: Pursuing Realistic MARL* — https://arxiv.org/abs/2405.11106
- Liu et al. (TPAMI) — *MIXRTs: Interpretable MARL via Mixing Recurrent Soft Decision Trees* — https://arxiv.org/abs/2209.07225
- Zhang et al. (2023) — *TGCNet: Dynamic Directed Graph Communication for MARL* — https://arxiv.org/abs/2312.08662
- Mavroudis et al. (2025) — *Guidelines for Applying RL/MARL in Cybersecurity* (deployment-readiness checklists transfer to trading) — https://arxiv.org/abs/2503.04262
- Zhang et al. (2022) — *Global Convergence of Localized Policy Iteration in Networked MARL* — https://arxiv.org/abs/2211.17116
- Amato — *Introduction to CTDE in Cooperative MARL* — https://www.ccs.neu.edu/home/camato/publications/IntroMARL.pdf

**Mis-cited in the corpus** (do not propagate): `arxiv.org/abs/2102.04883` resolves to a general ML-for-sciences textbook, not MARL; `arxiv.org/abs/2107.13671` resolves to Raschka's pedagogy paper. Replace with the intended citations before publishing.

**Paywalled / failed** (manual retrieval needed): `sciencedirect.com/.../S2949855424000042`; `adasci.org/all-you-need-to-know-about-multi-agent-reinforcement-learning/` (404).

### 8.3 Frameworks & repos (the working stack)

- **EPyMARL** — https://github.com/uoe-agents/epymarl (default training framework)
- **MARLlib** — https://github.com/Replicable-MARL/MARLlib (scale path) + docs https://marllib.readthedocs.io
- **PettingZoo** — https://github.com/Farama-Foundation/PettingZoo (env API standard)
- **PyMARL** — https://github.com/oxwhirl/pymarl (historical reference)
- **MARL-code-pytorch** — https://github.com/Lizhi-sjtu/MARL-code-pytorch (reference implementations)
- **deep-marl-toolkit** — https://github.com/jianzhnie/deep-marl-toolkit (taxonomy reference)
- **FinRL** — https://github.com/AI4Finance-Foundation/FinRL (domain anchor; project starts as a MARL extension of this)
- **ABIDES-Gym** — most realistic LOB simulator
- **MARL-Papers** — https://github.com/LantaoYu/MARL-Papers (rolling literature)

### 8.4 Courses (pick one per phase, finish it)

- **Foundations**: Berkeley CS285 (Levine) **or** DeepMind × UCL RL Course (Silver) **or** Stanford CS234 (Brunskill)
- **MARL**: IIIA-CSIC MARL course (Albrecht, follows the textbook) **or** Berkeley Multi-Agent Learning Seminar
- **Trading**: Stanford CME 241 (RL applications in finance) **or** Oxford Saïd Algorithmic Trading Programme
- **Practical**: HuggingFace Deep RL Course (free, certificate); OpenAI Spinning Up; DeepLearning.AI *Multi AI Agent Systems with crewAI* (for the LLM-agent sibling track only)

---

## 9. Milestone Plan (calendar)

| Milestone | Target date | Definition of done |
|---|---|---|
| M0 — Repo scaffold | 2026-05-15 | `app/` skeleton + `pyproject.toml` + ≥80% coverage gate green; `MASTER_PLAN.md` reviewed |
| M1 — Single-agent reproductions | 2026-06-15 | DQN + PPO within 5% of published returns on CartPole/LunarLander |
| M2 — MARL reproductions | 2026-07-31 | MAPPO + QMIX on PettingZoo within 10% of published; W&B dashboards live |
| M3 — Toy market env | 2026-08-31 | PettingZoo env, 1 asset, 2 agents, transaction-cost model, walk-forward harness |
| M4 — Hierarchical agents | 2026-10-15 | Tier 1/2/3 topology in `rl_policy`; 3 specialist agents trainable end-to-end |
| M5 — Risk shield | 2026-11-15 | Formal-verification-style action filter; promotion criteria YAML; audit trail |
| M6 — Shadow mode | 2026-12-31 | Broker-API connector behind feature flag; ≥4 weeks paper trading; sign-off doc |

Each milestone closes with a written postmortem in `docs/postmortems/MN_*.md` covering: what shipped, what didn't, what surprised, what's next.

---

## 10. What this plan deliberately does **not** do

- It does not commit to LLM-as-trading-agent as the primary paradigm. Tracked, not adopted.
- It does not chase JAX/Mava performance until correctness on EPyMARL is proven.
- It does not deploy autonomous trading without the full ladder (shadow → advisory → autonomous).
- It does not promise that backtested Sharpe = live Sharpe. The evaluation harness exists precisely because that promise is false.
- It does not collapse research and production into the same code path. `app/` and `research/` are separate; promotions from `research/` to `app/` go through a written PR review with the promotion criteria as the checklist.

---

**Source material**: 34 documents in `docs/` (≈2,650 unique URL references; full deduped list at `outputs/all_unique_urls.txt`, public subset at `outputs/public_urls.txt`, walled/interactive subset at `outputs/walled_urls.txt`). Synthesis was done in three parallel passes — first half of the corpus, second half, and curated external-reference fetch — then merged. Every algorithmic and architectural claim in this plan is traceable to at least one corpus document; substantive claims with single-source provenance are flagged. Re-run `python src/rank_urls.py` to refresh citation-frequency rankings as the docs corpus grows.
