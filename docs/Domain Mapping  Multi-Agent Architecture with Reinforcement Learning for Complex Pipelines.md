# Domain Mapping: Multi-Agent Architecture with Reinforcement Learning for Complex Pipelines

***

## Overview

Multi-Agent Reinforcement Learning (MARL) for complex pipelines represents the convergence of three major disciplines: **multi-agent systems theory**, **deep reinforcement learning**, and **agentic AI architecture**. In this paradigm, multiple autonomous agents — each with its own policy, observation space, and reward signal — operate within a shared environment to optimize a joint objective across an orchestrated pipeline of tasks. The field has exploded in relevance as LLM-based agentic frameworks (LangGraph, AutoGen, CrewAI) increasingly need principled training and optimization strategies for multi-step, multi-agent workflows.[^1][^2][^3][^4]

This domain map organizes the full knowledge landscape into foundational layers, algorithms, pipeline architectures, learning paradigms, tooling, benchmark environments, and frontier research — providing a practitioner's reference for building, training, and deploying MARL-powered complex pipelines.

***

## Domain Architecture Map

### Layer 0 — Mathematical & Theoretical Foundations

All MARL pipelines are formally grounded in **Stochastic Games** (a generalization of Markov Decision Processes for multiple agents):[^1]

- **Markov Decision Process (MDP):** A sequential decision problem defined by state space \( S \), action space \( A \), transition function \( P \), reward function \( R \), and discount factor \( \gamma \)[^5]
- **Stochastic Game (Markov Game):** A multi-agent MDP extended to \( N \) agents, each with individual action sets \( \mathcal{A}_i \) and reward functions \( R_i \), where joint actions determine transitions[^1]
- **Partially Observable Stochastic Game (POSG):** Each agent \( i \) receives an observation \( o_i \in \Omega_i \) rather than the full state — the standard model for real-world pipelines with information asymmetry[^3]
- **Dec-POMDP (Decentralized Partially Observable MDP):** A cooperative POSG in which all agents share a single team reward; the formal basis for centralized training with decentralized execution (CTDE)[^6][^3]
- **Nash Equilibrium:** A joint policy where no agent can improve its expected return by unilaterally deviating; the solution concept for competitive MARL[^1]
- **Game Theory Primitives:** Normal-form games, extensive-form games, cooperative coalitional games, mechanism design, and social welfare functions — all foundational to designing multi-agent reward structures[^7][^8]

***

### Layer 1 — Single-Agent RL Fundamentals (Prerequisite)

Before tackling MARL, practitioners must command single-agent RL building blocks:

| Concept | Description |
|---|---|
| **Bellman Equation** | Recursive value decomposition: \( V^\pi(s) = \mathbb{E}_\pi[r + \gamma V^\pi(s')] \) |
| **Q-Learning / DQN** | Value-based, off-policy; Deep Q-Network extended with replay buffers and target networks |
| **Policy Gradient (REINFORCE)** | Direct policy optimization via gradient ascent on expected return |
| **Actor-Critic (A2C, A3C)** | Hybrid architecture: policy actor + value critic reducing variance of PG[^5] |
| **PPO (Proximal Policy Optimization)** | Clipped surrogate objective for stable on-policy training; workhorse of modern RL |
| **SAC (Soft Actor-Critic)** | Off-policy, maximum entropy RL; excels in continuous action spaces |
| **TRPO** | Trust region policy updates with KL divergence constraint; precursor to PPO |
| **Model-Based RL** | Agent builds an internal world model to plan before acting |
| **Temporal Difference Learning** | TD(\( \lambda \)) bootstrapping; bridges Monte Carlo and DP methods[^5] |
| **Reward Shaping** | Intrinsic reward augmentation (curiosity, RND) to handle sparse rewards |

***

### Layer 2 — Core MARL Paradigms

MARL training paradigms define how agents share (or don't share) information during training and execution:[^3]

#### 2.1 Centralized Training, Decentralized Execution (CTDE)
The dominant paradigm: a centralized critic accesses global state during training but each agent executes using only local observations at deployment. Enables credit assignment with zero communication overhead at runtime.[^9]

#### 2.2 Decentralized Training, Decentralized Execution (DTDE)
Each agent trains independently — simplest to implement (Independent Q-Learning / IPPO) but suffers from non-stationarity as other agents' policies change simultaneously.[^3]

#### 2.3 Centralized Training, Centralized Execution (CTCE)
Full joint action space; only feasible for small agent counts due to exponential state-action growth. Used in simulation environments and AutoML pipeline synthesis.[^6]

#### 2.4 Hierarchical Reinforcement Learning (HRL)
Decomposes the decision problem into multiple abstraction levels: **high-level manager agents** set subgoals, **mid-level coordinators** route subtasks, and **low-level executor agents** take primitive actions. Represents the canonical architecture for orchestrated complex pipelines.[^10]

#### 2.5 Cooperative vs. Competitive vs. Mixed
- **Cooperative:** Shared team reward — all agents optimize collective outcome (search and rescue, warehouse automation)
- **Competitive:** Zero-sum reward — agents in direct opposition (adversarial security, market microstructure)
- **Mixed (General-Sum):** Independent rewards with partial alignment — closest to real-world enterprise pipelines[^11]

***

### Layer 3 — Key MARL Algorithms

| Algorithm | Category | Key Idea | Use Case |
|---|---|---|---|
| **IQL** (Independent Q-Learning) | DTDE Value | Each agent treats others as part of environment | Baseline; simple cooperative tasks |
| **VDN** (Value Decomposition Networks) | CTDE Value | Team Q = sum of individual Q-values | Cooperative tasks with additive structure |
| **QMIX** | CTDE Value | Monotonic mixing network for non-linear value factorization[^12] | StarCraft micromanagement, SMAC |
| **QPLEX** | CTDE Value | Duplex dueling factorization; provably expressive | High-complexity cooperative games |
| **MADDPG** | CTDE Actor-Critic | Centralized critic + individual actors for continuous actions[^13] | Robotics, continuous action MARL |
| **COMA** (Counterfactual Multi-Agent) | CTDE Actor-Critic | Counterfactual baseline for credit assignment | Differentiating individual contribution |
| **MAPPO** | CTDE Actor-Critic | Multi-agent PPO with global state critic; outperforms QMIX and MADDPG in most benchmarks[^14][^15] | Production MARL, pipeline optimization |
| **IPPO** | DTDE Actor-Critic | Independent PPO; surprisingly strong despite no centralization[^15] | Large-scale decentralized settings |
| **MAAC** | CTDE Actor-Critic | Attention mechanism over agent observations | Dynamic team composition |
| **RODE** | CTDE Value | Role-based agent decomposition | Task-specialized agent roles |
| **HARL** (Heterogeneous-Agent RL) | CTDE | Supports heterogeneous policy networks and action spaces | Mixed-capability agent teams |
| **DCPO** (Distributed Co-evolutionary Policy Optimization) | Hybrid | Evolutionary + policy gradient across distributed nodes[^16] | Large-scale pipeline training |

***

### Layer 4 — Pipeline Architectures for Complex Tasks

#### 4.1 Flat Multi-Agent Pipeline
All agents at the same level; typically cooperative and homogeneous. Suitable for parallelizable subtasks (map-reduce style agentic workflows).

#### 4.2 Hierarchical Pipeline (Manager-Worker)
Two or three tiers where high-level agents decompose objectives and pass subgoal instructions downward:[^10]
- **Tier 1 (Orchestrator/Planner):** Parses complex task instructions, generates a task dependency graph or action plan
- **Tier 2 (Coordinator):** Routes subtasks to specialized executors, manages inter-agent communication
- **Tier 3 (Executor/Motor Agents):** Interact directly with the environment; return observations and rewards upward

#### 4.3 Graph-Structured (DAG) Pipeline — Reinforcement Networks
The most general and expressive architecture: agents as vertices in a **Directed Acyclic Graph (DAG)**, with edges defining information flow. This extends hierarchical RL to arbitrary DAGs, enabling:[^17][^18]
- Flexible credit assignment across non-adjacent layers via skip-connections (bridged DAGs)
- Shared substructures and multi-parent agent relationships
- Parallelized inference via topological ordering
- Applications to LLM pipeline optimization, RAG systems, and AutoML[^18]

Each agent \( \omega_i \) is defined by the tuple \( \langle \mathcal{M}_i, \mathcal{O}^{-i}, \mathcal{A}_i, \mathcal{O}^{+i}, \pi_i, \phi_i, \psi_i, R_i \rangle \), where the communication function \( \phi_i \) propagates messages upstream and the proxy-reward function \( \psi_i \) enables hierarchical credit assignment.[^18]

#### 4.4 LLM + MARL Hybrid Pipeline
Emerging frontier: LLM planners handle task decomposition and reasoning while trained MARL policies manage real-time execution and coordination:[^2]
- **LGC-MARL:** LLM-based planner generates action dependency graphs; graph-based collaboration meta-policy uses meta-learning for rapid task adaptation[^2]
- **LangMARL:** Natural language-parameterized policies with centralized credit assignment enabling emergent role specialization without predefined roles[^19]
- **MAGRPO (Multi-Agent Group Relative Policy Optimization):** Extends GRPO to multi-agent LLM collaboration, optimizing writing and coding agent teams[^20]
- **MarsRL:** Joint optimization of all agents in a Solver → Verifier → Corrector pipeline via agentic pipeline parallelism

#### 4.5 RAG Pipeline Optimization via MARL
Complex RAG pipelines model each component (query rewriting, document retrieval, document filtering, answer generation) as an independent RL agent. **MMOA-RAG** treats the full RAG pipeline as a cooperative MARL task, achieving superior performance over supervised fine-tuning baselines.[^21]

#### 4.6 CI/CD and Operational Pipelines
RL applied to continuous integration pipelines: agents dynamically adjust test execution strategies as a Markov Decision Process to optimize throughput while maintaining quality thresholds.

***

### Layer 5 — Credit Assignment Problem

Credit assignment — attributing which agent's actions contributed to the team's reward — is MARL's central algorithmic challenge in complex pipelines:[^22]

- **Global Reward with Individual Agents:** Simple but inefficient — each agent cannot distinguish its contribution
- **Difference Rewards:** Each agent's reward = team reward minus reward without that agent (computationally intensive)
- **COMA Counterfactual Baseline:** Marginal contribution estimated by comparing actual action to a counterfactual average[^9]
- **Value Decomposition (VDN, QMIX, QPLEX):** Factorize global Q-value into per-agent contributions with structural constraints on mixing[^3]
- **Proxy Reward Functions:** In hierarchical architectures, lower-level agents receive proxy rewards from their supervisors rather than the terminal environment reward[^18]
- **Sparse Ablation Credit Approximation:** Approximate component-level credit using sparse ablations with historical reuse — improves interpretability and transfer readiness[^6]

***

### Layer 6 — Communication in MARL

| Protocol | Description | Key Paper |
|---|---|---|
| **No Communication** | Agents act on local observations only (DTDE/CTDE decentralized execution) | IQL, IPPO |
| **CommNet** | Continuous vector communication via learned communication channels | Sukhbaatar et al., 2016 |
| **DIAL / RIAL** | Differentiable inter-agent learning; gradients flow through communication channel | Foerster et al., 2016 |
| **ATOC** | Attention-based dynamic communication; agents selectively initiate communication | Jiang & Lu, 2018 |
| **Shared Memory (SRMT)** | Shared Recurrent Memory Transformer enables implicit information exchange across agents | Sagirova et al., 2025 |
| **Graph Attention** | Agents communicate via graph attention mechanism capturing interaction dependencies[^23] | MA-GA-DDPG |
| **Language-Based (LangMARL)** | Agents communicate via natural language, treated as textual gradients[^19] | LangMARL, 2025 |

***

### Layer 7 — Training Stability & Scalability Challenges

Complex pipelines amplify standard MARL pathologies:

- **Non-Stationarity:** As other agents' policies update, each agent's environment effectively changes; the Markov property breaks[^24][^22]
- **Exponential State-Action Space:** Joint action space grows as \( |\mathcal{A}|^N \) with \( N \) agents[^24]
- **Partial Observability:** Agents cannot observe the full pipeline state; Dec-POMDP formulation required[^9]
- **Multi-Time-Scale Learning:** Higher-level agents operate on slower timescales than executors; requires careful temporal abstraction in HRL[^18]
- **Pipeline Bubbles in RL Training:** Idle GPU time from mismatched rollout/training speeds — addressed by frameworks like SeamlessFlow via spatiotemporal multiplexing[^25]
- **Reward Sparsity in Long-Horizon Pipelines:** Terminal rewards arrive after many agent steps; intrinsic motivation and hierarchical reward shaping necessary
- **Sample Inefficiency:** Deep MARL is data-hungry; JaxMARL's GPU-accelerated pipeline achieves 12,500× speedup over conventional approaches[^26][^27]

***

## Benchmark Environments

| Environment | Type | Key Tasks | Framework |
|---|---|---|---|
| **SMAC / SMAX** | Cooperative | StarCraft II micromanagement | PyMARL, JaxMARL[^27] |
| **MPE (Multi-Agent Particle Envs)** | Mixed | Cooperative navigation, predator-prey | PettingZoo, MARLlib[^28] |
| **PettingZoo** | API Standard | 50+ MARL tasks: Atari, Butterfly, Classic, MPE, SISL[^29] | Farama Foundation |
| **MaMuJoCo** | Continuous Control | Multi-agent robotic locomotion | OpenAI Gym extension |
| **Overcooked** | Cooperative | Human-robot collaboration kitchen tasks | CarrollRLlib |
| **Hanabi** | Partial Info Cooperative | Card game requiring theory of mind | JaxMARL[^30] |
| **VMAS (Vectorized)** | Cooperative/Competitive | Physics-based multi-robot tasks | BenchMARL[^31] |
| **AI2-THOR** | Embodied AI | Complex household tasks, multi-room navigation | LGC-MARL evaluation[^2] |
| **AIME2025 / ProofNet** | Reasoning Pipeline | Mathematical theorem proving | MarsRL evaluation |

***

## Glossary

| Term | Definition |
|---|---|
| **Agent** | An entity embedded in an environment that observes state, takes actions, and receives rewards to maximize cumulative return[^5] |
| **Policy** \( \pi \) | A mapping from observations to a probability distribution over actions; the agent's decision function[^5] |
| **Value Function** \( V^\pi(s) \) | Expected cumulative discounted reward from state \( s \) under policy \( \pi \) |
| **Q-Function** \( Q^\pi(s,a) \) | Expected return after taking action \( a \) in state \( s \) under policy \( \pi \); action-value function |
| **Discount Factor** \( \gamma \) | Scalar \( \in [0,1) \) weighing future rewards; near 1 = far-sighted, near 0 = myopic[^5] |
| **Markov Decision Process (MDP)** | Formal model \( (S, A, P, R, \gamma) \) for sequential decision-making with the Markov property[^5] |
| **Dec-POMDP** | Decentralized partially observable MDP — cooperative MARL with shared reward and private observations; the formal basis for CTDE[^3] |
| **CTDE** | Centralized Training, Decentralized Execution — centralized critic during training, independent actors at deployment[^3] |
| **Joint Action** | Vector of all agents' simultaneous actions; defines multi-agent transition dynamics[^1] |
| **Nash Equilibrium** | Stable joint strategy where no agent improves by unilaterally changing its policy[^1] |
| **Value Decomposition** | Factorizing global team Q-value into per-agent components to enable credit assignment (VDN, QMIX)[^3] |
| **Actor-Critic** | Architecture where the actor learns a policy and the critic estimates the value function to reduce gradient variance[^5] |
| **PPO (Proximal Policy Optimization)** | On-policy gradient method with clipped surrogate objective for stable updates; basis of MAPPO[^14] |
| **MAPPO** | Multi-Agent PPO: centralized value critic with global state + independent PPO actors; state-of-the-art cooperative MARL[^15] |
| **QMIX** | Value decomposition algorithm using a monotonic mixing network combining individual Q-values into a joint Q[^12] |
| **MADDPG** | Multi-Agent Deep Deterministic Policy Gradient — centralized critic for continuous action multi-agent settings[^13] |
| **COMA** | Counterfactual Multi-Agent policy gradient — uses counterfactual baselines to assign credit to individual agents |
| **Intrinsic Motivation** | Reward bonus based on novelty, curiosity, or information gain to encourage exploration in sparse-reward environments |
| **Reward Shaping** | Augmenting the environment reward signal to accelerate learning and guide agent behavior |
| **Hierarchical RL (HRL)** | Multi-level RL where high-level policies set subgoals for lower-level policies to achieve[^32][^10] |
| **Option Framework** | Temporal abstraction in HRL: an option is a temporally extended action with initiation set, policy, and termination condition |
| **Non-Stationarity** | In MARL, as other agents update their policies, the environment appears non-stationary from each agent's perspective[^22] |
| **Credit Assignment** | Determining how much each individual agent contributed to the team's collective reward outcome[^22] |
| **Self-Play** | Training paradigm where agents compete/cooperate against copies of themselves; used in AlphaZero, OpenAI Five |
| **Emergent Behavior** | Complex coordination patterns arising from individual agent interactions without explicit programming[^11] |
| **Proxy Reward** | In hierarchical pipelines, a reward generated by a supervisor agent to guide lower-level agent training[^18] |
| **DAG (Directed Acyclic Graph)** | Graph structure for agent pipelines enabling flexible multi-parent hierarchies, parallelism, and skip-connections[^18] |
| **Communication Channel** | Learned or fixed protocol by which agents share information (vectors, attention weights, language tokens)[^33] |
| **POSG** | Partially Observable Stochastic Game — generalization of POMDP to \( N \) agents with individual observations[^1] |
| **Rollout** | A complete sequence of interactions between agents and environment to generate training data |
| **Off-Policy Learning** | Training on transitions collected by a different (older) policy, improving sample efficiency |
| **On-Policy Learning** | Training only on transitions collected by the current policy; more stable but less sample-efficient |
| **Curriculum Learning** | Progressive task difficulty scheduling to guide agent learning from simple to complex scenarios[^6] |
| **Meta-Learning (MAML)** | Learning to learn: adapting to new tasks rapidly from few examples; critical for pipeline generalization[^2] |
| **Transfer Learning in MARL** | Reusing policies or representations learned in one scenario to accelerate learning in new scenarios |
| **LLM Planner** | A large language model used as a high-level orchestrator that decomposes complex tasks into executable subtask graphs[^2] |
| **Graph-Based Collaboration Policy** | Agent communication and coordination modeled as graph neural networks over action dependency graphs[^2] |
| **Pipeline Bubble** | Idle GPU time caused by mismatched rollout/training throughput in distributed RL training[^25] |
| **RLHF** | Reinforcement Learning from Human Feedback — aligning agent behavior to human preferences via reward modeling |
| **GRPO** | Group Relative Policy Optimization — RL method for LLMs using relative reward within a group of responses[^20] |
| **Agentic RL** | RL applied to sequential, tool-using, multi-step LLM agent tasks with complex reward signals |

***

## Books

| Title | Authors | Level | Focus |
|---|---|---|---|
| **Reinforcement Learning: An Introduction** (2nd Ed., MIT Press, 2018) | Richard S. Sutton & Andrew G. Barto | Foundational | The canonical RL text; MDP theory, TD learning, policy gradients, function approximation[^34][^35] |
| **Multi-Agent Reinforcement Learning: Foundations and Modern Approaches** (MIT Press, 2024) | Stefano V. Albrecht, Filippos Christianos, Lukas Schäfer | Intermediate–Advanced | First comprehensive MARL textbook; game models, CTDE, deep MARL algorithms; free PDF + code at marl-book.com[^36][^37] |
| **Multiagent Systems: Algorithmic, Game-Theoretic, and Logical Foundations** (Cambridge, 2009) | Yoav Shoham & Kevin Leyton-Brown | Advanced | Game theory, mechanism design, auctions, distributed problem-solving; foundational for competitive MARL[^38][^39] |
| **Deep Reinforcement Learning Hands-On** (3rd Ed., Packt, 2024) | Maxim Lapan | Intermediate | DQN, PPO, DDPG, D4PG, AlphaGo Zero in PyTorch; practical implementations for pipelines[^40][^41] |
| **Mastering Multi-Agent Reinforcement Learning: From Foundations to Simulations** (2025) | (KDP) | Beginner–Intermediate | Accessible MARL with CTDE, reward shaping, reproducible workflows, and sim environments[^42] |
| **Designing Multi-Agent Systems** (O'Reilly, 2024) | Victor Dibia, PhD | Practitioner | Framework-agnostic; 6 orchestration patterns, agent UX, evaluation, RAI; build from scratch in Python[^43] |
| **An Introduction to Deep Reinforcement Learning** (arXiv/JMLR, 2018) | Francois-Lavet et al. | Introductory | Free survey textbook bridging single-agent DRL into practice[^44] |

***

## Courses

| Course | Institution / Platform | Level | Description |
|---|---|---|---|
| **Deep RL Course** | Hugging Face (free) | Beginner–Intermediate | Q-learning, deep Q-learning, policy gradients, multi-agent systems, RLHF, Decision Transformers; hands-on with HF Model Hub[^45] |
| **Reinforcement Learning Specialization** (4 courses) | University of Alberta / Coursera | Intermediate | Taught by Richard Sutton and Martha White; rigorous MDP theory, TD learning, function approximation; the gold standard RL curriculum[^46] |
| **MARL: Foundations and Modern Approaches** | IIIA-CSIC (YouTube, free) | Intermediate–Advanced | Full lecture series by Stefano V. Albrecht following the MIT Press textbook; covers CTDE, value decomposition, self-play[^47][^48] |
| **Deep Reinforcement Learning** (CS285) | UC Berkeley (free) | Advanced | Graduate-level course; model-based RL, policy gradients, meta-RL, offline RL, multi-agent extensions[^49] |
| **Spinning Up in Deep RL** | OpenAI (free) | Intermediate | Educational resource with curated paper list, standalone algorithm implementations (PPO, SAC, TD3), and exercises[^50][^51] |
| **Advanced Deep Learning & RL** | DeepMind / UCL (YouTube, free) | Advanced | 18-lecture series on modern DRL including multi-agent systems, AlphaGo architecture, and safe RL |
| **Practical RL** | Yandex School of Data Analysis (GitHub, free) | Intermediate | Hands-on notebooks from Q-learning to policy gradients and multi-agent environments |

***

## Technical Papers — Landmark & Frontier

### Foundational MARL
| Paper | Year | Key Contribution | Link |
|---|---|---|---|
| **QMIX** (Rashid et al.) | 2018 | Monotonic value function factorization for cooperative MARL; dominant benchmark result on StarCraft[^12] | arXiv:1803.11485 |
| **MADDPG** (Lowe et al.) | 2017 | Centralized critic for continuous-action multi-agent environments; canonical CTDE actor-critic | arXiv:1706.02275 |
| **MAPPO** (Yu et al.) | 2022 | Multi-agent PPO with global state critic; outperforms MADDPG and QMIX in most benchmarks[^15] | arXiv:2103.01955 |
| **COMA** (Foerster et al.) | 2018 | Counterfactual multi-agent policy gradients for credit assignment | arXiv:1705.08926 |
| **A Survey of MDRL** (Hernandez-Leal et al.) | 2019 | Comprehensive overview and critique of multiagent deep RL literature[^52] | arXiv:1810.05587 |
| **Cooperative MARL Introduction** (Amato) | 2024 | Tutorial covering CTE, CTDE, DTE settings; VDN, QMIX, QPLEX, MADDPG, MAPPO[^3] | arXiv:2405.06161 |

### Pipeline Architecture & Hierarchical MARL
| Paper | Year | Key Contribution | Link |
|---|---|---|---|
| **Reinforcement Networks** (ICLR 2026 submission) | 2025 | DAG-structured MARL framework unifying hierarchical, modular, and graph-structured MARL; skip-connections, proxy rewards[^18][^17] | OpenReview |
| **LGC-MARL** (Jia et al.) | 2025 | LLM planner + graph-based collaboration policy for complex task decomposition in AI2-THOR[^2] | arXiv:2503.10049 |
| **SeamlessFlow** | 2025 | Industrial RL framework eliminating pipeline bubbles via tag-scheduling and spatiotemporal multiplexing[^25] | arXiv:2508.11553 |
| **MarsRL** | 2025 | Joint MARL training for Solver-Verifier-Corrector agentic reasoning pipelines | hf.co/papers/2511.11373 |
| **Agentic AI Architecture for RL Pipelines** | 2025 | Multi-agent LLM orchestration for RL lifecycle: file selection, detection, fix suggestion, code generation[^4] | University of Vienna |

### LLM + MARL Frontier
| Paper | Year | Key Contribution | Link |
|---|---|---|---|
| **LLM Collaboration with MARL** (Liu et al.) | 2025 | MAGRPO: multi-agent group relative policy optimization for LLM writing/coding collaboration[^20] | arXiv:2508.04652 |
| **LangMARL** | 2025 | Natural language-parameterized policies with centralized credit assignment; emergent role specialization[^19] | arXiv:2604.00722 |
| **Chain-of-Agents** | 2025 | End-to-end agent foundation models via multi-agent distillation + agentic RL | hf.co/papers/2508.13167 |
| **MMOA-RAG** | 2025 | MARL-based joint optimization of all RAG pipeline components (retrieval, filtering, generation)[^21] | NeurIPS 2025; hf.co/papers/2501.15228 |
| **Teacher-Student MARL for AutoML** (ICLR 2026) | 2025 | Asymmetric teacher-student Dec-POMDP for AutoML pipeline synthesis; counterfactual credit + curriculum[^6] | OpenReview |
| **BFS-Prover-V2** | 2025 | Multi-turn off-policy RL + planner-enhanced multi-agent search for LLM theorem proving; 95.08% on MiniF2F[^53] | arXiv:2509.06493 |
| **SRMT** | 2025 | Shared Recurrent Memory Transformer for implicit multi-agent information exchange in lifelong pathfinding | hf.co/papers/2501.13200 |

***

## Repositories & Frameworks

### Core MARL Frameworks

| Repository | Stars | Description | Link |
|---|---|---|---|
| **RLlib (Ray)** | 30k+ ⭐ | Production-grade, distributed RL; PyTorch/TF; single and multi-agent; cloud-ready[^54] | github.com/ray-project/ray |
| **JaxMARL** (FLAIROx) | ~800 ⭐ | GPU-accelerated MARL environments and algorithms in JAX; 12,500× faster training[^26][^27] | github.com/FLAIROx/JaxMARL |
| **PyMARL / EPyMARL** (WhiRL) | — | QMIX, COMA, VDN, IQL implementations; standard SMAC benchmark runner[^55] | github.com/oxwhirl/pymarl |
| **MARLlib** (Replicable-MARL) | — | Unified MARL library: 18 algorithms × 10 environments built on Ray/RLlib[^56][^57] | github.com/Replicable-MARL/MARLlib |
| **BenchMARL** (Facebook Research) | — | Standardized MARL benchmarking via TorchRL backend; one-line benchmark configuration[^31] | github.com/facebookresearch/BenchMARL |
| **PettingZoo** (Farama) | — | Python API standard for MARL; 50+ environments across Atari, MPE, Classic, Butterfly[^58][^29] | github.com/Farama-Foundation/PettingZoo |
| **OpenAI Baselines** | 14.4k+ ⭐ | PPO, DDPG, TRPO, A2C reference implementations; RL benchmarking standard[^54] | github.com/openai/baselines |
| **CleanRL** | 3.5k+ ⭐ | Single-file RL algorithm implementations; excellent for study and customization[^54] | github.com/vwxyzjn/cleanrl |
| **Spinning Up** (OpenAI) | — | Educational deep RL resource: curated papers, standalone PPO/SAC/TD3/DDPG implementations[^50][^51] | github.com/openai/spinningup |
| **MARL-tutorials** (CMU) | — | Step-by-step MARL tutorial notebooks covering game theory foundations through modern algorithms[^59] | github.com/pjschneiCMU/marl-tutorials |

### Paper Collections & Reading Lists

| Repository | Description | Link |
|---|---|---|
| **MARL-Papers** (LantaoYu) | Comprehensive paper list sorted by year; covers joint action, coordination, communication, MARL in LLMs[^60] | github.com/LantaoYu/MARL-Papers |
| **Paper-List-of-MARL** (cheryyunl) | Actively maintained MARL paper list since 2018; includes NeurIPS/ICML/ICLR spotlight papers[^33] | github.com/cheryyunl/Paper-List-of-MARL |
| **LLM-Agents-Papers** | Papers on LLM-based agents including multi-agent RAG, CRAT, multi-modal planning[^61] | github.com/AGI-Edgerunners/LLM-Agents-Papers |
| **awesome-deep-rl** (tigerneil) | 1.5k+ ⭐ curated list for deep RL including hierarchical, distributional, and multi-agent approaches[^62] | github.com/tigerneil/awesome-deep-rl |

### Domain-Specific MARL Applications

| Repository | Domain | Link |
|---|---|---|
| **JaxMARL-HFT** | High-frequency trading; GPU-accelerated 240× faster than CPU baselines[^63] | Available via ACM DL |
| **MARLEM** | Decentralized local energy markets; implicit cooperation in grid management[^64] | github.com/salazarna/marlem |
| **EM-MARL (UAV Wildlife)** | UAV coordination for wildlife protection with latent variable modeling[^65] | GitHub (paper arXiv:2509.02579) |
| **marl-book codebase** | Official implementations for Albrecht/Christianos/Schäfer MARL textbook[^36] | marl-book.com |

***

## Learning Roadmap

### Stage 1 — Foundations (4–6 weeks)
1. Complete **Sutton & Barto Ch. 1–9** (MDPs, TD, Q-learning, function approximation)[^34]
2. Implement **DQN, REINFORCE, Actor-Critic** in CleanRL or Spinning Up[^51]
3. Take the **HuggingFace Deep RL Course** Units 1–5[^45]
4. Set up **PettingZoo** — run IQL on Simple Spread[^29]

### Stage 2 — Core MARL (6–8 weeks)
1. Read **Albrecht et al. MARL textbook** Ch. 1–8; watch IIIA-CSIC lecture series[^36][^47]
2. Study the **Amato AAMAS 2025 tutorial** PDF (cooperative MARL survey)[^9]
3. Implement **QMIX and MAPPO** using EPyMARL on SMAC[^55][^15]
4. Run **BenchMARL** for standardized algorithm comparison[^31]

### Stage 3 — Pipeline Architecture (4–6 weeks)
1. Study **Hierarchical RL**: Feudal Networks, HIRO, Option-Critic architecture[^32]
2. Read **IBM hierarchical agents overview** and **Reinforcement Networks paper**[^10][^18]
3. Build a 2-tier pipeline: LLM orchestrator → RL executor agents using **LGC-MARL concepts**[^2]
4. Explore **JaxMARL** for high-throughput experimentation[^26]

### Stage 4 — Frontier: LLM + MARL (Ongoing)
1. Study **LangMARL** (language-parameterized policies) and **MAGRPO**[^20][^19]
2. Apply MARL to a domain pipeline: RAG optimization (MMOA-RAG), AutoML (teacher-student), or code repair[^21][^6]
3. Explore **MarsRL agentic pipeline parallelism** for reasoning system training
4. Follow the **MARL-Papers** repo for the latest NeurIPS/ICLR/ICML publications[^60]

***

## Applications in Complex Real-World Pipelines

| Domain | MARL Pattern | Notes |
|---|---|---|
| **LLM Agent Pipelines** | Hierarchical / DAG | Planner → coordinator → executor; LGC-MARL, Chain-of-Agents[^2] |
| **RAG Systems** | Cooperative flat | Each component = agent; joint optimization via MMOA-RAG[^21] |
| **Algorithmic Trading** | Cooperative + competitive | 3-layer LLM + MARL + DRL framework; 53.87% annualized return in validation[^66] |
| **AutoML Pipeline Synthesis** | Teacher-student Dec-POMDP | Asymmetric pedagogical control; adaptive threshold interventions[^6] |
| **Robotics / Autonomous Vehicles** | Cooperative CTDE | SMAC-style micromanagement; CAV intersection decision-making[^23] |
| **CI/CD Pipeline Optimization** | Single/multi-agent MDP | Dynamic test execution adjustment via RL for throughput vs. quality trade-off |
| **Cybersecurity** | Adversarial MARL | Self-supervised DRL agents for zero-day attack mitigation[^67] |
| **HOA / Property Management SaaS** | Hierarchical cooperative | Planner agent (task intake) → specialist agents (finance, maintenance, communications) → executor agents |
| **Energy Grid Management** | Decentralized cooperative | MARLEM implicit cooperation across distributed prosumer agents[^64] |

---

## References

1. [Multi-agent reinforcement learning - Wikipedia](https://en.wikipedia.org/wiki/Multi-agent_reinforcement_learning)

2. [Enhancing Multi-Agent Systems via Reinforcement Learning with LLM-based Planner and Graph-based Policy](https://www.arxiv.org/abs/2503.10049) - Multi-agent systems (MAS) have shown great potential in executing complex tasks, but coordination an...

3. [An Initial Introduction to Cooperative Multi-Agent Reinforcement ...](https://arxiv.org/abs/2405.06161) - Multi-agent reinforcement learning (MARL) has exploded in popularity in recent years. While numerous...

4. [[PDF] Agentic AI Architecture for Evaluating and Improving Reinforcement ...](https://eprints.cs.univie.ac.at/8686/1/Agentic_AI_Architecture_for_Evaluating_and_Improving_Reinforcement_Learning_Pipelines.pdf) - This paper introduces an Agentic AI architecture that utilizes multiple specialized LLM-based agents...

5. [Glossary of Terminology in Reinforcement Learning](https://all.cs.umass.edu/rlr/terms.html) - Glossary of Terminology in Reinforcement Learning · actor-critic · agent · average-reward methods · ...

6. [Teacher-Student Multi-Agent Reinforcement Learning Framework for...](https://openreview.net/forum?id=yhqCTAFy0O) - We present an asymmetric teacher--student multi-agent reinforcement learning framework for automated...

7. [[PDF] Multiagent Systems and Essentials of Game Theory - ACM SIGecom](https://www.sigecom.org/exchanges/volume_7/3/LEYTONBROWN.pdf) - The origin of Essentials of Game Theory is our much longer book, Multiagent. Systems: Algorithmic, G...

8. [Algorithmic, Game-Theoretic, and Logical Foundations | Guide books](https://dl.acm.org/doi/book/10.5555/1483085) - Multiagent systems: algorithmic, game-theoretic, and logical foundations by Y. Shoham and K. Leyton-...

9. [[PDF] Chris Amato and Frans Oliehoek](https://www.ccs.neu.edu/home/camato/publications/AAMAS-Tutorial-Amato-2025.pdf)

10. [What are Hierarchical AI Agents? - IBM](https://www.ibm.com/think/topics/hierarchical-ai-agents) - Hierarchical agents are artificial intelligence (AI) agents that work together in a tiered multi-age...

11. [Multi Agent Reinforcement Learning Marl - Lark](https://www.larksuite.com/en_us/topics/ai-glossary/multi-agent-reinforcement-learning-marl) - MARL refers to a cooperative learning framework where multiple agents make decisions in an environme...

12. [QMIX: Monotonic Value Function Factorisation for Deep Multi-Agent
  Reinforcement Learning](https://arxiv.org/pdf/1803.11485.pdf) - ...off-policy learning, and guarantees consistency between
the centralised and decentralised policie...

13. [Experimental Evaluation of Coordinated Decision Making Strategies Based on Multi-Agent Reinforcement Learning](https://ieeexplore.ieee.org/document/11478990/) - Multi-agent systems are a major challenge when it comes to coordinated decision-making, mostly in th...

14. [Imitation Learning Strategies for Success in Multiagent ...](https://proceedings.neurips.cc/paper_files/paper/2024/file/99d7a578d72ed133203d1f88c9d39044-Paper-Conference.pdf)

15. [The Surprising Effectiveness of MAPPO in Cooperative, Multi-Agent Games](https://nicsefc.ee.tsinghua.edu.cn/%2Fnics_file%2Fpdf%2Fpublications%2F2021%2Farxiv_None_MJIGnPO.pdf)

16. [DISTRIBUTED EVOLUTIONARY POLICY OPTIMIZATION FOR EFFICIENT TRAINING OF MULTI-AGENT REASONING MODELS](https://ictactjournals.in/IJSC/ArticleDetails?id=21209) - Multi-Agent Reinforcement Learning (MARL) has emerged as a key paradigm for solving complex real-wor...

17. [MULTI-AGENT REINFORCEMENT LEARNING TASKS.](https://openreview.net/pdf?id=kpFdKCMt59)

18. [[Papierüberprüfung] Reinforcement Networks: novel framework for ...](https://www.themoonlight.io/de/review/reinforcement-networks-novel-framework-for-collaborative-multi-agent-reinforcement-learning-tasks) - The paper introduces **Reinforcement Networks**, a novel and general framework for collaborative Mul...

19. [LangMARL: Natural Language Multi-Agent Reinforcement Learning](https://arxiv.org/pdf/2604.00722.pdf)

20. [LLM Collaboration With Multi-Agent Reinforcement Learning - arXiv](https://arxiv.org/html/2508.04652v1) - A large amount of work has been done in Multi-Agent Systems (MAS) for modeling and solving problems ...

21. [Improving Retrieval-Augmented Generation through Multi-Agent ...](https://neurips.cc/virtual/2025/poster/119552) - Specifically, we present MMOA-RAG2, Multi-Module joint Optimization Algorithm for RAG, which employs...

22. [Multi-Agent Reinforcement Learning: A Review of Challenges and Applications](https://www.mdpi.com/2076-3417/11/11/4948/pdf) - In this review, we present an analysis of the most used multi-agent reinforcement learning algorithm...

23. [Cooperative Decision-Making for CAVs at Unsignalized Intersections: A
  MARL Approach with Attention and Hierarchical Game Priors](https://arxiv.org/html/2409.05712v1) - ...Attention Deep Deterministic Policy Gradient (MA-GA-DDPG), is
proposed to address these limitatio...

24. [Combining Planning and Reinforcement Learning for Solving Relational
  Multiagent Domains](https://arxiv.org/html/2502.19297v1) - Multiagent Reinforcement Learning (MARL) poses significant challenges due to
the exponential growth ...

25. [SeamlessFlow: A Trainer Agent Isolation RL Framework Achieving Bubble-Free Pipelines via Tag Scheduling](https://arxiv.org/abs/2508.11553) - We introduce SeamlessFlow, a server based reinforcement learning (RL) framework that addresses two c...

26. [JaxMARL: Multi-Agent RL Environments and Algorithms in JAX - arXiv](https://arxiv.org/html/2311.10090v4) - This is particularly useful for multi-agent reinforcement learning (MARL) research. First of all, mu...

27. [JaxMARL: Multi-Agent RL Environments and Algorithms in JAX](https://neurips.cc/virtual/2024/poster/97649) - The code is available at https://github.com/flairox/jaxmarl. Show more ... Multi-Agent Reinforcement...

28. [An Extended Benchmarking of Multi-Agent Reinforcement Learning ...](https://arxiv.org/html/2502.04773v1) - PettingZoo Terry et al. (2021) is a Python library consisting of several MARL tasks. In our benchmar...

29. [GitHub - Farama-Foundation/PettingZoo: An API standard for multi ...](https://github.com/Farama-Foundation/PettingZoo) - PettingZoo is a Python library for conducting research in multi-agent reinforcement learning, akin t...

30. [JaxMARL: Multi-Agent RL environments and algorithms in JAX](https://blog.foersterlab.com/jaxmarl/) - We present JaxMARL, a library of multi-agent reinforcement learning (MARL) environments and algorith...

31. [BenchMARL: Benchmarking Multi-Agent Reinforcement Learning](https://arxiv.org/abs/2312.01472) - The field of Multi-Agent Reinforcement Learning (MARL) is currently facing a reproducibility crisis....

32. [Agentic AI with Hierarchical Reinforcement Learning - YouTube](https://www.youtube.com/watch?v=hLl2D51QJb4) - This presentation will explore hierarchical reinforcement learning (HRL) as one of the most popular ...

33. [cheryyunl/Paper-List-of-MARL: A new paper list for multi ... - GitHub](https://github.com/cheryyunl/Paper-List-of-MARL) - A new paper list for multi-agent reinforcement learning (actively maintained), collecting papers sin...

34. [Reinforcement learning: an introduction](https://bibbase.org/network/publication/sutton-barto-reinforcementlearninganintroduction-2018) - The easiest way to keep your publications page up to date

35. [Reinforcement Learning](https://books.google.com/books/about/Reinforcement_Learning.html?id=CAFR6IBF4xYC) - Richard Sutton and Andrew Barto provide a clear and simple account of the key ideas and algorithms o...

36. [Multi-Agent Reinforcement Learning: Foundations and Modern ...](https://www.marl-book.com) - The book comes with a codebase written in the Python programming language, which contains implementa...

37. [Multi-Agent Reinforcement Learning: Foundations and Modern ...](https://www.goodreads.com/en/book/show/210099696-multi-agent-reinforcement-learning) - This text provides a lucid and rigorous introduction to the models, solution concepts, algorithmic i...

38. [[PDF] Multiagent Systems: Algorithmic, Game-Theoretic, and Logical ...](https://jmvidal.cse.sc.edu/library/shoham09a.pdf) - Page 1. MULTIAGENT SYSTEMS. Algorithmic, Game-Theoretic, and Logical Foundations. Yoav Shoham. Stanf...

39. [Multiagent Systems: Algorithmic, Game-Theoretic, and Logical ...](https://www.goodreads.com/book/show/5241622-multiagent-systems) - This exciting and pioneering new overview of multiagent systems, which are online systems composed o...

40. [Deep Reinforcement Learning Hands-On [Book] - O'Reilly](https://www.oreilly.com/library/view/deep-reinforcement-learning/9781788834247/) - Develop agents that solve Atari arcade and board games like Connect4 through self-learning. Explore ...

41. [PacktPublishing/Deep-Reinforcement-Learning-Hands-On-Third ...](https://github.com/PacktPublishing/Deep-Reinforcement-Learning-Hands-On-Third-Edition) - This is the code repository for Deep Reinforcement Learning Hands-On, Third Edition, published by Pa...

42. [Mastering Multi-Agent Reinforcement Learning](https://books.google.com/books/about/Mastering_Multi_Agent_Reinforcement_Lear.html?id=VeKO0QEACAAJ) - Mastering Multi-Agent Reinforcement Learning: From Foundations to SimulationsFeeling curious about A...

43. [4 AI Agent Books for 2025: Designing, Patterns, and LLMs - LinkedIn](https://www.linkedin.com/posts/dibiavictor_4-books-to-learn-ai-agents-in-2025-and-activity-7402782290654748673-x-Zi) - 4 books to learn AI agents in 2025 (and what each one is best for) I spent two years writing the Des...

44. [[PDF] An Introduction to Deep Reinforcement Learning - arXiv](https://arxiv.org/pdf/1811.12560.pdf) - ABSTRACT. Deep reinforcement learning is the combination of reinforce- ment learning (RL) and deep l...

45. [5 Free Courses on Reinforcement Learning](https://machinelearningmastery.com/5-free-courses-on-reinforcement-learning/) - Reinforcement learning (RL) is a subfield of machine learning where an agent learns to make decision...

46. [Top 5 Reinforcement Learning Courses in 2025 - GoCodeo](https://www.gocodeo.com/post/top-5-reinforcement-learning-courses-in-2025-learn-from-basics-to-advanced-practice) - Master reinforcement learning in 2025 with top developer-focused courses, build, train, and deploy r...

47. [SESSION 1 | Multi-Agent Reinforcement Learning: Foundations and Modern Approaches | IIIA-CSIC Course](https://www.youtube.com/watch?v=QfYx5q0Q75M) - 🔵 This course was given by Stefano V. Albrecht and has been organised by the Artificial Intelligence...

48. [Multi-Agent Reinforcement Learning - IIIA-CSIC](https://iiia.csic.es/en-us/marl-course/) - The IIIA is a research center of the CSIC, located on the Autonomous University of Barcelona, specia...

49. [Getting started: OpenAI Spinning Up vs Coursera RL Specialisation?](https://www.reddit.com/r/reinforcementlearning/comments/18la1ah/getting_started_openai_spinning_up_vs_coursera_rl/) - It makes for great reference, especially for implementations, but it's probably not going to do a go...

50. [Spinning Up in Deep RL - OpenAI](https://openai.com/index/spinning-up-in-deep-rl/) - We're releasing Spinning Up in Deep RL, an educational resource designed to let anyone learn to beco...

51. [openai/spinningup: An educational resource to help anyone learn ...](https://github.com/openai/spinningup) - Welcome to Spinning Up in Deep RL! This is an educational resource produced by OpenAI that makes it ...

52. [A Survey and Critique of Multiagent Deep Reinforcement Learning](http://arxiv.org/pdf/1810.05587.pdf) - .... Recent works have explored learning beyond single-agent scenarios and
have considered multiagen...

53. [Scaling up Multi-Turn Off-Policy RL and Multi-Agent Tree Search for LLM Step-Provers](https://arxiv.org/abs/2509.06493) - The integration of Large Language Models (LLMs) into automated theorem proving has shown immense pro...

54. [Best GitHub repositories for reinforcement learning - Top 2% Scientists](https://top2percentscientists.com/best-github-repositories-for-reinforcement-learning/) - 1. OpenAI Baselines · 14.4k+ | · TensorFlow. Best For: Benchmarking standard RL algorithms ; 2. Dopa...

55. [oxwhirl/pymarl: Python Multi-Agent Reinforcement ...](https://github.com/oxwhirl/pymarl) - Python Multi-Agent Reinforcement Learning framework - oxwhirl/pymarl

56. [Framework — MARLlib v1.0.0 documentation](https://marllib.readthedocs.io/en/latest/handbook/architecture.html) - MARLlib is a software library designed to facilitate the development and evaluation of multi-agent r...

57. [MARLlib: A Scalable and Efficient Multi-agent Reinforcement Learning Library](https://www.semanticscholar.org/paper/85bab103e25fb48daadca3da183e51e27cb83de1) - A significant challenge facing researchers in the area of multi-agent reinforcement learning (MARL) ...

58. [PettingZoo Documentation](https://pettingzoo.farama.org/index.html) - PettingZoo is a simple, pythonic interface capable of representing general multi-agent reinforcement...

59. [pjschneiCMU/marl-tutorials: Multi-Agent Reinforcement Learning](https://github.com/pjschneiCMU/marl-tutorials) - This repository aims to provide tutorials on multi-agent reinforcement learning (MARL). Before divin...

60. [Paper list of multi-agent reinforcement learning (MARL) · GitHub](https://github.com/LantaoYu/MARL-Papers) - This is a collection of research and review papers of multi-agent reinforcement learning (MARL). The...

61. [AGI-Edgerunners/LLM-Agents-Papers - GitHub](https://github.com/AGI-Edgerunners/LLM-Agents-Papers) - A repo lists papers related to LLM based agent. Contribute to AGI-Edgerunners/LLM-Agents-Papers deve...

62. [multiagent-reinforcement-learning · GitHub Topics](https://github.com/topics/multiagent-reinforcement-learning?l=html&o=asc&s=updated) - A Differentiable Inference-Time World Model utilizing ZODIAC: a multi-agent framework that performs ...

63. [JaxMARL-HFT: GPU-Accelerated Large-Scale Multi-Agent Reinforcement Learning for High-Frequency Trading](https://dl.acm.org/doi/10.1145/3768292.3770416) - Agent-based modelling (ABM) approaches for high-frequency financial markets are difficult to calibra...

64. [MARLEM: A Multi-Agent Reinforcement Learning Simulation Framework for Implicit Cooperation in Decentralized Local Energy Markets](https://linkinghub.elsevier.com/retrieve/pii/S0306261926001984) - This paper introduces a novel, open-source MARL simulation framework for studying implicit cooperati...

65. [Latent Variable Modeling in Multi-Agent Reinforcement Learning via Expectation-Maximization for UAV-Based Wildlife Protection](https://arxiv.org/abs/2509.02579) - Protecting endangered wildlife from illegal poaching presents a critical challenge, particularly in ...

66. [Adaptive LLM-based multi-agent systems to enhance quantitative trading performance](https://peerj.com/articles/cs-3630) - Traditional quantitative trading approaches have limited capacity for synthesizing heterogeneous dat...

67. [Artificial Intelligence-Powered Cybersecurity Reinforcement Agents: Self-Supervised Deep Representation Learning Using High-Dimensional Real-Time Attack Mitigation Techniques](https://ieeexplore.ieee.org/document/11323852/) - The cyber-attack landscape has been magnified by the rapid expansion of IT infrastructures, highligh...

