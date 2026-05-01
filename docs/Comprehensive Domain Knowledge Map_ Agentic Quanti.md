<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Comprehensive Domain Knowledge Map: Agentic Quantitative Research

The emerging field of Agentic Quantitative Research represents a powerful convergence of artificial intelligence, computational economics, and quantitative finance. This domain synthesizes agent-based modeling, reinforcement learning, and multi-agent systems to understand and predict complex market behaviors that traditional equilibrium models often fail to capture. This comprehensive knowledge map provides a structured guide for researchers, practitioners, and students seeking to master this interdisciplinary field.[^1][^2][^3]

## Glossary \& Terminology

**Agentic AI/Systems**: Artificial intelligence systems designed to act autonomously on behalf of users to achieve specific goals, characterized by the ability to perceive, reason, act, and evaluate in an "observe-reason-act-evaluate" loop. Unlike traditional AI that responds to queries, agentic systems make decisions, execute multi-step workflows, and adapt to changing environments with minimal human intervention.[^4][^5][^6]

**Agent-Based Model (ABM)**: A computational model for simulating the actions and interactions of autonomous agents—both individual and collective entities—to assess their effects on the system as a whole. ABMs are particularly valuable in finance for modeling heterogeneous market participants whose interactions generate emergent macro-level phenomena.[^2][^7][^8][^9][^1]

**Reinforcement Learning (RL)**: A machine learning paradigm where an agent learns to make sequential decisions by interacting with an environment, receiving rewards or penalties, and iteratively refining its policy to maximize cumulative rewards. In financial contexts, RL agents learn optimal trading strategies through trial and error without relying on predefined rules.[^10][^11][^12][^13][^14]

**Multi-Agent Systems (MAS)**: Computational systems composed of multiple interacting intelligent agents that can negotiate, cooperate, or compete to solve problems that are beyond individual agents' capabilities. In finance, MAS models capture the complex dynamics arising from heterogeneous traders with different strategies and information sets.[^15][^16][^17][^18][^19]

**Quantitative Agent-Based Models**: ABMs that are matched to empirical data and designed to make quantitative forecasts or perform policy analysis, representing a shift from purely qualitative or theoretical agent-based models.[^20][^2]

**Heterogeneous Agents**: Market participants modeled with varying characteristics, beliefs, information sets, and decision-making rules, contrasting with the representative agent assumption of traditional economic models.[^3][^21][^22][^2]

**Bounded Rationality**: The concept that economic agents have limited computational capabilities and information, leading them to use heuristics and satisficing behaviors rather than perfect optimization.[^16][^21][^22]

**Emergent Behavior**: Complex macro-level patterns that arise from simple micro-level agent interactions, such as market bubbles, crashes, and volatility clustering.[^7][^23][^1]

**Adaptive Belief Systems (ABS)**: Economic models where agents are heterogeneous and switch between different trading strategies based on evolutionary fitness measures like accumulated past profits.[^21][^22]

**Deep Reinforcement Learning (DRL)**: The combination of deep neural networks with reinforcement learning, enabling agents to learn from high-dimensional state spaces and make complex sequential decisions.[^11][^12][^24][^10]

## Core Concepts \& Theories

### Agency Theory and Behavioral Extensions

Traditional agency theory examines the relationship between principals (shareholders) and agents (managers), focusing on how to align interests through monitoring and incentives. However, **Behavioral Agency Theory** extends this framework by incorporating psychological factors, cognitive biases, and emotional influences that shape managerial decision-making. This theory recognizes that managers exhibit loss aversion, vary in their risk perceptions based on reference points, and are influenced by organizational loyalty beyond pure financial incentives.[^25][^26][^27][^28]

The key departure from traditional agency theory lies in acknowledging that agents operate with bounded rationality, time-inconsistent preferences, and motivation beyond monetary compensation. This behavioral perspective is crucial for agentic quantitative research because it provides realistic microfoundations for modeling trader and institutional behavior in financial markets.[^26][^27][^25]

### Agent-Based Computational Economics (ACE)

Agent-based computational economics studies economic processes as dynamic systems of interacting agents, replacing the mathematical optimization assumption with agents exhibiting bounded rationality who adapt to market forces. ACE models employ numerical methods to simulate complex dynamics that resist analytical solutions, making them particularly suited for studying financial markets where traditional equilibrium assumptions break down.[^17][^29][^30][^16]

The Santa Fe Artificial Stock Market, pioneered by Arthur, Holland, LeBaron, Palmer, and Tayler, represents a landmark ACE application. This model demonstrated that heterogeneous agents using simple adaptive trading rules could generate realistic market phenomena including volatility clustering, fat-tailed return distributions, and excess trading volume—stylized facts absent from rational expectations models.[^31][^32][^33][^34]

### Heterogeneous Agent Models (HAMs)

Heterogeneous agent models, particularly those developed by Brock and Hommes, provide analytical frameworks for studying markets with diverse trader types. These models typically feature fundamentalists who trade based on asset valuations and chartists who extrapolate price trends. The key innovation is endogenous strategy switching based on evolutionary fitness measures: agents gravitate toward recently profitable strategies, creating nonlinear dynamics and enabling "rational routes to randomness".[^35][^36][^37][^38][^39][^22][^40][^21]

The Brock-Hommes framework demonstrates that even simple two-type heterogeneous agent models can generate complex dynamics including bifurcations, chaos, and multiple equilibria as the intensity of strategy switching increases. This work bridges theoretical economics and computational simulation, showing that bounded rationality and adaptive learning can explain market phenomena that rational expectations models cannot.[^39][^22][^40][^21]

### Reinforcement Learning in Finance

Reinforcement learning has emerged as a powerful approach for developing adaptive trading strategies. The Markov Decision Process (MDP) framework naturally aligns with sequential trading decisions: states capture market conditions, actions represent trading decisions (buy, sell, hold), and rewards reflect risk-adjusted returns like the Sharpe ratio.[^41][^12][^13][^14][^42][^10][^11]

Deep reinforcement learning algorithms—including Deep Q-Networks (DQN), Proximal Policy Optimization (PPO), and Actor-Critic methods—have demonstrated the ability to learn profitable strategies across multiple asset classes. The FinRL framework provides an open-source implementation specifically designed for quantitative finance applications. However, researchers must address challenges including reward function design, handling non-stationary market dynamics, and avoiding overfitting to historical data.[^12][^24][^43][^44][^14][^10][^11][^41]

### Behavioral Finance and Market Microstructure

Behavioral finance provides empirical foundations for agent-based models by documenting systematic deviations from rational behavior. Key findings include overconfidence, herding, disposition effects, and the use of heuristics for decision-making under uncertainty. Agent-based models explicitly incorporate these behavioral patterns, allowing researchers to study their aggregate market impact.[^36][^37][^35]

Market microstructure considerations—including order book dynamics, bid-ask spreads, liquidity provision, and price formation mechanisms—are essential for realistic agent-based market simulations. Models incorporating continuous double auction mechanisms and asynchronous event-driven trading can capture high-frequency market dynamics and flash crash scenarios.[^45][^46][^47][^48][^49][^15]

### Adaptive Markets Hypothesis

Andrew Lo's Adaptive Markets Hypothesis (AMH) reconciles efficient market theory with behavioral finance by applying evolutionary principles to financial interactions. The AMH posits that market efficiency is context-dependent and dynamic, varying with environmental factors like the number and diversity of market participants, the magnitude of profit opportunities, and participants' adaptability.[^50][^51][^52][^53]

This hypothesis provides theoretical grounding for agent-based models by suggesting that investors use heuristics adapted to their environment, learn from mistakes, and compete for survival in an ever-changing ecosystem. The AMH framework explains why markets can exhibit both efficient and inefficient periods, depending on ecological conditions.[^51][^52][^53][^50]

## Conceptual Connections: Agentic Models in Quantitative Research

### Integration of Reinforcement Learning and Agent-Based Modeling

The synthesis of reinforcement learning and agent-based modeling creates powerful frameworks for studying market dynamics. Individual agents employ RL algorithms to learn optimal strategies while interacting through an agent-based market simulation. This integration enables researchers to study:[^54][^55][^56][^14][^57][^47][^58][^10][^12]

- **Coevolutionary dynamics**: How learning agents adapt to each other's strategies, creating feedback loops and regime shifts[^59][^60][^61]
- **Strategy ecology**: The diversity and evolution of trading strategies in populations of learning agents[^62][^63][^59]
- **Systemic risk propagation**: How intelligent agents' coordinated responses to shocks amplify crises[^64][^15]

Multi-agent reinforcement learning (MARL) extends these frameworks by allowing heterogeneous agents to simultaneously learn in shared environments. Applications include modeling interbank lending networks, decentralized market coordination, and the impact of high-frequency trading algorithms.[^57][^18][^16][^17]

### Application to Algorithmic Trading

Agentic quantitative research directly addresses algorithmic trading challenges. RL-based trading agents can:[^56][^65][^66][^54][^10]

- **Execute optimal trades**: Learning to minimize market impact and transaction costs through techniques like Deep Q-Learning and policy gradient methods[^10][^11][^12]
- **Adapt to market regimes**: Automatically adjusting strategies as volatility, liquidity, and correlation structures shift[^67][^65][^56][^41]
- **Discover alpha**: Identifying profitable patterns in high-dimensional data including price, volume, sentiment, and alternative data sources[^65][^68][^54][^56]

The QuantConnect platform provides infrastructure for developing, backtesting, and deploying algorithmic trading strategies using Python and C\#. It offers extensive historical data, realistic transaction cost modeling, and integration with multiple brokerages for live trading.[^69][^70][^71]

### Economic Policy and Risk Management

Agent-based models serve as computational laboratories for evaluating economic policies and assessing systemic risks. The Office of Financial Research and central banks increasingly utilize ABMs to:[^61][^15][^2][^7]

- **Stress test financial systems**: Simulating cascading defaults, liquidity spirals, and fire sales under extreme scenarios[^49][^15][^64]
- **Design regulations**: Testing the impact of capital requirements, leverage limits, and circuit breakers on market stability[^1][^7]
- **Model monetary policy transmission**: Understanding how heterogeneous agents respond to interest rate changes and quantitative easing[^29][^72][^61]

Multi-agent models capture institutional heterogeneity (banks, hedge funds, pension funds) and network structures (interbank lending, repo markets) that traditional macro models aggregate away.[^17][^29][^64]

## Applications Across Domains

### Portfolio Optimization and Asset Management

Reinforcement learning offers novel approaches to dynamic portfolio optimization. RL agents learn to balance risk-return tradeoffs, rebalance portfolios in response to market signals, and incorporate transaction costs into decision-making. The framework naturally handles multi-period objectives and can optimize non-standard criteria like maximum drawdown or value-at-risk.[^73][^74][^75][^76]

Agent-based models complement these methods by simulating how portfolios perform under various market ecology scenarios, including stress periods when agent behavior shifts dramatically.[^77][^78][^1]

### High-Frequency Trading and Market Making

Agent-based models excel at studying high-frequency trading environments where strategic interactions occur at millisecond timescales. Researchers model diverse agent types including market makers providing liquidity, arbitrageurs exploiting mispricings, and directional traders. These simulations reveal:[^79][^46][^47][^80][^81][^45]

- **Optimal execution strategies**: How to split large orders to minimize market impact[^58][^82][^81]
- **Liquidity dynamics**: When and why liquidity suddenly evaporates during stress periods[^46][^49]
- **Flash crash mechanisms**: The role of feedback loops and coordination failures in rapid price crashes[^48][^46]


### Risk Management and Derivatives Pricing

Reinforcement learning applies to derivatives trading through dynamic hedging strategies. RL agents learn to rebalance hedge portfolios in response to changing market conditions, potentially outperforming traditional delta-hedging approaches. Agent-based models simulate counterparty risk, collateral dynamics, and the impact of margin requirements on derivatives markets.[^24][^13][^76][^15][^64]

### Alternative Data and Market Intelligence

Agentic AI systems are transforming how organizations process alternative data for market intelligence. Multi-agent frameworks can:[^83][^84]

- **Synthesize diverse information**: Combining news, social media sentiment, satellite imagery, and transaction data[^84][^68]
- **Generate proactive insights**: Identifying emerging trends and anomalies before they become widely recognized[^83][^84]
- **Answer complex questions**: Integrating quantitative and qualitative data to provide nuanced market assessments[^84][^83]


## Courses from Top Universities

### Massachusetts Institute of Technology (MIT)

MIT offers several relevant programs through MIT Sloan and the broader engineering school:

- **15.879: Agent-Based Modeling for Health Policy**: While focused on health applications, this course teaches fundamental ABM techniques using AnyLogic that transfer to financial modeling[^85]
- **Mathematical Methods for Quantitative Finance** (MITx online): Covers probability theory, stochastic calculus, and numerical methods essential for quantitative finance[^86][^87]
- **Finance MicroMasters Program**: A comprehensive online curriculum covering modern finance theory, analytics, and applications[^87]

MIT faculty including Andrew Lo have pioneered research on adaptive markets and computational finance, making it a leading institution for this field.[^88][^52][^53][^50]

### Stanford University

**CS224R: Deep Reinforcement Learning** (Spring 2025): This course provides comprehensive coverage of modern deep RL methods with applications to robotics and language modeling. Topics include policy gradients, actor-critic methods, offline RL, model-based RL, and meta-learning. The course structure includes lectures, programming assignments in PyTorch, and a research project.[^89][^90]

**CS234: Reinforcement Learning** (Winter 2025): An introductory course covering MDPs, temporal-difference learning, policy search, exploration, and applications. The curriculum specifically addresses offline RL and imitation learning, which are crucial for financial applications where interaction data is limited.[^91][^92]

**CME 241: Foundations of Reinforcement Learning with Applications in Finance**: This specialized course directly addresses RL applications in quantitative finance, covering Markov processes, dynamic programming, and financial trading problems.[^93][^94]

Stanford's Mathematical and Computational Finance program provides strong foundations in stochastic processes, numerical methods, and optimization relevant to agentic systems.[^95]

### Princeton University

**Operations Research and Financial Engineering (ORFE)**: Princeton's ORFE department offers one of the most prestigious programs in quantitative finance. The undergraduate and graduate curricula include:[^96][^97][^98][^99][^100]

- **ORF 309: Probability and Stochastic Systems**: Foundation in stochastic processes including Markov chains and Brownian motion[^96]
- **ORF 335: Financial Mathematics**: Arbitrage pricing, risk-neutral valuation, and derivatives modeling[^96]
- **ORF 311: Stochastic Optimization and Machine Learning in Finance**: Direct application of optimization and ML to financial problems[^96]
- **ORF 445: High Frequency Markets**: Analysis of high-frequency trading and market microstructure[^96]

Princeton faculty including Ronnie Sircar specialize in financial mathematics, stochastic volatility, and optimal control—all relevant to agentic quantitative research.[^96]

### University of Oxford

**MSc in Mathematical and Computational Finance**: This program is ranked \#1 in the UK for quantitative finance by QuantNet. The curriculum includes:[^101][^102][^103]

- **Core courses**: Stochastic calculus, financial derivatives, numerical methods, statistics, deep learning, and quantitative risk management[^102][^101]
- **Financial Computing**: Extensive training in C++ and Python implementation of quantitative models[^101][^102]
- **Electives**: Market microstructure and algorithmic trading, advanced Monte Carlo methods, decentralized finance[^102][^101]
- **Dissertation**: Research project potentially conducted alongside industry internship[^101][^102]

Oxford's Mathematical \& Computational Finance faculty represents the largest mathematical finance research group globally with 14 faculty members.[^103][^102]

### ETH Zurich and University of Zurich

**Master of Science in Quantitative Finance (MScQF)**: This joint program between ETH Zurich and University of Zurich is ranked \#2 in Europe and \#7 worldwide. The program offers:[^104][^105]

- Unique blend of economic theory, mathematical methods (probability, statistics, numerical analysis), and practical applications[^104]
- Courses taught by leading scholars and financial practitioners[^104]
- Coverage of recent FinTech developments[^104]
- Highly affordable tuition (~CHF 800 per semester) making elite quantitative finance education accessible[^104]


## Key Researchers \& Thought Leaders

**J. Doyne Farmer** (University of Oxford, Santa Fe Institute): Farmer is a pioneering figure in agent-based economics and complexity science applied to finance. His work on quantitative agent-based models demonstrates how ABMs can serve as empirical alternatives to traditional macroeconomic models. Farmer co-developed the Santa Fe Artificial Stock Market and continues advancing ABM methodology for economic forecasting and policy analysis.[^60][^106][^107][^32][^34][^2][^20][^61]

**Blake LeBaron** (Brandeis University): LeBaron is a leading expert in agent-based computational finance with extensive contributions to artificial financial markets. His seminal paper "Agent-Based Computational Finance" serves as a foundational guide for researchers building financial ABMs. LeBaron's work on the Santa Fe Artificial Stock Market demonstrated how heterogeneous learning agents could generate realistic market dynamics.[^108][^109][^110][^32][^33][^31]

**William Brock and Cars Hommes**: These economists developed influential heterogeneous agent models featuring endogenous strategy switching based on evolutionary fitness. Their work provides analytical foundations for understanding how boundedly rational agents create complex market dynamics through adaptive belief formation.[^38][^22][^40][^39][^21]

**W. Brian Arthur** (Santa Fe Institute): Arthur contributed to complexity economics and co-created the Santa Fe Artificial Stock Market. His work on increasing returns and path dependence provides theoretical foundations for understanding economic systems with positive feedback.[^32][^33][^34]

**Robert Axtell** (George Mason University): Axtell has advanced agent-based modeling methodology and applications to economics, particularly in understanding firm dynamics and innovation. His collaboration with Farmer produced a major review of ABM in economics and finance.[^20][^88]

**Andrew Lo** (MIT Sloan): Lo developed the Adaptive Markets Hypothesis, which provides evolutionary foundations for understanding financial market dynamics. His work bridges efficient market theory and behavioral finance through biological principles of competition, adaptation, and natural selection.[^52][^111][^112][^53][^50][^51]

**Richard Bookstaber** (Office of Financial Research): Bookstaber advocates for agent-based approaches to understanding financial crises and systemic risk. His book "The End of Theory" articulates why traditional equilibrium models fail to capture crisis dynamics and how ABMs offer superior alternatives.[^15][^88][^64]

**Leigh Tesfatsion** (Iowa State University): Tesfatsion has been instrumental in developing and promoting agent-based computational economics as a research methodology. Her educational resources on ACE provide comprehensive introductions to the field.[^113][^114]

**Thomas Starke**: As CEO of AAA Quants, Starke applies reinforcement learning to quantitative finance and actively educates the trading community through workshops and presentations.[^115][^116]

## Videos \& Playlists

### Academic Lectures and Courses

**CSSSA Webinar: "Agent-Based Modeling in Economics and Finance"** (2025): Robert Axtell and Doyne Farmer discuss past, present, and future of ABM in economics, covering methodology, applications, and the quantitative turn in agent-based modeling. The webinar addresses tractability advantages of ABM, handling complex nonlinear systems, and moving from qualitative to quantitative applications.[^72][^20]

**Stanford CS224R Deep Reinforcement Learning** (Spring 2025): Complete lecture series covering modern deep RL methods with applications to complex decision-making. Topics include policy gradients, actor-critic methods, offline RL, reward learning, model-based RL, and multi-task learning.[^90]

**Stanford CS234 Reinforcement Learning** (Winter 2025): Introductory RL course covering MDPs, tabular methods, function approximation, policy search, and exploration. The course includes practical implementations and addresses applications to sequential decision problems.[^92]

**Bank of England: "Agent-Based Modelling for Macroeconomics"** with Giovanni Dosi (2023): Discussion of complex evolving economies and how ABMs can illuminate technology, innovation, and macroeconomic policy. The event targets policy-makers and policy economists, demonstrating practical ABM applications.[^72]

**Mesa Tutorial: Agent-Based Modeling in Python** by Dr. Tom Pike (2023): Hands-on tutorial covering the Mesa framework for building agent-based models in Python. Demonstrates Mesa 2.0 features including improved visualization and new capabilities.[^117]

**Doyne Farmer on Markets as Ecosystems and Agent-Based Modeling** (2024): Interview discussing Farmer's approach to modeling financial markets, including how heterogeneous agents with different heuristics and strategies create market dynamics. Covers the methodology, philosophy, and practical applications of agent-based economic modeling.[^60]

### Quantitative Finance and RL Applications

**Implementing Reinforcement Learning in Trading Strategies** by QuantInsti (2024): Comprehensive guide covering gamification concepts in RL for trading, reward function design, input feature selection, neural network architectures, and challenges in building RL models with financial data.[^118]

**How Reinforcement Learning Can Be Applied to Quantitative Finance** - Quantopian (2018): Dr. Tom Starke discusses different uses of reinforcement learning in finance, machine learning types, and how they relate to trading applications. Provides practical insights on applying RL to financial markets.[^115]

**Deep Reinforcement Learning for Trading** - Hudson \& Thames (2024): Explores adoption of deep RL algorithms for designing trading strategies in continuous futures contracts. Discusses the connection between modern portfolio theory and the RL reward hypothesis, comparing multiple RL algorithms across asset classes.[^119]

**Reinforcement Learning for Trading Tutorial** by The Python Quants (2022): Webinar series on RL in finance covering fundamentals, implementation, and applications. Discusses benefits, drawbacks, and practical considerations for applying RL to trading.[^120]

**Dr. Ernest Chan - Machine Learning in Trading** Playlist: Informative series featuring renowned expert on quantitative trading and machine learning applications to financial markets.[^121]

### Specialized Topics

**Andrew Lo on the Adaptive Markets Hypothesis** (OECD, 2017): Lo outlines his adaptive markets hypothesis, explaining how financial market dynamics are driven by interactions as participants behave, learn, and adapt to each other and their environment.[^111]

**Andrew W. Lo: "Adaptive Markets: Financial Evolution at the Speed of Thought"** (Museum of American Finance, 2018): Evening lecture presenting Lo's framework for understanding market rationality and efficiency through evolutionary principles. Discusses how the theory reconciles efficient market and behavioral perspectives.[^112]

## Must-Read Articles \& Papers

### Foundational Papers

**"Asset Pricing Under Endogenous Expectations in an Artificial Stock Market"** by Arthur, Holland, LeBaron, Palmer, and Tayler (1996): This landmark paper introduces the Santa Fe Artificial Stock Market and demonstrates how heterogeneous agents with adaptive expectations can generate realistic market phenomena including technical trading, bubbles, crashes, and GARCH behavior.[^34][^122][^32]

**"Agent-Based Computational Finance"** by Blake LeBaron (2006): Comprehensive survey of agent-based models in finance, covering design questions, artificial financial markets, evolutionary dynamics, and market microstructure. Serves as an essential guide for researchers building computational financial markets.[^110][^31]

**"A Builder's Guide to Agent-Based Financial Markets"** by Blake LeBaron (2001): Practical guide for constructing agent-based financial market models, discussing trading rules, learning mechanisms, market microstructure, and evolutionary selection.[^123][^124][^31]

**"Heterogeneous Agent Models in Economics and Finance"** by Cars Hommes (2006): Thorough review of heterogeneous agent models featuring endogenous strategy switching, bounded rationality, and evolutionary selection. Demonstrates how simple HAMs generate complex dynamics and explains stylized facts of financial markets.[^125][^22][^40][^39][^21]

**"A Test for Independence Based on the Correlation Dimension"** by Brock, Scheinkman, Dechert, and LeBaron (1996): Statistical methodology paper enabling rigorous testing of nonlinear dependencies and chaos in financial time series. This methodological contribution underpins empirical validation of agent-based models.[^108]

### Recent Advances in Agent-Based Financial Modeling

**"Agent-Based Modeling in Economics and Finance: Past, Present, and Future"** by Robert Axtell and J. Doyne Farmer (2025): Major review article published in the Journal of Economic Literature providing comprehensive overview of ABM methodology, applications, and future directions. Discusses the shift toward quantitative ABMs that make testable predictions.[^3][^20]

**"Quantitative Agent-Based Models: A Promising Alternative for Macroeconomics"** by Farmer and colleagues (2025): Published in Oxford Review of Economic Policy, this paper makes the case for ABMs as practical alternatives to DSGE models for economic forecasting and policy analysis.[^106][^2]

**"Agent-based Model for Financial Vulnerability"** by Bookstaber, Paddrik, and Tivnan (2014): OFR working paper developing ABM framework for analyzing fire sales and funding vulnerabilities in the financial system. The model traces shock propagation through intermediation chains from cash providers to dealers to end investors.[^15]

**"Scalable Agent-Based Modeling for Complex Financial Market Simulations"** (2024): Describes computational framework for large-scale ABM simulations supporting multiple simultaneous assets and distributed computing. Demonstrates capturing stylized facts with heterogeneous agents making parallel decisions.[^46]

**"Agent-Based Modelling of Financial Markets and the New Kind of Science Market Model"** (2025): Introduces sophisticated ABM framework featuring 6,561 possible trading strategies with stochastic elements, feedback effects, and herding dynamics. Reproduces key stylized facts including fat-tailed distributions and volatility clustering.[^77]

### Reinforcement Learning in Finance

**"Deep Reinforcement Learning in Quantitative Algorithmic Trading: A Review"** (2021): Comprehensive review of deep RL applications to automated trading, covering theoretical foundations, practical challenges, and empirical results. Discusses lack of real-time testing and profitability issues in many studies.[^11]

**"FinRL: Deep Reinforcement Learning Framework to Automate Trading in Quantitative Finance"** (2021): Presents open-source framework implementing fine-tuned state-of-the-art DRL algorithms for quantitative trading. Provides accessible platform for developing and testing RL-based trading strategies.[^12]

**"Capturing Financial Markets to Apply Deep Reinforcement Learning"** (2019): Proposes novel Markov decision process model for capturing financial trading markets and explores modifications to existing RL approaches. Demonstrates generating consistently profitable trading signals.[^126]

**"Deep Reinforcement Learning for Trading"** (2024): Adopts deep RL algorithms for designing trading strategies in continuous futures contracts. Demonstrates significant outperformance versus classical strategies across multiple asset classes.[^119]

**"FLAG-Trader: Fusion LLM-Agent with Gradient-based Reinforcement Learning for Financial Trading"** (2025): Cutting-edge paper integrating large language models with gradient-driven RL for financial trading. Proposes unified architecture where partially fine-tuned LLM acts as policy network.[^24]

### Multi-Agent Systems and Market Microstructure

**"Stock Market Microstructure Inference via Multi-Agent Reinforcement Learning"** (2019): Applies multi-agent RL to infer market microstructure and model interactions between heterogeneous traders. Advances understanding of collective market behavior emerging from agent interactions.[^47]

**"Multi-Agent Systems for Computational Economics and Finance"** (2022): Reviews multi-agent systems research at the intersection of computer science, AI, finance, and economics. Covers algorithmic game theory, mechanism design, and computational social choice applications.[^18][^127][^17]

**"An Agent-Based Model for Crisis Liquidity Dynamics"** (2015): OFR working paper examining liquidity dynamics during financial crises using limit-order-book framework. Models interaction between liquidity demanders, suppliers, and market makers under stress.[^49]

**"High-frequency Financial Market Simulation and Flash Crash Scenarios Analysis"** (2022): Designs and implements novel high-frequency ABM generating realistic millisecond-level price time series. Analyzes flash crash scenarios in E-Mini S\&P 500 futures market.[^48]

### Behavioral Finance and Adaptive Markets

**"Adaptive Markets and the New World Order"** by Andrew Lo (2012): Presents the Adaptive Markets Hypothesis and its implications for portfolio management, risk management, and financial regulation. Demonstrates how evolutionary principles explain market efficiency as context-dependent and dynamic.[^53]

**"Behavioral Finance and Agent-Based Model: The New Evolving Discipline of Quantitative Behavioral Finance"** (2013): Argues that ABMs combined with behavioral insights create new discipline capable of quantifying impact of cognitive biases on market prices. Discusses integration of neuroeconomics findings into agent design.[^36]

**"Behavioral Agency Theory: New Foundations for Theorizing About Corporate Governance"** by Pepper and Gore (2012): Provides theoretical foundations for behavioral agency theory, incorporating loss aversion, time discounting, inequity aversion, and intrinsic motivation. Essential for modeling realistic principal-agent relationships in financial institutions.[^26]

### Estimation and Validation

**"Bayesian Estimation and Likelihood-Based Comparison of Agent-Based Volatility Models"** (2020): Proposes Hamiltonian Monte Carlo as general method for Bayesian inference of ABMs. Demonstrates rigorous statistical fitting and model comparison for agent-based volatility models.[^128]

**"Estimation of Financial Agent-Based Models with Simulated Maximum Likelihood"** (2016): Develops simulated maximum likelihood methodology for estimating ABM parameters from financial data. Advances ability to calibrate models quantitatively.[^129][^130]

## Toolkits \& Platforms

### Python Agent-Based Modeling Frameworks

**Mesa**: The premier open-source Python framework for agent-based modeling. Mesa 3.0 (released 2025) features:[^131][^132][^133][^134][^135][^136][^137]

- **AgentSet management**: Pandas-like capabilities for filtering, grouping, and analyzing agents[^132][^135][^136]
- **Flexible spatial grids**: Discrete (cell-based) and continuous space implementations[^134][^135][^132]
- **Browser-based visualization**: Interactive Solara-based interface with real-time data visualization[^135][^132][^134]
- **Integration with scientific Python**: Seamless use with NumPy, pandas, NetworkX, and Matplotlib[^132][^134][^135]
- **Built-in tools**: Data collection, batch runs, and parameter sweeps for systematic experimentation[^134][^135][^132]

Mesa has been applied across domains from economics and finance to ecology and epidemiology. The framework is designed to be the Python alternative to NetLogo, Repast, and MASON.[^137][^131][^135][^132][^134]

**Mesa-Geo**: Extension for geospatial agent-based modeling, enabling simulation of agents in real-world geographic contexts.[^138][^139]

**AgentPy**: Alternative package for agent-based modeling emphasizing simplicity and accessibility for researchers and students.[^140]

### Algorithmic Trading Platforms

**QuantConnect**: Cloud-based algorithmic trading platform with institutional-grade infrastructure. Key features include:[^70][^71][^141][^142][^143][^69]

- **LEAN algorithmic trading engine**: Open-source, event-driven framework supporting multi-asset portfolios[^71][^143][^69]
- **Extensive data library**: 400TB+ historical data covering equities, options, futures, forex, crypto, and indices since 1998[^69][^71]
- **Backtesting infrastructure**: Lightning-fast cloud cores with realistic fee, slippage, and margin modeling[^71]
- **Live trading integration**: Support for 20+ brokers including Interactive Brokers with co-located servers providing sub-100ms latency[^69][^71]
- **Multi-language support**: Algorithm development in Python or C\# with access to scientific libraries[^70][^71][^69]
- **Alternative data**: Rich library from 40+ vendors automatically linked to underlying securities[^71]

QuantConnect has deployed 375,000+ live strategies processing \$45B+ in monthly notional volume. The platform recently introduced MCP Server enabling AI agents to design, backtest, and trade strategies autonomously.[^71]

**QuantLib**: Free/open-source library for quantitative finance providing tools for modeling, trading, and risk management. QuantLib offers comprehensive derivatives pricing, fixed income analytics, and risk measurement capabilities.[^144]

### Financial Data and Research Platforms

**QuantConnect Datasets Marketplace**: Provides access to alternative datasets with uniform timestamps and point-in-time delivery to avoid selection bias. Datasets span fundamental data, sentiment analysis, satellite imagery, and more.[^71]

**PyPortfolioOpt**: Python library for portfolio optimization implementing modern portfolio theory, Black-Litterman allocation, and risk models. Can be integrated with other quant frameworks for complete portfolio management solutions.[^70][^69]

### Reinforcement Learning Frameworks

**FinRL**: Open-source deep reinforcement learning framework specifically designed for automated trading in quantitative finance. Features:[^145][^12]

- **Fine-tuned DRL algorithms**: Implementations of major algorithms (DQN, PPO, A2C, SAC, TD3) optimized for financial applications[^12]
- **Common reward functions**: Pre-built reward structures for financial objectives[^12]
- **Reduced debugging burden**: Alleviates error-prone programming in financial contexts[^12]

**Ray RLlib**: Scalable reinforcement learning library supporting distributed training and a wide range of algorithms. Used by researchers for large-scale financial RL experiments.

### Multi-Agent Simulation Tools

**Simudyne**: Enterprise platform for large-scale agent-based modeling with applications to financial market simulation. Powered by AWS and Red Hat OpenShift, Simudyne enables:[^81][^7]

- **Scalable market simulation**: Distributed computing for modeling millions of agents[^7][^81]
- **Realistic market microstructure**: Continuous double auction matching engine[^81]
- **Risk assessment**: Testing execution strategies and analyzing market impact[^81]


### Specialized ABM Tools

**NetLogo**: Popular agent-based modeling environment widely used in education and research. While not Python-based, it offers accessible entry point to ABM concepts.[^146][^147]

**AnyLogic**: Commercial multi-method simulation software supporting agent-based, system dynamics, and discrete event modeling. Used in business and policy applications.[^9][^85]

**NL4Py**: Python package enabling parallel execution of NetLogo simulations, bridging NetLogo's accessibility with Python's analytical capabilities.[^147]

## Conclusion

Agentic Quantitative Research represents the frontier of computational finance, synthesizing insights from artificial intelligence, behavioral economics, and complex systems science. This interdisciplinary field moves beyond traditional equilibrium models by explicitly modeling the heterogeneous, adaptive, and interacting nature of market participants.[^2][^3][^20]

The convergence of agent-based modeling and reinforcement learning creates powerful frameworks for understanding market dynamics, developing trading strategies, and assessing systemic risks. As computing power increases and data availability expands, quantitative agent-based models are transitioning from qualitative illustrations to empirical tools capable of making testable predictions and informing policy decisions.[^14][^47][^58][^106][^2][^20][^12]

The knowledge map presented here provides researchers and practitioners with structured pathways to master this domain. From foundational theories like the Adaptive Markets Hypothesis and Behavioral Agency Theory to cutting-edge applications in high-frequency trading and multi-agent coordination, the field offers rich opportunities for innovation. Leading universities provide rigorous training, while open-source tools like Mesa and QuantConnect democratize access to sophisticated modeling capabilities.[^57][^18][^47][^89][^135][^50][^52][^17][^46][^132][^134][^102][^48][^26][^69][^101][^71][^104][^96]

As financial markets grow more complex and interconnected, the ability to model them as adaptive ecosystems of intelligent agents becomes increasingly valuable. This comprehensive knowledge map equips the next generation of quantitative researchers to advance our understanding of financial markets and develop more robust, adaptive, and intelligent trading systems.[^50][^52][^1][^60]
<span style="display:none">[^148][^149][^150][^151][^152][^153][^154][^155][^156][^157][^158][^159][^160][^161][^162][^163][^164][^165][^166][^167][^168][^169][^170][^171][^172][^173][^174][^175][^176][^177][^178][^179][^180][^181][^182][^183][^184][^185][^186][^187][^188][^189][^190][^191][^192][^193][^194][^195][^196][^197][^198][^199][^200][^201][^202][^203][^204][^205][^206][^207][^208][^209][^210][^211][^212][^213][^214][^215][^216][^217][^218][^219][^220][^221][^222][^223][^224][^225][^226][^227][^228][^229][^230][^231][^232][^233][^234][^235][^236][^237][^238][^239][^240][^241][^242][^243][^244][^245][^246][^247]</span>

<div align="center">⁂</div>

[^1]: https://smythos.com/managers/finance/agent-based-modeling-in-finance/

[^2]: https://academic.oup.com/oxrep/advance-article/doi/10.1093/oxrep/graf027/8281854

[^3]: https://www.aeaweb.org/articles?id=10.1257%2Fjel.20221319

[^4]: https://www.remesh.ai/resources/agentic-ai-for-research-primer

[^5]: https://devrev.ai/blog/what-is-agentic-ai

[^6]: https://www.mckinsey.com/capabilities/tech-and-ai/our-insights/why-agents-are-the-next-frontier-of-generative-ai

[^7]: https://simudyne.com/wp-content/uploads/2019/08/A4-Guide-to-ABM-FINAL-5.pdf

[^8]: https://en.wikipedia.org/wiki/Agent-based_model

[^9]: https://ieeexplore.ieee.org/document/8632240/

[^10]: https://ijrai.org/index.php/ijrai/article/view/105/102

[^11]: https://www.semanticscholar.org/paper/a6a7e7be402fc5f7703e5c74a7b2afa84613a429

[^12]: https://arxiv.org/pdf/2111.09395.pdf

[^13]: https://milvus.io/ai-quick-reference/how-does-reinforcement-learning-work-in-financial-trading

[^14]: https://blog.mlq.ai/deep-reinforcement-learning-trading-strategies-automl/

[^15]: https://www.financialresearch.gov/working-papers/files/OFRwp2014-05_BookstaberPaddrikTivnan_Agent-basedModelforFinancialVulnerability_revised.pdf

[^16]: https://en.wikipedia.org/wiki/Agent-based_computational_economics

[^17]: https://repository.essex.ac.uk/33382/1/main.pdf

[^18]: https://arxiv.org/abs/2210.03540

[^19]: https://en.wikipedia.org/wiki/Multi-agent_system

[^20]: https://www.youtube.com/watch?v=r6VMpeTg8dU

[^21]: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=738423

[^22]: https://core.ac.uk/download/pdf/7178409.pdf

[^23]: https://ijtm.my.id/index.php/IJTM/article/view/123

[^24]: https://arxiv.org/pdf/2502.11433.pdf

[^25]: https://plutuseducation.com/blog/behavioral-agency-theory/

[^26]: https://eprints.lse.ac.uk/47569/1/Pepper_Behavioural_agency_theory_2012.pdf

[^27]: http://www.diva-portal.org/smash/get/diva2:937086/FULLTEXT01.pdf

[^28]: https://corporatefinanceinstitute.com/resources/esg/agency-theory/

[^29]: https://www.econstor.eu/bitstream/10419/64236/1/572990189.pdf

[^30]: https://www.cemla.org/actividades/2019-final/2019-09-estabilidad-financiera/2019-09-estabilidad-financiera-4.pdf

[^31]: https://people.brandeis.edu/~blebaron/wps/hbook.pdf

[^32]: https://sites.santafe.edu/~wbarthur/Papers/Arthur-HollandStockMarket.pdf

[^33]: https://www.sciencedirect.com/science/article/pii/0167278994902879

[^34]: https://www.santafe.edu/research/results/working-papers/asset-pricing-under-endogenous-expectations-in-an-

[^35]: https://keio.elsevierpure.com/en/publications/agent-based-modeling-bridges-theory-of-behavioral-finance-and-fin

[^36]: https://www.academia.edu/4775830/Behavioral_Finance_and_Agent_Based_Model_the_new_evolving_discipline_of_quantitative_behavioral_finance

[^37]: https://www.uni-bamberg.de/fileadmin/uni/fakultaeten/sowi_lehrstuehle/vwl_wirtschaftspolitik/Team/Westerhoff/Publications/2009/2009_Pbl_Westerhoff_II.pdf

[^38]: http://link.springer.com/10.1007/3-211-38043-4_5

[^39]: http://www.ssrn.com/abstract=742384

[^40]: https://www.econstor.eu/bitstream/10419/86441/1/05-056.pdf

[^41]: https://www.mdpi.com/2076-3417/13/3/1956

[^42]: https://arxiv.org/html/2411.07585v1

[^43]: http://arxiv.org/pdf/2407.09557.pdf

[^44]: https://www.preprints.org/manuscript/202111.0044/v1/download

[^45]: https://dl.acm.org/doi/10.1145/3604237.3626873

[^46]: https://arxiv.org/pdf/2312.14903.pdf

[^47]: https://arxiv.org/abs/1909.07748

[^48]: https://arxiv.org/pdf/2208.13654.pdf

[^49]: https://www.financialresearch.gov/working-papers/files/OFRwp-2015-18_Agent-based-Model-for-Crisis-Liquidity-Dynamics.pdf

[^50]: https://en.wikipedia.org/wiki/Adaptive_market_hypothesis

[^51]: https://www.investopedia.com/terms/a/adaptive-market-hypothesis.asp

[^52]: https://blogs.cfainstitute.org/investor/2017/12/18/the-adaptive-markets-hypothesis-a-financial-ecosystems-survival-guide/

[^53]: https://dspace.mit.edu/bitstream/handle/1721.1/75362/Lo_Adaptive%20Markets.pdf

[^54]: https://www.investglass.com/top-ai-agent-for-trading-revolutionizing-financial-market-strategies/

[^55]: https://www.luxalgo.com/blog/ai-agent-and-trading-psychology-can-machines-improve-human-decision-making/

[^56]: https://alpaca.markets/learn/how-traders-are-using-ai-agents-to-create-trading-bots-with-alpaca

[^57]: https://www.reddit.com/r/CapitalismVSocialism/comments/1e7fpr0/economic_planning_via_multiagent_reinforcement/

[^58]: https://arxiv.org/abs/2208.10434

[^59]: https://arxiv.org/abs/1801.08222

[^60]: https://www.youtube.com/watch?v=nbHpFrFjoC8

[^61]: https://faculty.sites.iastate.edu/tesfatsi/archive/tesfatsi/ABMForEconomics.TalkECB2014.JDoyneFarmer.pdf

[^62]: https://www.ssrn.com/abstract=3331423

[^63]: https://arxiv.org/pdf/1703.06840.pdf

[^64]: https://digitalcommons.usf.edu/cgi/viewcontent.cgi?article=10119\&context=etd

[^65]: https://www.biz4group.com/blog/ai-trading-agent-development

[^66]: https://www.lyzr.ai/blog/ai-agents-for-stock-market/

[^67]: https://www.osl.com/hk-en/academy/article/trading-bots-vs-ai-agents-everything-you-need-to-know

[^68]: https://dl.acm.org/doi/10.1145/3637528.3671801

[^69]: https://www.luxalgo.com/blog/quantconnect-review-best-platform-for-algo-trading-2/

[^70]: https://py.ai/tools/quantconnect/

[^71]: https://www.quantconnect.com

[^72]: https://www.youtube.com/watch?v=xGil0S8KkgY

[^73]: https://ieeexplore.ieee.org/document/10871473/

[^74]: https://arxiv.org/pdf/2112.04755.pdf

[^75]: https://arxiv.org/pdf/2208.10707.pdf

[^76]: https://neptune.ai/blog/7-applications-of-reinforcement-learning-in-finance-and-trading

[^77]: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5110020

[^78]: https://ijmsbe.journals.ekb.eg/article_237797_b864877abecedbea8bd2be7b64141160.pdf

[^79]: https://www.tandfonline.com/doi/full/10.1080/14697688.2024.2420609

[^80]: http://arxiv.org/pdf/2405.02480.pdf

[^81]: https://aws.amazon.com/blogs/hpc/harnessing-the-power-of-agent-based-modeling-for-equity-market-simulation-and-strategy-testing/

[^82]: https://arxiv.org/pdf/2108.07806.pdf

[^83]: https://marketlogicsoftware.com/blog/agentic-ai-as-a-market-intelligence-analyst/

[^84]: https://www.causaly.com/blog/introducing-agentic-research-a-new-era-for-scientific-decision-making

[^85]: https://www.youtube.com/playlist?list=PLA9C67321E8433E5A

[^86]: https://www.edx.org/learn/finance/massachusetts-institute-of-technology-mathematical-methods-for-quantitative-finance

[^87]: https://micromasters.mit.edu/fin/

[^88]: https://mitsloan.mit.edu/shared/ods/documents?DocumentID=4660

[^89]: https://cs224r.stanford.edu

[^90]: https://www.youtube.com/watch?v=EvHRQhMX7_w

[^91]: http://web.stanford.edu/class/cs234/

[^92]: https://www.youtube.com/watch?v=WsvFL-LjA6U

[^93]: https://explorecourses.stanford.edu/search?view=catalog\&filter-coursestatus-Active=on\&page=0\&catalog=\&q=CME+241%3A+Foundations+of+Reinforcement+Learning+with+Applications+in+Finance\&collapse=

[^94]: https://cme241.github.io

[^95]: https://mcf.stanford.edu

[^96]: https://conduct.edu.vn/conduct/princeton-course-guide/

[^97]: https://talk.collegeconfidential.com/t/orfe-v-econ-for-i-banking/875378

[^98]: https://www.reddit.com/r/ApplyingToCollege/comments/1kuijz0/princeton_quantitative_finance_financial/

[^99]: https://orfe.princeton.edu/graduate/courses

[^100]: https://orfe.princeton.edu/undergraduate/courses

[^101]: https://digital.ucas.com/coursedisplay/courses/8ec3c35c-89dc-55ca-717c-07d8162257aa

[^102]: https://www.maths.ox.ac.uk/study-here/postgraduate-study/msc-mathematical-and-computational-finance

[^103]: https://www.ox.ac.uk/admissions/graduate/courses/msc-mathematical-and-computational-finance

[^104]: https://www.msfinance.uzh.ch/en.html

[^105]: https://www.reddit.com/r/quantfinance/comments/1jggk03/target_unis_in_europe_eth_vs_oxford/

[^106]: https://www.linkedin.com/posts/doyne-farmer-4aa57517_quantitative-agent-based-models-a-promising-activity-7383540405746810881-7Yg7

[^107]: https://www.santafe.edu/news-center/news/agent-based-models-move-into-the-economic-mainstream

[^108]: https://scholar.google.com/citations?user=CiwEc6gAAAAJ\&hl=en

[^109]: https://ideas.repec.org/e/c/ple1.html

[^110]: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=224048

[^111]: https://www.youtube.com/watch?v=MW6zqaKP-dU

[^112]: https://www.youtube.com/watch?v=swWBVVYeA7s

[^113]: https://faculty.sites.iastate.edu/tesfatsi/archive/tesfatsi/afinance.htm

[^114]: https://faculty.sites.iastate.edu/tesfatsi/archive/econ308/tesfatsion/SFISTOCKDetailed.LT.htm

[^115]: https://www.youtube.com/watch?v=O7BGfHZShZI

[^116]: https://www.youtube.com/watch?v=_n4JOMnAeCs

[^117]: https://www.youtube.com/watch?v=8P5P7NpCx5o

[^118]: https://www.youtube.com/watch?v=hDhFRT8DcGY

[^119]: https://www.youtube.com/watch?v=PwoTb-SxoC0

[^120]: https://www.youtube.com/watch?v=bDlnrf9Er5E

[^121]: https://www.youtube.com/playlist?list=PLD7IrLyN7uvIdAtZPBikfIaUNmFWe4pdz

[^122]: https://people.brandeis.edu/~blebaron/wps/sfisum.pdf

[^123]: http://www.tandfonline.com/doi/abs/10.1088/1469-7688/1/2/307

[^124]: https://wiki.santafe.edu/images/2/25/Bldr.pdf

[^125]: https://linkinghub.elsevier.com/retrieve/pii/S157400210502023X

[^126]: https://arxiv.org/pdf/1907.04373.pdf

[^127]: https://arxiv.org/pdf/2210.03540.pdf

[^128]: https://link.springer.com/10.1007/s11403-020-00289-z

[^129]: http://www.ssrn.com/abstract=2783663

[^130]: https://www.semanticscholar.org/paper/9e764fb678b209432a237fd423ed0b058d61845a

[^131]: https://doi.curvenote.com/10.25080/Majora-7b98e3ed-009

[^132]: https://joss.theoj.org/papers/10.21105/joss.07668

[^133]: http://conference.scipy.org/proceedings/scipy2015/pdfs/jacqueline_kazil.pdf

[^134]: https://mesa.readthedocs.io

[^135]: https://www.theoj.org/joss-papers/joss.07668/10.21105.joss.07668.pdf

[^136]: https://www.reddit.com/r/Python/comments/1gn5q8z/mesa_30_a_major_update_to_pythons_agentbased/

[^137]: https://github.com/projectmesa/mesa

[^138]: https://www.semanticscholar.org/paper/47a66b9806660a87bb0a6ca5dfe6bcad4806fd0f

[^139]: https://arxiv.org/abs/2409.05235

[^140]: https://joss.theoj.org/papers/10.21105/joss.03065.pdf

[^141]: https://www.quantconnect.com/explore/

[^142]: https://github.com/quantconnect

[^143]: https://www.lean.io

[^144]: https://www.quantlib.org

[^145]: https://www.reddit.com/r/algotrading/comments/viag8p/reinforcement_learning_for_algorithmic_trading/

[^146]: https://dl.acm.org/doi/10.1145/3476883.3520218

[^147]: https://arxiv.org/pdf/1808.03292.pdf

[^148]: http://www.emerald.com/mrr/article/46/3/437-466/310966

[^149]: https://environmentalsystemsresearch.springeropen.com/articles/10.1186/s40068-024-00362-7

[^150]: https://interdisiplin.my.id/index.php/i/article/view/64

[^151]: https://www.nepjol.info/index.php/bmcrj/article/view/80082

[^152]: http://link.springer.com/10.1007/978-981-15-2537-7_2

[^153]: https://www.ijisrt.com/blossoming-amidst-adversity-a-quantitative-review-on-the-resilience-of-senior-high-school-students-using-connor-davidson-resilience-scale-cdrisc

[^154]: https://bmcmedresmethodol.biomedcentral.com/articles/10.1186/s12874-023-01929-1

[^155]: https://www.ijherjournal.com/dergi/mixed-methods-research-approaches-as-a-mechanism-for-bridging-the-gap-between-quantitative-and-qualitative-research-methodologies20230601013339.pdf

[^156]: https://bioone.org/journals/journal-of-coastal-research/volume-50/issue-sp1/JCR-SI50-011.1/An-application-of-an-adaptive-quantitative-method-to-measure-the/10.2112/JCR-SI50-011.1.full

[^157]: https://journal.formosapublisher.org/index.php/fjmr/article/view/9285

[^158]: https://pmc.ncbi.nlm.nih.gov/articles/PMC11600101/

[^159]: https://arxiv.org/abs/2503.23037

[^160]: http://arxiv.org/pdf/2410.22457.pdf

[^161]: https://arxiv.org/pdf/2503.06745.pdf

[^162]: https://pmc.ncbi.nlm.nih.gov/articles/PMC10920425/

[^163]: https://pmc.ncbi.nlm.nih.gov/articles/PMC11889410/

[^164]: https://onlinelibrary.wiley.com/doi/pdfdirect/10.1002/ejsp.2723

[^165]: https://arxiv.org/abs/2412.13114

[^166]: https://www.jaai.net/vol3/JAAI-V3N2-41.pdf

[^167]: https://www.inet.ox.ac.uk/news/agent-based-modelling-comes-of-age

[^168]: https://blogs.nvidia.com/blog/what-is-agentic-ai/

[^169]: https://livrepository.liverpool.ac.uk/id/eprint/3130139

[^170]: https://www.nationaleducationservices.org/deep-finance-cuttingedge-deep-learning-applications-in-market-prediction-risk-analytics-and-algorithmic-trading/pid-2230538479

[^171]: https://www.semanticscholar.org/paper/4800f2d1bf0ea1a069ae3c257b791dc040782f4b

[^172]: https://www.wne.uw.edu.pl/download_file/6165/0

[^173]: https://arxiv.org/pdf/2109.05283.pdf

[^174]: https://fsc.stevens.edu/trading-strategies-using-reinforcement-learning/

[^175]: https://academic.oup.com/neuro-oncology/article/26/Supplement_5/v56/7825094

[^176]: https://link.springer.com/10.1007/978-3-031-57057-5

[^177]: https://www.frontiersin.org/article/10.3389/fimmu.2019.01289/full

[^178]: https://www.mdpi.com/2071-1050/11/7/1967

[^179]: https://link.springer.com/10.1007/s40815-024-01731-1

[^180]: https://dx.plos.org/10.1371/journal.pcbi.1011070

[^181]: http://biorxiv.org/lookup/doi/10.1101/2023.01.12.523847

[^182]: https://arxiv.org/pdf/2206.09772.pdf

[^183]: https://arxiv.org/pdf/2501.09429.pdf

[^184]: https://arxiv.org/pdf/2412.11259.pdf

[^185]: https://mitsloan.mit.edu/faculty/academic-groups/finance/courses

[^186]: https://www.shiksha.com/studyabroad/usa/universities/princeton-university/mse-in-operations-research-and-financial-engineering

[^187]: http://jasss.soc.surrey.ac.uk/20/4/13.html

[^188]: https://link.springer.com/10.1007/978-3-030-24299-2_14

[^189]: https://ieeexplore.ieee.org/document/9776207/

[^190]: https://www.cambridge.org/core/product/identifier/CBO9780511617751A021/type/book_part

[^191]: https://www.semanticscholar.org/paper/d2a5591c9d7cfc177448253b26d069d145993539

[^192]: http://link.springer.com/10.1007/s11403-012-0100-y

[^193]: http://link.springer.com/10.1057/eej.2010.53

[^194]: https://pmc.ncbi.nlm.nih.gov/articles/PMC5330465/

[^195]: https://pmc.ncbi.nlm.nih.gov/articles/PMC4100891/

[^196]: https://www.emerald.com/insight/content/doi/10.1108/REPS-03-2019-0037/full/html

[^197]: http://arxiv.org/pdf/1909.11650.pdf

[^198]: https://arxiv.org/html/2510.12189v1

[^199]: https://www.jasss.org/4/4/reviews/abumostafa.html

[^200]: https://www.sciencedirect.com/science/article/pii/S0378437123009184

[^201]: https://scholarworks.brandeis.edu/esploro/outputs/book/Computational-Finance-1999/9924036746901921

[^202]: https://link.springer.com/10.1007/978-3-030-61255-9_30

[^203]: https://ieeexplore.ieee.org/document/10628357/

[^204]: http://biorxiv.org/lookup/doi/10.1101/2024.04.09.588670

[^205]: https://www.scitepress.org/DigitalLibrary/Link.aspx?doi=10.5220/0013645000003970

[^206]: https://arxiv.org/abs/2510.05185

[^207]: https://arxiv.org/pdf/1904.08315.pdf

[^208]: https://joss.theoj.org/papers/10.21105/joss.05100.pdf

[^209]: https://arxiv.org/pdf/2311.17688.pdf

[^210]: https://openresearchsoftware.metajnl.com/article/10.5334/jors.306/

[^211]: https://joss.theoj.org/papers/10.21105/joss.05087.pdf

[^212]: https://dl.acm.org/doi/10.1007/978-3-030-61255-9_30

[^213]: https://www.maths.ox.ac.uk/members/students/postgraduate-courses/msc-mcf/mscmcf-course-components

[^214]: https://mesa.readthedocs.io/stable/getting_started.html

[^215]: https://www.semanticscholar.org/paper/a4d33353dfdc546d499726c87456bf5dfc0e7bf2

[^216]: http://ieeexplore.ieee.org/document/7850016/

[^217]: http://www.ssrn.com/abstract=2149543

[^218]: https://arxiv.org/pdf/1101.1847.pdf

[^219]: https://arxiv.org/pdf/1601.00229.pdf

[^220]: https://www.tandfonline.com/doi/pdf/10.1080/1331677X.2021.2021098?needAccess=true

[^221]: https://www.linkedin.com/posts/puneet--khandelwal_quant-youtube-in-models-activity-7338097955196891137-EFWp

[^222]: https://people.brandeis.edu/~blebaron/wps/disagg.pdf

[^223]: https://open.ncl.ac.uk/academic-theories/3/agency-theory/

[^224]: https://arxiv.org/abs/2510.12189

[^225]: https://www.britannica.com/money/financial-agency-theory

[^226]: https://www.sciencedirect.com/science/article/pii/S2214845021000995

[^227]: https://www.sciencedirect.com/topics/social-sciences/agency-theory

[^228]: http://www.ssrn.com/abstract=738423

[^229]: http://link.springer.com/10.1007/978-3-642-56131-3_18

[^230]: https://www.semanticscholar.org/paper/b15bc00b3776714540a7c49ff3770ed13051425c

[^231]: https://www.semanticscholar.org/paper/174c382958521e8027e106f74a5e3a0adfffffc4

[^232]: https://www.semanticscholar.org/paper/04b001f6691956d347e56f9a35686a20c4ac017c

[^233]: https://www.mdpi.com/2073-8994/12/8/1281/pdf

[^234]: https://academic.oup.com/bib/article-pdf/16/1/137/5030642/bbt077.pdf

[^235]: https://arxiv.org/pdf/1305.2121.pdf

[^236]: https://www.frontiersin.org/articles/10.3389/fbioe.2020.00249/pdf

[^237]: https://biomedres.us/pdfs/BJSTR.MS.ID.004233.pdf

[^238]: https://pmc.ncbi.nlm.nih.gov/articles/PMC7301008/

[^239]: https://arxiv.org/pdf/2112.14377.pdf

[^240]: https://www.ecologyandsociety.org/vol11/iss1/art46/ES-2006-1749.pdf

[^241]: https://www.semanticscholar.org/paper/Building-the-Santa-Fe-Artiﬁcial-Stock-Market-LeBaron/8717ba6ca138af9dbf6ece0e625fa3d60be1f977

[^242]: https://ideas.repec.org/p/ams/ndfwpp/05-01.html

[^243]: https://webhome.phy.duke.edu/~palmer/papers/arob98.pdf

[^244]: http://research.economics.unsw.edu.au/vpanchenko/teaching/bh.pdf

[^245]: https://cendef.uva.nl/binaries/content/assets/subsites/amsterdam-school-of-economics/amsterdam-school-of-economics-research-institute/cendef/working-papers-2001/bhssri.pdf

[^246]: https://www.emergentmind.com/topics/heterogeneous-agent-based-model

[^247]: https://scholarworks.brandeis.edu/esploro/outputs/journalArticle/An-artificial-stock-market/9924036745701921

