# Reinforcement Learning — Research Landscape, Open Problems, and Opportunities

*Survey date: May 2026. Knowledge cutoff: Jan 2026, supplemented with current web sources.*

---

## TL;DR

RL has decisively re-entered the mainstream of AI through two channels: (1) **RLVR** (Reinforcement Learning with Verifiable Rewards) as the dominant post-training method for reasoning LLMs, and (2) **world-model-driven robotics** as the path to general-purpose embodied agents. Classical concerns — sample efficiency, distributional shift, scalability, multi-agent non-stationarity — are not solved; they have been *reframed* by foundation models. The biggest contested question of 2025–2026 is whether RLVR genuinely expands reasoning capacity or merely sharpens sampling from priors already in the base model. This is unsettled and the field is splitting into camps.

---

## 1. State of the Art (2025–2026)

### 1.1 RL for LLM reasoning — the RLVR era

Since DeepSeek-R1 (Guo et al., 2025) demonstrated that rule-based binary rewards on math and code could induce long chain-of-thought reasoning without explicit CoT supervision, **RLVR has eclipsed RLHF as the active research frontier** for post-training. Key developments:

- **GRPO** (Group-Relative Policy Optimization, Shao et al. 2024) eliminated the critic from PPO by computing advantages over groups of rollouts. It is the de facto baseline.
- A wave of GRPO refinements through 2025–2026: **DAPO** (Yu et al. 2025), **Dr.GRPO** (Liu et al. 2025), **VAPO** (Yue et al. 2025), **GSPO** (Zheng et al. 2025), **CPG** (Chu et al. 2025) — each targeting different pathologies in the loss (length bias, credit assignment, exploration collapse).
- **LongRLVR** (2026) extends RLVR to long-context settings with verifiable context rewards.
- **RLVRR** (2026) generalizes RLVR to open-ended generation using reference-based rewards rather than exact-match verifiers.
- **Random Policy Valuation** (Sept 2025, arxiv 2509.24981) challenges the GPI paradigm itself, suggesting evaluation-only approaches can match policy iteration for LLM RL.
- **Safety analysis of RLVR** (Nov 2025, arxiv 2511.21050) — first formal bounds showing KL-constrained RLVR can preserve safety alignment under specific conditions. Important because most RLVR work has ignored safety drift.

**Enterprise framing**: RLVR is being marketed as the answer to enterprise hallucination concerns because verifier signals are deterministic, repeatable, and auditable — properties RLHF lacks.

### 1.2 World models + robotics

Deep RL combined with high-fidelity physics simulators ("metaverse" training) has crossed a deployment threshold. Robots are trained to convergence in simulation (millions of trials in hours) and the policy is transferred to physical hardware. General-purpose humanoid deployments in factories are now a reported reality, not a demo. The pattern is: goal-conditioned policy + world model + sim-to-real transfer, with VLM-style perception front-ends.

### 1.3 Scaling RL to very large / infinite-dimensional systems

Li & Zhang (JMLR, Dec 2025) introduced a hierarchical RL formulation specifically for infinite-dimensional systems, addressing the computational complexity wall classical RL hits at scale. This matters for control of distributed systems (grids, traffic, biological networks) where the state space is effectively continuous and unbounded.

### 1.4 Offline RL — maturity and consolidation

Offline RL spent 2020–2024 producing a sprawl of incompatible benchmarks and entangled algorithm designs. **"A Clean Slate for Offline Reinforcement Learning"** (Tarasov et al., NeurIPS 2025 oral) proposes a unified taxonomy and evaluation procedure to make results comparable. The core unsolved problem — distributional shift between behavior and learned policies — has not been cracked, but a comprehensive survey (Springer, March 2026) lays out the OOD generalization landscape clearly. Visual offline RL (offline RL from pixels) remains substantially harder than from proprioceptive state.

### 1.5 Multi-agent RL (MARL)

MARL is now being deployed in finance (market making at ICAIF '25), networked control, and traffic systems. The persistent concerns are non-stationarity (the environment changes as other agents learn), credit assignment in cooperative settings, and emergent collusion in competitive settings. The field has identified **trustworthy MARL** — provable safety, robustness, and generalization in multi-agent contexts — as the central problem for the next decade.

### 1.6 Hardware-native RL

UCLA's optical-computing PPO result (2026) is an early example of training directly on physical, non-differentiable hardware. This sidesteps the simulator-to-reality gap entirely and points toward an emerging subfield of RL on novel computing substrates.

---

## 2. What's Settled vs. Contested

### Settled (broad consensus)

- Deep RL with policy gradients (PPO and descendants) is the workhorse.
- For LLMs, group-relative advantage estimation (GRPO family) outperforms classical PPO in compute and stability.
- Pure online RL is impractical for high-stakes domains (healthcare, autonomous driving); offline or hybrid offline-online is required.
- World models + simulation are essential for data-hungry physical domains.
- Reward shaping is more art than science, and verifiable rewards (when available) dominate human-preference rewards on objective tasks.

### Contested / unresolved

- **Does RLVR genuinely expand reasoning, or just amplify capabilities already latent in the base model?** Yue et al. (2025) argue Pass@K does not improve under RLVR, suggesting it merely re-weights existing reasoning paths. Wen et al. (2025, "Implicitly Incentivizes Correct Reasoning") and Chen et al. (2025) push back with theoretical bounds and Pass@K improvements at large K. This is the most important open empirical question in the field.
- **Is GPI (generalized policy iteration) the right paradigm for LLM RL?** Random Policy Valuation results suggest it may not be.
- **Reward hacking and Goodhart effects under RLVR.** Verifiers are gameable. Open question how to make verifiers robust.
- **Sample efficiency in offline RL.** No method clearly dominates across the new clean-slate benchmarks.
- **Whether MARL collusion is a feature or a bug** in market-making contexts — this has regulatory implications.

---

## 3. Open Problems & Gaps

1. **Verifier design and robustness.** RLVR depends on cheap, accurate verifiers. Building these for non-mathematical domains (legal reasoning, medical diagnosis, design, strategy) is unsolved. LLM-as-judge approaches help but introduce their own biases.
2. **Credit assignment in long horizons.** GRPO assigns uniform credit across a rollout. For multi-step reasoning or agentic workflows, intra-trajectory credit assignment is largely unsolved.
3. **Safety-capability decoupling.** Most RL fine-tuning erodes safety properties. The Nov 2025 RLVR-safety paper is a starting point, not a solution.
4. **Sim-to-real gap.** World models are good but not perfect; transfer failure modes are still common in dexterous manipulation, deformable objects, and contact-rich tasks.
5. **Scalability of MARL.** Algorithms still degrade rapidly past ~100 agents. Decentralized + networked MARL is a partial answer but doesn't generalize.
6. **Distributional shift in offline RL** — fundamental, not yet cracked despite five years of focused work.
7. **Compute cost of RL post-training.** RLVR on frontier LLMs is wildly expensive. Resource-efficient RLVR (one-shot policy refinement, drafter models) is an active subfield.
8. **Continual / lifelong RL.** No production-grade method for agents that must keep learning safely after deployment.
9. **Theoretical foundations for deep RL** lag empirical practice substantially. This is true across the field and gets worse with LLM-RL.
10. **Evaluation.** Benchmarks for reasoning, agentic behavior, and MARL are weak, gameable, or both.

---

## 4. Opportunities

### Research opportunities

- **Verifier engineering as a discipline.** Anyone who can produce robust, gameable-resistant verifiers for new domains owns a research wedge.
- **RL for code modernization and software engineering tasks** — verifiers exist (tests pass / don't pass), the data is plentiful, and the economic value is clear. Largely under-explored vs. math reasoning.
- **Hybrid offline-online RL with foundation-model priors.** Foundation models provide a behavior prior; offline RL provides safety constraints; online interaction provides correction. The combination is barely explored.
- **MARL with learned communication protocols.** Most MARL assumes hand-designed communication. Letting agents learn protocols is wide open.
- **RL on novel hardware** (optical, neuromorphic, analog). The UCLA result is a proof of concept; the field is empty.
- **Causal RL.** Reasoning over interventions rather than correlations remains a niche area with high upside.

### Commercial opportunities

- **Vertical RLVR-as-a-service** for industries with verifiable correctness signals: tax, accounting, contract review, insurance claims, code review, regulatory compliance.
- **RL for trading infrastructure** — execution algorithms, market making, portfolio optimization. The MARL market-making paper is one indicator; the broader space is active and well-funded.
- **Embodied agent platforms.** Robotics foundation models built on world-model + RL stacks are an emerging category with several well-funded entrants.
- **Agent orchestration frameworks** that incorporate RL fine-tuning loops on top of LLM agents (rather than treating LLMs as fixed). This is currently a pain point in production agentic systems.
- **Continual-learning safety tooling** — monitoring, rollback, and verification for RL agents in production. Almost no commercial offerings exist.
- **Automated verifier synthesis** — tools that convert business rules into RLVR-compatible reward functions.

### Adjacent / blue-ocean

- **RL for AI infrastructure itself** — scheduling, autoscaling, GPU allocation, prompt routing. Cheap to instrument, high economic leverage.
- **RL for scientific discovery loops** — proposing experiments, refining hypotheses. Early but real.

---

## 5. Key References (selected)

- Sutton & Barto, *Reinforcement Learning: An Introduction*, 2nd ed. (foundational)
- Schulman et al. (2017), Proximal Policy Optimization
- Levine et al. (2020), *Offline RL: Tutorial, Review, and Perspectives* — arxiv 2005.01643
- Shao et al. (2024), Group-Relative Policy Optimization (GRPO)
- Guo et al. (2025), DeepSeek-R1
- Yue et al. (2025), Pass@K critique of RLVR
- Wen et al. (2025), RLVR Implicitly Incentivizes Correct Reasoning — arxiv 2506.14245
- Tarasov et al. (NeurIPS 2025), A Clean Slate for Offline RL
- Li & Zhang (JMLR Dec 2025), RL for infinite-dimensional systems
- ICAIF '25 paper on MARL market making — arxiv 2510.25929
- Distribution shift / OOD survey, *Neural Computing and Applications*, March 2026

---

## 6. Workflow Notes

This survey was generated from web search across recent academic and industry sources. It is not exhaustive. For deeper coverage of any single subarea (e.g., RLVR algorithms, MARL in finance, offline RL benchmarks), a follow-up pass with subarea-specific queries is warranted.
