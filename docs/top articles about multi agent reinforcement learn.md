<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# top articles about multi agent reinforcement learning in 2025 sorted by month

The 2025 multi‑agent reinforcement learning (MARL) literature is already heavy on surveys, foundations, and LLM‑agent crossovers, but “top” is subjective and field‑specific. Below is a month‑ordered list of widely cited or thematically central MARL papers and surveys from 2025 so far, grouped by publication month and focused on general methods, theory, benchmarks, and real‑world applications rather than narrow domain one‑offs.

***

## February 2025

- **Multi-Agent Reinforcement Learning from Human Feedback (MARLHF)** – OpenReview (Feb 4, 2025)
    - Initiates a formal treatment of MARL from human feedback (MARLHF), defining the task as finding Nash equilibria using preference data instead of explicit reward functions.[^1]
    - Introduces temporal MSE regularization and pessimism penalties to stabilize reward learning and training in multi‑agent preference settings.[^1]

***

## April 2025

- **Meta-Thinking in LLMs via Multi-Agent Reinforcement Learning** – arXiv (Apr 19, 2025)
    - Proposes MARL as a framework for inducing **meta-thinking** capabilities in large language models, treating interacting LLM agents as cooperative or competitive learners.[^2]
    - Discusses how meta‑reasoning, self‑evaluation, and reflective planning can be framed as multi‑agent credit assignment and coordination problems.[^2]
- **Multi-Agent Reinforcement Learning for Resource Allocation** – arXiv (Apr 28, 2025)
    - Uses MARL to model distributed resource allocation, focusing on coordination among multiple decision‑makers under constraints.[^3]
    - Emphasizes scalability and decentralized learning for practical deployment in networked systems.[^3]

***

## May 2025

- **Resolving Conflicting Constraints in Multi-Agent Reinforcement Learning with Layered Safety** – arXiv (May 3, 2025)
    - Introduces a layered safety framework where MARL learns to minimize multi‑agent interactions that lead to constraint conflicts, with a safety filter providing tactical corrections.[^4]
    - Prioritizes agent pairs requiring urgent correction inside an engagement distance, combining learned strategies with rule‑based safety.[^4]
- **Hierarchical Frameworks for Scaling-up Multi-agent Coordination** – AAMAS 2025 Doctoral Consortium (May 19–23, 2025)
    - Studies hierarchical MARL for long‑horizon coordination, including complex tasks such as dual‑hand manipulation.[^5]
    - Explores integrating LLM‑based reasoning with MARL and evaluates limitations of state‑of‑the‑art algorithms on multi‑objective benchmarks like MOSMAC.[^5]
- **An Extended Benchmarking of Multi-Agent Reinforcement Learning in Fully Cooperative Tasks** – AAMAS 2025 (May 19–23, 2025)
    - Provides a broad benchmark suite for fully cooperative MARL, including sparse‑reward and image‑based high‑dimensional tasks.[^6]
    - Highlights overfitting and training‑time issues in current SOTA MARL methods and identifies tasks that remain unsolved by existing algorithms.[^6]

***

## June 2025

- **Multi-Agent Reinforcement Learning in Games** – (Games / systems review, June 5, 2025)
    - Systematically reviews MARL through value‑function decomposition, policy‑space design, and search mechanisms, linking them with game‑theoretic and bio‑inspired collective intelligence.[^7]
    - Targets applications from urban infrastructures to industrial cyber‑physical systems, emphasizing theoretical underpinnings and open challenges.[^7]

***

## July 2025

- **A Survey of Multi Agent Reinforcement Learning** – arXiv (Jul 7, 2025)
    - Comprehensive survey covering centralized, federated, decentralized, and non‑cooperative MARL under a unified view of interaction topologies.[^8][^9]
    - Reviews formal MDP formulations, representative algorithms, theoretical guarantees, and open problems in cooperation, communication, and strategic behavior.[^9][^8]
- **Real World Multi-Agent Reinforcement Learning: Latest Developments and Applications** – Vector Institute (Jul 27, 2025)
    - High‑level, practice‑oriented review of recent progress in sample‑efficient and scalable MARL for real‑world tasks like wildfire response, healthcare, and autonomous driving.[^10]
    - Focuses on how agents learn to collaborate and compete with diverse unseen agents in dynamic environments.[^10]
- **Multi-agent reinforcement learning for flexible shop scheduling** – Frontiers in Industrial Engineering (Jul 30, 2025)
    - Applies MARL to flexible job‑shop scheduling, emphasizing coordination, robustness, and integration with existing scheduling heuristics.[^11]
    - Situates MARL among other metaheuristics for multi‑objective scheduling and discusses industrial deployment considerations.[^11]

***

## August 2025

- **LLM Collaboration With Multi-Agent Reinforcement Learning (MAGRPO)** – arXiv (Aug 5, 2025)
    - Models collaboration among LLMs as a cooperative MARL problem and proposes Multi-Agent Group Relative Policy Optimization (MAGRPO).[^12]
    - Aims to replace complex per‑agent reward shaping with group‑based credit assignment tuned for multi‑turn, multi‑agent language interaction.[^12]

***

## September 2025

- **A Comprehensive Review of Multi-Agent Reinforcement Learning in Video Games** – arXiv (Sep 2, 2025)
    - Reviews MARL applications from two‑agent turn‑based games to large‑scale real‑time games such as StarCraft II, Dota 2, and Honor of Kings.[^13]
    - Analyzes core challenges—non‑stationarity, partial observability, sparse rewards, coordination, scalability—and proposes a method to estimate game complexity for MARL.[^13]

***

## Other 2025 survey‑style or adjacent works

- **A Survey of Cooperative Multi-agent Reinforcement Learning for Multi-task Scenarios** – Artificial Intelligence Science and Engineering (2025, volume 1(2))
    - Surveys cooperative MARL in multi‑task settings, covering algorithmic designs for sharing knowledge across tasks while preserving task‑specific performance.[^14]
- **Real‑world and domain‑specific applications**
    - Multiple domain papers (e.g., resource allocation, industrial scheduling, cyber‑physical systems) applying MARL appear throughout 2025; the ones above were chosen for breadth and methodological influence rather than a single domain focus.[^11][^7][^3]

***

If you want, the list can be reframed as a BibTeX bundle or filtered just to: (a) general surveys, (b) LLM‑agent + MARL work, or (c) benchmarks you can plug into your own multi‑agent platform.
<span style="display:none">[^15][^16][^17][^18][^19][^20]</span>

<div align="center">⁂</div>

[^1]: https://openreview.net/forum?id=4vPC6Aj6N7

[^2]: https://arxiv.org/abs/2504.14520

[^3]: https://arxiv.org/abs/2504.21048

[^4]: https://arxiv.org/abs/2505.02293

[^5]: https://www.ifaamas.org/Proceedings/aamas2025/pdfs/p2932.pdf

[^6]: https://www.ifaamas.org/Proceedings/aamas2025/pdfs/p1613.pdf

[^7]: https://pmc.ncbi.nlm.nih.gov/articles/PMC12190516/

[^8]: https://arxiv.org/pdf/2507.06278.pdf

[^9]: https://arxiv.org/abs/2507.06278

[^10]: https://vectorinstitute.ai/real-world-multi-agent-reinforcement-learning-latest-developments-and-applications/

[^11]: https://www.frontiersin.org/journals/industrial-engineering/articles/10.3389/fieng.2025.1611512/full

[^12]: https://arxiv.org/abs/2508.04652

[^13]: https://arxiv.org/abs/2509.03682

[^14]: https://ieeexplore.ieee.org/iel8/10899809/11077959/11077963.pdf

[^15]: https://arxiv.org/abs/2312.10256

[^16]: https://www.sciencedirect.com/science/article/pii/S2949855424000042

[^17]: https://dl.acm.org/doi/10.1613/JAIR.1.11396

[^18]: https://arxiv.org/list/cs.MA/2025-04

[^19]: https://github.com/xinzhel/LLM-Agent-Survey

[^20]: https://www.sciencedirect.com/topics/computer-science/multi-agent-reinforcement-learning

