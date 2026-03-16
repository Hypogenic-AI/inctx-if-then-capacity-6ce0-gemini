# Literature Review: In-context If-Then Capacity

## Research Area Overview
Large Language Models (LLMs) are increasingly used for complex tasks requiring instruction following. While basic instruction following is well-studied, the ability to handle **logical structures** within instructions—specifically sequential dependencies and conditional branching (if-then logic)—remains a frontier. Recent research indicates that LLMs' capacity for such structured reasoning is inconsistent and can be significantly influenced by prompt composition, reward modeling, and underlying reasoning capabilities (System 1 vs. System 2).

## Key Papers

### Paper 1: LSRIF: Logic-Structured Reinforcement Learning for Instruction Following
- **Authors**: Qingyu Ren, et al.
- **Year**: 2026
- **Source**: arXiv (2601.06431)
- **Key Contribution**: Proposes the LSRIF framework which explicitly models instruction logic (Parallel, Sequential, and Conditional).
- **Methodology**: 
    - **LSRInstruct**: A dataset capturing logical structures.
    - **LSRM (Logic-Structured Reward Modeling)**: A reward scheme that aligns with logical execution semantics. For conditional structures, rewards are assigned only to the branch corresponding to the satisfied condition.
- **Results**: LSRIF improves both in-domain and out-of-domain instruction following and general reasoning. Analysis shows "sharpened" attention on logical operators.
- **Relevance to Our Research**: Provides a formal definition of "Conditional Structure" in instructions (Trigger $\rightarrow$ True Branch / False Branch) and a template for measuring it.

### Paper 2: AGENTIF: Benchmarking Instruction Following of LLMs in Agentic Scenarios
- **Authors**: Yunjia Qi, et al.
- **Year**: 2025
- **Source**: arXiv (2505.16944)
- **Key Contribution**: Benchmarks instruction following in complex, multi-turn agentic scenarios.
- **Methodology**: Categorizes constraints into dimensions, including a "conditional" dimension where constraints only apply if certain conditions are met.
- **Results**: Highlights that existing models struggle with condition-dependent constraints in dynamic environments.
- **Relevance to Our Research**: Provides empirical evidence and a dataset (AgentIF) with explicitly labeled "conditional" constraints.

### Paper 3: Instruction-Following Evaluation by Large Language Models (IFEval)
- **Authors**: Jeffrey Zhou, et al.
- **Year**: 2023
- **Source**: arXiv (2311.07911)
- **Key Contribution**: Introduced IFEval, a benchmark of "verifiable instructions" (e.g., length constraints, format constraints).
- **Methodology**: Uses 25 types of objective, programmatically verifiable instructions.
- **Relevance to Our Research**: The standard baseline for any instruction-following study. While it lacks a dedicated "if-then" category, its "Combination" tasks provide a foundation for complex instruction testing.

### Paper 4: Language models show human-like content effects on reasoning tasks
- **Authors**: Ishita Dasgupta, et al.
- **Year**: 2022
- **Source**: arXiv (2207.07051)
- **Key Contribution**: Shows that LLM performance on logical tasks (like syllogisms) is heavily biased by the semantic content of the task (belief bias).
- **Relevance to Our Research**: Suggests that "if-then capacity" may not be a pure logical capability but is interactively influenced by the content of the "if" condition and the "then" action.

## Common Methodologies
- **Dataset Construction**: Using LLMs (like GPT-4) to generate complex, structured instructions from atomic constraints.
- **Verifiable Rewards**: Programmatic verification of constraints (e.g., regex for formats, word counts for length) to ensure objective evaluation.
- **Reward Modeling**: Using RL (like PPO or GRPO) with structured rewards that propagate failures in logical dependencies.

## Standard Baselines
- **IFEval**: The primary benchmark for instruction adherence.
- **ComplexBench**: For compositional constraints.
- **Reasoning Models**: GPT-4o, Claude 3.5 Sonnet, and "System 2" models like DeepSeek-R1/o1 as upper bounds for logical consistency.

## Gaps and Opportunities
- **Consistency over Semantic Variations**: Most benchmarks test if-then logic with a specific semantic content. There is a gap in analyzing if the *logic itself* holds when the *content* changes (e.g., abstract vs. concrete conditions).
- **Reliability of Trigger Detection**: Investigating whether failure occurs in detecting the "if" condition or in executing the "then" branch.

## Recommendations for Our Experiment
1. **Dataset**: Use a combination of IFEval (for baseline) and a custom "If-Then" dataset modeled after LSRIF's `Selection` structure.
2. **Metrics**: Measure **Conditional Accuracy** (following the correct branch) vs. **Global Accuracy** (satisfying all constraints regardless of logic).
3. **Control Variables**: Vary the complexity of the "if" trigger (e.g., simple keyword vs. semantic property) and the "then" action.
