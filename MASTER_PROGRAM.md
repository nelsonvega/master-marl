---
noteId: "bcd523b0459311f1b7f7e37a06f60118"
tags: []

---

# Master Program — Mastery Profile

**Topic**: Multi-Agent Reinforcement Learning for Algorithmic Trading
**Owner**: Nelson Vega (Kleio Technology)
**Generated**: 2026-05-01
**Source substrate**: 2,022 fetched resources in `downloads/` — 373 arxiv PDFs, 156 arxiv abstracts, 85 YouTube lecture transcripts, plus textbooks, course pages, and framework docs. Instantiated against the Mastery Profile template in `master-plan-agent.md`.

This document is the **learning roadmap and measurement system** that complements `MASTER_PLAN.md` (the codebase architecture). MASTER_PLAN.md says *what to build*; this says *how to actually become competent enough to build it*.

---

## 0. Calibration

| | |
|---|---|
| **Topic** | Multi-Agent Reinforcement Learning for Algorithmic Trading |
| **Domain** | Quantitative Finance ∩ Reinforcement Learning ∩ Distributed Systems |
| **Current Dreyfus Level** | Advanced Beginner (strong Python/systems, baseline ML, single-agent RL exposure, no MARL implementations) |
| **Prior knowledge** | Senior software engineering, SaaS/cloud-native, baseline statistics, comfortable with PyTorch concepts |
| **Time budget** | 10 hours/week sustained (≈ 130 hrs / 90 days) |
| **Target proficiency horizon** | 90 days to Proficient (Dreyfus 4); 6 months to Expert-light on chosen sub-domain |
| **Ultimate goal** | Ship a hierarchical MARL trading system into shadow mode, then advisory mode |
| **Constraints** | Self-directed (no formal instructor); needs research-grade depth; production-discipline bar |

---

## 1. Domain Map — Knowledge Components

The domain is a graph of **47 atomic Knowledge Components** across four types. Each has a target Bloom level, difficulty (1–5), dependency, and estimated time. Mastery requires KC coverage ≥ 95% at the listed thresholds.

### 1.1 Foundation layer — Single-agent RL (prerequisite)

| ID | KC | Type | Bloom | Diff | Depends on | Hours |
|---|---|---|---|---|---|---|
| F-01 | MDP formalism (states, actions, rewards, transitions, γ) | conceptual | Apply | 2 | — | 4 |
| F-02 | Bellman equation, value functions V(s), Q(s,a) | conceptual | Apply | 2 | F-01 | 5 |
| F-03 | Policy gradient theorem, REINFORCE | conceptual | Analyze | 3 | F-02 | 6 |
| F-04 | Actor-critic family (A2C, A3C) | procedural | Apply | 3 | F-03 | 6 |
| F-05 | DQN (deep Q-learning, replay buffer, target net) | procedural | Apply | 3 | F-02 | 8 |
| F-06 | PPO (clipped objective, GAE, importance ratio) | procedural | Analyze | 3 | F-03, F-04 | 10 |
| F-07 | SAC, TD3 (continuous control, off-policy) | procedural | Apply | 4 | F-04 | 6 |
| F-08 | Exploration vs exploitation; ε-greedy, entropy bonus | strategic | Evaluate | 2 | F-02 | 3 |
| F-09 | On-policy vs off-policy tradeoffs | strategic | Evaluate | 3 | F-04, F-05 | 3 |

### 1.2 Multi-agent core

| ID | KC | Type | Bloom | Diff | Depends on | Hours |
|---|---|---|---|---|---|---|
| M-01 | Markov Game / Stochastic Game formalism | conceptual | Apply | 3 | F-01 | 4 |
| M-02 | Dec-POMDP, POSG (partial observability formalism) | conceptual | Analyze | 4 | M-01 | 5 |
| M-03 | Nash equilibrium, dominant strategy, mixed strategy | conceptual | Apply | 3 | — | 5 |
| M-04 | Self-play and league training | strategic | Evaluate | 4 | M-01, M-03 | 4 |
| M-05 | Non-stationarity (the central MARL pathology) | conceptual | Evaluate | 4 | M-01 | 4 |
| M-06 | Credit assignment problem | conceptual | Evaluate | 4 | M-02 | 3 |
| M-07 | Centralized Training Decentralized Execution (CTDE) | strategic | Evaluate | 3 | M-02 | 4 |
| M-08 | IPPO / IQL (independent learners baseline) | procedural | Apply | 3 | F-05, F-06 | 6 |
| M-09 | MAPPO (centralized critic, parameter sharing) | procedural | Analyze | 4 | M-07, F-06 | 10 |
| M-10 | QMIX (monotonic value decomposition, IGM principle) | procedural | Analyze | 4 | M-07, F-05 | 10 |
| M-11 | MADDPG (continuous, mixed coop/competitive) | procedural | Apply | 4 | M-07, F-07 | 8 |
| M-12 | COMA (counterfactual baseline credit assignment) | procedural | Evaluate | 4 | M-06, M-07 | 4 |
| M-13 | Communication architectures (CommNet, ATOC, GNN) | procedural | Apply | 4 | M-09 | 6 |
| M-14 | Mean-field MARL (scaling to large agent counts) | conceptual | Understand | 4 | M-01 | 3 |
| M-15 | Hierarchical MARL (Manager-Worker, options framework) | strategic | Evaluate | 4 | M-09 | 6 |

### 1.3 Trading / market microstructure

| ID | KC | Type | Bloom | Diff | Depends on | Hours |
|---|---|---|---|---|---|---|
| T-01 | Limit Order Book mechanics, levels, microprice | conceptual | Apply | 3 | — | 4 |
| T-02 | Market microstructure models: Kyle, Glosten-Milgrom | conceptual | Analyze | 4 | T-01 | 5 |
| T-03 | Avellaneda-Stoikov inventory-aware market making | conceptual | Apply | 4 | T-01, T-02 | 5 |
| T-04 | Transaction cost models (linear, sqrt, Almgren-Chriss) | procedural | Apply | 3 | T-01 | 5 |
| T-05 | Risk-adjusted return metrics: Sharpe, Sortino, Calmar | conceptual | Apply | 2 | — | 3 |
| T-06 | Walk-forward & combinatorial purged cross-validation | procedural | Evaluate | 4 | T-05 | 6 |
| T-07 | Adversarial validation, leakage detection | procedural | Evaluate | 4 | T-06 | 4 |
| T-08 | Differential Sharpe and gameable reward pitfalls | strategic | Evaluate | 4 | T-05 | 3 |
| T-09 | Regime detection (trend / range / crisis labels) | procedural | Apply | 3 | T-05 | 4 |
| T-10 | Sim-to-real gap diagnosis for trading policies | strategic | Evaluate | 5 | T-04, T-06 | 5 |

### 1.4 MARL-for-trading integration (where the actual work lives)

| ID | KC | Type | Bloom | Diff | Depends on | Hours |
|---|---|---|---|---|---|---|
| I-01 | PettingZoo env API for trading (AEC vs Parallel) | procedural | Apply | 3 | M-09, T-01 | 6 |
| I-02 | Hierarchical agent topology (Orchestrator → Specialists) | strategic | Create | 5 | M-15, T-09 | 10 |
| I-03 | Multi-objective reward composition for trading | procedural | Create | 5 | T-05, T-08, M-09 | 8 |
| I-04 | Shielded action spaces (LTL constraints, risk overrides) | procedural | Evaluate | 5 | T-04, M-09 | 6 |
| I-05 | Cross-agent state and inventory observation design | procedural | Analyze | 4 | M-07, T-01 | 5 |
| I-06 | EPyMARL / MARLlib training pipeline configuration | procedural | Apply | 3 | M-09, M-10 | 6 |
| I-07 | Distributed training with Ray / Tune | procedural | Apply | 4 | I-06 | 5 |
| I-08 | Concept drift detection on policy entropy / reward dist | procedural | Evaluate | 4 | I-06, T-09 | 5 |
| I-09 | Shadow → advisory → autonomous deployment ladder | strategic | Create | 5 | I-04, T-10 | 6 |

### 1.5 Metacognitive KCs (often skipped, decisive at expert level)

| ID | KC | Type | Bloom | Diff | Depends on | Hours |
|---|---|---|---|---|---|---|
| X-01 | Reading + reproducing a research paper end-to-end | metacognitive | Create | 5 | F-06, M-09 | 15 |
| X-02 | Calibrated confidence in policy quality (predicted vs actual Sharpe) | metacognitive | Evaluate | 4 | T-06 | ongoing |
| X-03 | Recognizing overfitting patterns from training curves | metacognitive | Evaluate | 4 | F-06, T-06 | ongoing |
| X-04 | Diagnosing MARL training instability (5 failure modes) | metacognitive | Evaluate | 5 | M-09, M-10 | ongoing |

**Total estimated hours to Proficient**: ≈ 230 (compressible to 130–150 with focused, deliberate practice on the highest-leverage KCs). Hours-to-Expert: 800–1500.

### 1.6 Dependency graph (visual summary)

```
F-01 ─┬─ F-02 ─┬─ F-03 ─ F-04 ─┐
      │        └─ F-05 ────────┤
      │                        ├─ F-06 ─┐
      │                        ├─ F-07 ─┤
M-01 ─┼─ M-02 ─ M-07 ─┬────────┼────────┼─── M-08 (IPPO)
      │              ├────────┴────────┼─── M-09 (MAPPO)  ──┐
M-03 ─┘              ├─ M-10 (QMIX) ───┘                     │
                     ├─ M-11 (MADDPG)                        │
                     ├─ M-12 (COMA)                          │
T-01 ─ T-02 ─ T-03 ──┴──┐                                   │
T-04 ─ T-05 ─ T-06 ─ T-07 ─ T-08                            │
T-09 ─ T-10                                                  │
                                                             ▼
                                  I-01 → I-02 → I-03 → I-04 → I-09
                                              │
                                     I-05, I-06, I-07, I-08
                                              │
                                              ▼
                              X-01 ─ X-02 ─ X-03 ─ X-04
```

---

## 2. Mastery Definition

**Plain-language declaration**: "I am Proficient in MARL for algorithmic trading when I can independently design, implement, train, evaluate, and ship a hierarchical MARL trading policy from a research paper or a problem statement, defending every architectural choice from first principles, recognizing failure modes from training curves alone, and maintaining calibrated confidence about live performance vs backtest."

**Hard thresholds**:

| Criterion | Threshold |
|---|---|
| KC coverage at ≥ 0.85 mastery probability | ≥ 95% of required KCs |
| Average mastery probability across KCs | ≥ 0.85 |
| 30-day retention rate on core KCs | ≥ 85% |
| Application task count (full-implementation projects) | ≥ 5 |
| Transfer task count (novel-context applications) | ≥ 3 |
| Bloom level minimum for ≥ 60% of KCs | Evaluate or Create |
| Self-explanation quality on each landmark paper | ≥ 4/5 |
| Calibration error on Sharpe predictions | ≤ 0.10 |

**The four "you've made it" tests**:

1. Read a never-seen MARL paper from arxiv 2024+, summarize the contribution, identify which of the 4 MARL pathologies (M-05 non-stationarity, M-06 credit assignment, M-02 partial obs, scaling) it addresses, and reproduce its core experiment in ≤ 8 hours.
2. Take a single-agent FinRL strategy and convert it to a 3-agent hierarchical MAPPO setup with measurable improvement on out-of-sample Sharpe (transfer task).
3. Diagnose a failing MARL training run from W&B curves alone in < 30 minutes, naming the cause from a vocabulary of ≥ 8 distinct failure modes.
4. Defend your reward function against a hostile reviewer for 20 minutes covering: gameability, distributional shift under regime change, credit assignment, and out-of-sample drift.

---

## 3. Learning Path — Phase by Phase

Six phases, mapped to the M0–M6 milestones in `MASTER_PLAN.md`. Each phase has a single primary KC cluster, a capstone, and explicit exit criteria.

### Phase 0 — Orientation (Week 0; 5 hrs)

- **KCs targeted**: none new — domain mapping
- **Activities**: Skim Albrecht/Christianos/Schäfer Ch. 1 (`downloads/www.marl-book.com-index_*.html` and the textbook PDF). Watch the IIIA-CSIC MARL course intro (transcript already in `downloads/youtube.com-*.transcript.txt`). Walk the dependency graph in §1.6 above and locate which KCs you already partially own.
- **Exit criterion**: Self-rate every KC in §1 on a 1–5 scale; commit baseline to `research/curriculum/baseline_kc_vector.yml`.

### Phase 1 — Single-agent RL foundation (Weeks 1–4; 40 hrs)

- **KCs**: F-01 → F-09
- **Primary text**: Sutton & Barto, chapters 1–6 + 13 (`downloads/incompleteideas.net-book_the-book-2nd.html_*`).
- **Primary course (pick one, finish it)**: Berkeley CS285 (`downloads/rail.eecs.berkeley.edu-deeprlcourse_*`), Stanford CS234 lectures, or HuggingFace Deep RL Course (`downloads/huggingface.co-learn_deep-rl-course_*`).
- **Reproductions** (in `research/reproductions/single_agent/`):
  1. DQN on CartPole and LunarLander (target: within 5% of published returns)
  2. PPO on the same envs, plus Pendulum-v1
  3. SAC on a continuous control benchmark
- **Reference implementations**: CleanRL, Stable-Baselines3. Read source — do not just import.
- **Daily drill (15 min)**: spaced-repetition flashcards on F-01 to F-09 vocabulary (Bellman, GAE, importance ratio, entropy, advantage, etc.).
- **Capstone**: Single-agent PPO trader on a toy environment with 1 asset and synthetic returns. Walk-forward backtested.
- **Exit criteria**: F-01 to F-09 all at ≥ 0.80 mastery; CartPole + LunarLander reproductions checked into git; can explain GAE in 90 seconds without notes.

### Phase 2 — MARL core (Weeks 5–8; 40 hrs)

- **KCs**: M-01 → M-12
- **Primary text**: Albrecht/Christianos/Schäfer chapters 2–8 (`downloads/www.marl-book.com-*`).
- **Survey reading** (3 papers, in this order):
  1. Zhang/Yang/Başar 2019 survey — `downloads/arxiv.org-pdf_1911.10635.pdf_*`
  2. Huh/Mohapatra 2023 survey — `downloads/arxiv.org-abs_2312.10256_*`
  3. Yu et al. MAPPO paper + BAIR blog — `downloads/arxiv.org-pdf_2103.01955.pdf_*` and `downloads/bair.berkeley.edu-blog_2018_12_12_rllib_*`
- **Course**: IIIA-CSIC MARL course (Albrecht's free YouTube series — transcripts in `downloads/youtube.com-*.transcript.txt`).
- **Reproductions** on PettingZoo (`downloads/github.com-Farama-Foundation_PettingZoo_*`):
  1. IPPO on `simple_spread` (baseline)
  2. MAPPO on the same env (compare returns + sample efficiency)
  3. QMIX on a 4×4 SMAC scenario
  4. MADDPG on `simple_adversary`
- **Reference code to read** (these clarify what the textbooks gloss over):
  - `downloads/github.com-Lizhi-sjtu_MARL-code-pytorch_*` (compact PyTorch impls)
  - `downloads/github.com-uoe-agents_epymarl_*` (production patterns)
  - `downloads/github.com-oxwhirl_pymarl_*` (the original)
- **Capstone**: Port one MARL algorithm into a 2-agent toy market env (1 asset, parallel actors, no transaction cost).
- **Exit criteria**: M-01 to M-12 at ≥ 0.80; can explain on a whiteboard the difference between IPPO and MAPPO's centralized critic; PettingZoo reproductions are within 10% of published numbers.

### Phase 3 — Trading domain (Weeks 9–14; 40 hrs)

- **KCs**: T-01 → T-10
- **Primary texts**:
  - López de Prado, *Advances in Financial ML* (chapters 4–7 critical: walk-forward, purged CV, adversarial validation)
  - Lehalle & Laruelle, *Market Microstructure in Practice* (chapters on LOB and impact)
- **Course**: Stanford CME 241 (`downloads/cme241.github.io-index_*`) — RL applications in finance.
- **Anchor paper**: FinRL paper — `downloads/arxiv.org-pdf_2111.09395.pdf_*`. Read code: `downloads/github.com-AI4Finance-Foundation_FinRL_*`.
- **Reading list** (8 hrs total):
  - Avellaneda-Stoikov 2008 (market making) — search `downloads/` for the paper
  - Almgren-Chriss 2001 (execution costs)
  - Brock-Hommes (heterogeneous agent models) — agent-based modeling lineage
  - At least 5 trading-specific arxiv papers tagged in MASTER_PLAN.md as "domain anchors"
- **Build**:
  1. `app/slices/scanning` — historical data ingest + LOB feature engineering
  2. `app/slices/signals` — pattern detection (VWAP, breakout, regime label)
  3. Walk-forward backtesting harness (`research/notebooks/walk_forward.ipynb`)
  4. Transaction cost simulator with linear, sqrt, and Almgren-Chriss models
  5. Latency simulator (50 ms, 200 ms, 1 s injection)
- **Exit criteria**: T-01 to T-10 at ≥ 0.80; walk-forward harness is the single source of truth for any policy evaluation; can articulate three concrete ways differential Sharpe gets gamed.

### Phase 4 — MARL-for-trading integration (Weeks 15–20; 50 hrs)

- **KCs**: I-01 → I-09; revisit M-09, M-10, M-15 in trading context
- **The hard part**: this is where everything compounds. Allocate the most time here, not in the foundations.
- **Build**:
  1. Custom PettingZoo-compatible market env wrapping the LOB simulator (AEC mode for sequential agent decisions)
  2. Hierarchical agent topology in `app/slices/rl_policy`: Tier 1 Orchestrator + Tier 2 Coordinators (per regime) + Tier 3 Specialists (Scalper, Market-maker, Momentum, Hedger)
  3. Multi-objective reward composition: `R = w₁·return − w₂·downside_vol − w₃·tx_cost − w₄·inventory_var − w₅·drawdown + w₆·risk_adj_return`. Each weight justified in writing.
  4. Risk shield in `app/slices/risk` — formal-verification-style action filter with hard constraints (drawdown, position limits, leverage) the policy cannot override.
  5. EPyMARL training pipeline (`downloads/github.com-uoe-agents_epymarl_*`) producing trained policies; W&B logging on every run.
  6. Concept-drift detector on policy entropy + reward distribution KL.
- **Reading during build**:
  - MIXRTs paper for interpretability primitives — `downloads/arxiv.org-pdf_2209.07225.pdf_*`
  - Mavroudis et al. cybersecurity-MARL guidelines (transfer to trading) — `downloads/arxiv.org-pdf_2503.04262.pdf_*`
  - Localized policy iteration networked MARL — `downloads/arxiv.org-pdf_2211.17116.pdf_*`
- **Exit criteria**: I-01 to I-09 at ≥ 0.80; one full hierarchical MARL run end-to-end, walk-forward Sharpe > monolithic single-agent baseline; risk shield demonstrably blocks at least one synthetic adversarial action sequence.

### Phase 5 — Production discipline & shadow deployment (Weeks 21–26; 35 hrs)

- **KCs**: I-09, T-10, X-02, X-03, X-04
- **Build**:
  1. Promotion criteria YAML in `app/slices/rl_policy/promotion_criteria.yml`
  2. Audit-trail annotation: every order tagged with `(policy_version, signal_versions, observation_hash, risk_decision)`
  3. Kill-switch: drawdown > X bps in N min, fill ratio threshold, latency p99 threshold, action distribution KL threshold
  4. Broker API connector (Alpaca / IBKR) behind a feature flag, paper-trading account
  5. ≥ 4 weeks of shadow-mode operation, with daily comparison of policy intent vs market outcome
  6. Sign-off doc summarizing performance, deviations, and risk posture
- **Capstone**: Ship to advisory mode (orders to a UI for human approval) on at least one liquid asset.
- **Exit criteria**: shadow run completed with documented outcomes; calibration error on predicted Sharpe ≤ 0.10; postmortem written.

### Phase 6 — Transfer & extension (Weeks 27+; ongoing)

- **KCs**: X-01 deepening, frontier exploration
- **Activities**: paper reproduction cadence (one new MARL paper / month, log time + outcomes); contribute to one open-source MARL project; write up your hierarchical-agent topology as a blog post or tech report; mentor someone earlier in the path.
- **Frontier tracking**: quarterly review of the Berkeley MARL Seminar (`downloads/sites.google.com-*` for the seminar page) and Albrecht's IIIA-CSIC course updates.

---

## 4. KPIs and Measurement Plan

### 4.1 Quantitative KPIs (the dashboard)

| KPI | Tool / method | Frequency | Mastery target |
|---|---|---|---|
| KC Coverage % | Anki deck or `research/curriculum/kc_state.yml` | Weekly | ≥ 95% at 0.85 prob |
| Average Mastery Probability | Bayesian update from quiz performance | Weekly | ≥ 0.85 |
| 7-day Retention Rate | Spaced review (Anki / RemNote) | Continuous | ≥ 90% |
| 30-day Retention Rate | Spaced review | Continuous | ≥ 85% |
| First-attempt Success Rate | Novel paper-replication tasks | Per phase | ≥ 70% |
| Reproduction Sharpe vs Published | W&B comparison runs | Per reproduction | within 10% |
| Walk-forward Out-of-sample Sharpe | Custom backtester | Per policy version | track + improve |
| Training Stability (KL between consecutive policies) | W&B per-step logging | Per training run | < 0.05 typical |
| Policy Entropy Drift Detection Lag | Drift detector | Continuous | < 1 day after onset |

### 4.2 Qualitative mastery indicators (what mastery looks like for this topic)

- **Algorithm choice intuition**: Given a new MARL problem, you reach the right algorithm within 60 seconds (cooperative + discrete → QMIX; cooperative + general → MAPPO; mixed continuous → MADDPG; networked agents → localized policy iteration). No catalog scrolling.
- **Failure-mode pattern matching**: A training curve with collapse-then-spike behavior, you immediately suspect non-stationarity from concurrent policy updates and propose CTDE with shared critic; a flat reward curve, you suspect credit assignment and reach for COMA or value decomposition.
- **Reward design defensiveness**: Every reward weight in `I-03` you can name an attack against (gameability, regime drift, gradient explosion under tail volatility) and the mitigation.
- **Calibrated humility about backtest-to-live**: When asked "what Sharpe will this hit live?" you answer with a distribution and stress-test scenarios, not a number.
- **Vocabulary fluency**: You stop translating in your head between "POSG" and "decentralized partial-obs game" — they're the same primitive.

### 4.3 30 / 60 / 90-day checkpoint criteria

| Day | Must demonstrate |
|---|---|
| **30** | F-01 to F-09 + M-01 to M-07 at ≥ 0.80; DQN + PPO reproduced; can derive REINFORCE from scratch |
| **60** | M-08 to M-12 at ≥ 0.80; T-01 to T-08 at ≥ 0.70; MAPPO + QMIX reproduced; walk-forward harness running |
| **90** | I-01 to I-05 at ≥ 0.70; one custom market env in PettingZoo; one hierarchical MARL run trained end-to-end; shadow mode design documented |

---

## 5. OKRs — 90-Day Sprint

**Objective**: Reach Proficient-level mastery of MARL for algorithmic trading and ship one hierarchical MARL policy into shadow mode.

**Key Results** (each measurable, time-bounded):

- **KR1**: Achieve ≥ 0.80 mastery probability on 100% of foundation KCs (F-01 to F-09) and 100% of MARL-core KCs (M-01 to M-12) by day 60. *Measured*: weekly Anki review accuracy + reproduction success.
- **KR2**: Reproduce DQN + PPO + MAPPO + QMIX with returns within 10% of published results, all checked into `research/reproductions/` with W&B dashboards, by day 75.
- **KR3**: Score ≥ 4/5 on self-explanation quality for the 5 landmark papers (Sutton-Barto Ch. 1–6, MARL Book Ch. 1–8, MAPPO paper, FinRL paper, Zhang/Yang/Başar survey), evaluated by writing a 1500-word internal explainer for each that a non-specialist can follow.
- **KR4**: Ship one custom PettingZoo-compatible market env + one hierarchical MARL policy that beats a single-agent PPO baseline on out-of-sample walk-forward Sharpe by ≥ 0.20, by day 90.
- **KR5**: Apply MARL knowledge to one novel real-world problem outside the trading context (transfer task — see §8) before day 90.

**Review cadence**:
- **Daily** (15 min): spaced-repetition flashcards, self-rate KCs touched today
- **Weekly** (Sunday, 60 min): KC vector audit, OKR progress review, blocker triage
- **Monthly** (last Friday, 2 hr): application-project rubric scoring + 1500-word retro
- **90-day**: full transfer assessment + recalibration of next-quarter OKRs

---

## 6. Mental Models to Master First

The 7 frameworks that, once internalized, make every later concept faster to acquire. Each has a clear **misconception to unlearn** alongside.

| # | Model | Core insight | Misconception to actively unlearn |
|---|---|---|---|
| 1 | **MDP / Markov Game** as the primitive | Everything reduces to ⟨S, A, R, T, γ⟩; multi-agent just adds joint actions and per-agent reward | "RL is fundamentally different from supervised learning" — it's not, the loss function just samples its own data |
| 2 | **CTDE** | At training time you may use info no agent has at execution; this single trick unlocks half of modern MARL | "Decentralized = better" — pure independent learning has worse sample complexity and weaker coordination |
| 3 | **The four pathologies** (non-stationarity, credit assignment, partial obs, scaling) | Every MARL paper addresses one of these four; identify which before reading | "More agents = better" — coordination cost grows, emergent failure modes proliferate |
| 4 | **Bias-variance in policy gradients** | TRPO / PPO / SAC are bias-variance tradeoff knobs in disguise | "PPO is just a heuristic" — the clipping objective is principled and you should derive it once |
| 5 | **Backtest-to-live reality gap** | Out-of-sample Sharpe is an optimistic ceiling; live Sharpe is what counts | "Higher backtest Sharpe = better strategy" — the corpus repeatedly shows this destroys capital in production |
| 6 | **Reward as policy specification** | The reward function IS the spec; "the agent learned the wrong thing" almost always means the spec was wrong | "We just need more compute / more data / a bigger network" — usually the reward is gameable |
| 7 | **Sim-to-real as an explicit engineering problem** | Domain randomization, walk-forward validation, latency injection, adversarial training — all deliberate, not optional | "If it works in sim it'll work live" — the corpus's #1 documented disaster pattern |

These 7 are not optional. Master them BEFORE the algorithms. The algorithms come and go; these frameworks endure.

---

## 7. Deliberate Practice Plan

### 7.1 The 60-minute practice session (canonical structure)

| Minutes | Activity |
|---|---|
| 0–5 | Warm-up: spaced-repetition flashcards, ≤ 20 cards, on KCs touched in last 7 days |
| 5–15 | Active recall: write a 1-page explanation, from memory, of one KC at the edge of your competence (the stretch zone, Vygotsky ZPD) |
| 15–55 | The hard part: ONE focused attempt at a challenging problem — derive PPO from scratch, port a paper's algorithm, debug a stuck training run. Single-task, no email. |
| 55–60 | Reflection: write 3 sentences. What did I learn? Where did I get stuck? What's tomorrow's stretch problem? |

### 7.2 Targeted drills per KC cluster

| Cluster | Drill |
|---|---|
| Foundation (F-*) | Re-derive Bellman equation, REINFORCE, GAE, PPO clipped objective on paper. Once a week. |
| MARL core (M-*) | Implement IPPO / MAPPO / QMIX on toy envs without looking at reference code; compare to reference after. |
| Trading (T-*) | Write a transaction-cost-aware backtester from scratch. Then break it adversarially. |
| Integration (I-*) | Take a paper, give yourself 8 hours to reproduce its central experiment in your own codebase. Time-box ruthlessly. |
| Metacognitive (X-*) | Predict your reproduction's final Sharpe before it finishes. Track calibration error over 20+ runs. |

### 7.3 Spaced-repetition schedule for retention

Days **1, 3, 7, 14, 30, 60, 90, 180** for each KC. Card formats:

- **Vocabulary cards** (cheap, plentiful): "What is COMA's counterfactual baseline?"
- **Derivation cards** (harder, fewer): "Derive the policy gradient theorem in 5 lines."
- **Tradeoff cards** (strategic): "When do you reach for QMIX vs MAPPO?"
- **Failure-mode cards** (metacognitive): "What does a flat MARL training curve usually mean?"

Tooling: Anki or RemNote. Cards live in `research/curriculum/anki/`. Card count target: ~150 cards by day 90.

### 7.4 Feedback hierarchy you'll actually use

| Feedback type | Source | Frequency |
|---|---|---|
| Immediate automated | Reproduction return targets, test suites, type checker | Continuous |
| Self-feedback via reflection | Weekly retros + monthly 1500-word essays | Weekly + monthly |
| Peer feedback | One paper-discussion buddy + one MARL Discord/Slack | Bi-weekly |
| Expert feedback | Stefano Albrecht's office hours (IIIA-CSIC), MARL discord, paper-author email outreach | Monthly when stuck |
| Performance outcome | Live shadow-mode P&L vs backtest predictions | Daily once shipped |

---

## 8. Transfer Tasks (mastery confirmation)

Five tasks structurally different from anything in the training corpus. Each has scoring criteria. Hit ≥ 4/5 on all five → mastery declared.

### Task 1 — Reverse the domain (cybersecurity)

Apply your MARL trading skill to a cybersecurity problem: design a multi-agent defender vs attacker setup using the Mavroudis et al. guidelines (`downloads/arxiv.org-pdf_2503.04262.pdf_*`). Implement IPPO + MAPPO defenders against scripted attackers in NASim or similar. **Score**: 1 point each for environment design, agent topology, training run, written tradeoff analysis vs your trading version, working demo.

### Task 2 — Adjacent finance domain (portfolio rebalancing)

Take your hierarchical trading agents and reformulate them for **portfolio rebalancing across N correlated assets** (not single-asset trading). The shift forces explicit cross-asset coordination. **Score**: rubric on observation design, action space, reward composition, backtested Sharpe vs equal-weight baseline, written analysis of what transferred and what didn't.

### Task 3 — Adversarial paper review

Pick an arxiv MARL paper you haven't read, published 2025+. Write a 2000-word review identifying: (a) which of the four pathologies it addresses, (b) what's novel vs Yu/Rashid/Lowe baselines, (c) a concrete weakness or unsupported claim, (d) how you would extend it. **Score**: against a senior researcher's review (or submit to OpenReview).

### Task 4 — Teach it (the ultimate Bloom-Create test)

Give a 30-minute internal talk (recorded) covering: MAPPO's centralized critic, the credit assignment problem, and your hierarchical trading topology. Q&A ≥ 15 min. **Score**: rubric on accuracy, clarity, ability to handle hostile questions, depth of follow-up answers.

### Task 5 — Calibration audit

After 20+ training runs, compare your pre-run predicted Sharpe to actual achieved Sharpe. Compute mean absolute calibration error. **Score**: error ≤ 0.10 = pass; error ≤ 0.25 = developmentally acceptable; > 0.25 = you're not yet Proficient regardless of anything else.

---

## 9. Metacognitive Plan

### 9.1 Weekly self-reflection prompts (Sunday review)

Answer all five, in writing, every Sunday:

1. **What surprised me this week?** (Surprise = a model update; track these — they're the highest-yield learning moments.)
2. **What did I struggle with that I should have known?** (Catches gaps that the KC dashboard misses.)
3. **What did I learn that I'll forget without reinforcement?** (Add to Anki immediately.)
4. **What did I confidently get wrong?** (The most dangerous category — write the calibration correction explicitly.)
5. **What's the smallest experiment that would resolve my biggest open question?** (Forces concreteness.)

### 9.2 Calibration check (monthly)

For every prediction made in writing this month (Sharpe estimate, hyperparameter outcome, paper review verdict), record predicted vs actual. Track:

- **Brier score** for binary predictions
- **Mean absolute error** for continuous predictions
- **Hit rate within 1σ** for distributional predictions

If calibration is off, the fix is not "predict less" — it's "predict more, get more data, adjust priors". A non-predicting researcher does not improve.

### 9.3 Plateau diagnosis (the breakthrough protocol)

If your KC mastery curve flattens for ≥ 14 days:

1. **Difficulty calibration**: Are you in the comfort zone? Increase difficulty by 20%.
2. **Feedback latency**: Is feedback faster than 24 hours? If no, find a faster loop.
3. **Mental model gap**: Have you been Apply-level on something that needs Analyze? Re-read the source material with the goal of explaining, not consuming.
4. **Energy / sleep / focus audit**: Cognitive output ∝ sleep quality. No exceptions.
5. **Teach it**: Plateau breaks fast when you're forced to explain. Volunteer to give a 20-min talk in 7 days; you'll learn more in those 7 days than in the previous 30.

### 9.4 Signs you're plateauing (early indicators)

- Consuming content (papers, videos, blog posts) without producing anything of your own
- "Tool-chasing" — installing yet another framework instead of finishing the current one
- Reading at ≥ 1.5× speed (skimming as a defense)
- Predicting with low resolution ("about Sharpe 1.5") instead of high resolution ("Sharpe 1.43 ± 0.11 over 90-day OOS, conditional on no regime change")

---

## 10. Mastery Scorecard

Final dashboard. Score weekly; aim for ≥ 85% composite by day 90.

| Dimension | Weight | Day-0 baseline (your call) | Day-90 target | How measured |
|---|---|---|---|---|
| **KC Coverage** | 20% | _self-rate today_ | 100% of required KCs at ≥ 0.85 | Anki / quiz dashboard |
| **Retention Stability** | 20% | _baseline_ | ≥ 85% at 30-day recall | Spaced review accuracy |
| **Application Performance** | 25% | _baseline_ | ≥ 80% task success on novel reproduction | Per-phase capstone rubric |
| **Transfer Performance** | 20% | 0% | ≥ 70% on the 5 tasks in §8 | Per-task rubric |
| **Metacognitive Accuracy** | 15% | _baseline_ | Calibration error ≤ 0.10 | Predicted-vs-actual log |

**Overall Mastery Score** = `0.20·KC + 0.20·Retention + 0.25·Application + 0.20·Transfer + 0.15·Metacognition`

| Score range | Dreyfus level | Plain-language label |
|---|---|---|
| 0.50 – 0.65 | Advanced Beginner | Knows the vocabulary, can follow tutorials |
| 0.65 – 0.80 | Competent | Can build with guidance; predictions miscalibrated |
| 0.80 – 0.90 | Proficient | Can ship independently; calibrated; recognizes failure modes |
| 0.90 – 0.95 | Expert | Sets technical direction; teaches others; makes original contributions |
| ≥ 0.95 | Master | Generates novel knowledge; advances the field on a sub-domain |

**Mastery declaration condition**: Composite ≥ 0.85 AND each individual dimension ≥ 0.75 AND all 5 transfer tasks completed at ≥ 4/5 AND ≥ 4 weeks of shadow-mode operation in `app/`.

---

## Appendix A — Resource map (which downloaded file matches which KC)

A pointer index from KCs to the most relevant artifacts in `downloads/`. Not exhaustive — just the highest-signal anchor per KC.

| KC | Primary anchor |
|---|---|
| F-01..F-09 | `incompleteideas.net-book_the-book-2nd.html_*` (Sutton & Barto) + `rail.eecs.berkeley.edu-deeprlcourse_*` (Berkeley CS285) |
| M-01..M-07 | `www.marl-book.com-index_*` + `arxiv.org-pdf_1911.10635.pdf_*` (Zhang/Yang/Başar survey) |
| M-08, M-09 | `arxiv.org-pdf_2103.01955.pdf_*` (MAPPO) + `bair.berkeley.edu-blog_*mappo*` |
| M-10 | `github.com-oxwhirl_pymarl_*` (QMIX reference impl) |
| M-11 | `github.com-Lizhi-sjtu_MARL-code-pytorch_*` (MADDPG impl) |
| M-12 | search `downloads/` for "COMA" — the Foerster paper |
| M-13 | `arxiv.org-pdf_2312.08662.pdf_*` (TGCNet dynamic graph) + `arxiv.org-pdf_2408.07397.pdf_*` |
| T-01..T-04 | `databento.com-*` and Lehalle's textbook |
| T-05..T-08 | López de Prado (book; key chapter PDFs in `downloads/` if present) |
| T-10 | `arxiv.org-pdf_2503.04262.pdf_*` (Mavroudis cybersecurity guidelines — transfers to trading) |
| I-01..I-09 | FinRL paper `arxiv.org-pdf_2111.09395.pdf_*` + EPyMARL repo + your own `MASTER_PLAN.md` |
| X-01 | All 85 transcripts in `downloads/youtube.com-*.transcript.txt` — pick the IIIA-CSIC ones first |

---

## Appendix B — Anti-patterns specific to this topic

The corpus repeatedly flags these. Your KPI dashboard should explicitly red-flag them:

1. **Tutorial loop** — endless single-agent CartPole/PPO tutorials without ever advancing to MARL. *Symptom*: phase 1 lasts > 6 weeks. *Fix*: time-box phase 1 hard at 4 weeks.
2. **Algorithm zoo** — implementing every algorithm in MARL Book Ch. 5–8 before doing anything trading-specific. *Symptom*: phase 2 lasts > 8 weeks. *Fix*: pick MAPPO + QMIX, learn deeply, defer the rest until needed.
3. **Backtest worship** — reporting in-sample Sharpe with no walk-forward. *Symptom*: any number reported without OOS qualifier. *Fix*: walk-forward harness from week 9 onward, treat in-sample numbers as advisory only.
4. **Premature LLM agents** — switching from RL policies to LLM orchestration mid-program because LLMs feel hotter. *Symptom*: more time spent on LangGraph than MAPPO. *Fix*: LLM agents stay in `research/`, not `app/`, until phase 6.
5. **Metric mining** — adjusting reward weights until the backtest looks good. *Symptom*: more than 3 reward-weight changes per evaluation cycle. *Fix*: every weight change requires written justification + held-out window.

---

## Closing principle

Mastery is not a feeling. It is a **measurable composite score** across five dimensions, defended by transfer tasks, calibrated by tracked predictions, and demonstrated by a working policy in shadow mode. Everything in this document is in service of crossing the 0.85 line on that composite — not in service of feeling expert.

Start with the baseline KC self-rating (Phase 0). Then run the loop. The path is legible.
