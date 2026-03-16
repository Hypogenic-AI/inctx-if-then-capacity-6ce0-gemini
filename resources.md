# Resources Catalog: In-context If-Then Capacity

## Summary
This document catalogs the papers and datasets gathered for the "In-context If-Then Capacity" research.

## Papers
Total papers downloaded: 5

| Title | Authors | Year | File | Key Info |
|-------|---------|------|------|----------|
| LSRIF | Ren et al. | 2026 | [papers/2601.06431_LSRIF.pdf](papers/2601.06431_LSRIF.pdf) | Defines "Conditional Structure" for instructions. |
| AGENTIF | Qi et al. | 2025 | [papers/2505.16944_AGENTIF.pdf](papers/2505.16944_AGENTIF.pdf) | Benchmark with "conditional" constraint dimensions. |
| Content Effects | Dasgupta et al. | 2022 | [papers/2207.07051_Content_Effects.pdf](papers/2207.07051_Content_Effects.pdf) | Cognitive basis for inconsistent reasoning. |
| IFEval | Zhou et al. | 2023 | [papers/2311.07911_IFEval.pdf](papers/2311.07911_IFEval.pdf) | Standard verifiable instruction-following benchmark. |
| Reasoning Survey | Various | 2025 | [papers/2502.17419_Reasoning_Survey.pdf](papers/2502.17419_Reasoning_Survey.pdf) | Overview of System 2 and reasoning LLMs. |

## Datasets
Total datasets sample downloaded: 2

| Name | Source | Size | Task | Location | Notes |
|------|--------|------|------|----------|-------|
| IFEval | HuggingFace (google/IFEval) | 541 samples | Instruction Following | [datasets/ifeval_sample.jsonl](datasets/ifeval_sample.jsonl) | Standard verifiable benchmark. |
| AgentIF | HuggingFace (THU-KEG/AgentIF) | 707 samples | Agentic Instructions | [datasets/agentif_sample.jsonl](datasets/agentif_sample.jsonl) | Contains "conditional" constraint labels. |

## Recommendations for Experiment Design

1. **Primary Evaluation**: Use **IFEval** as a baseline for general instruction following capability.
2. **Conditional Evaluation**: Construct a specialized "If-Then" dataset inspired by the **LSRIF** template:
    - **Structure**: `If [Condition C] then [Action A1] else [Action A2]`.
    - **Control**: Vary [Condition C] between simple (keyword present) and complex (semantic property).
    - **Control**: Vary [Action A1/A2] between simple (formatting) and complex (reasoning).
3. **Consistency Metric**: Analyze if the model follows the logic across different *semantic contents* of C, A1, and A2.
4. **Error Analysis**: Log if failures occur at the condition detection stage or the action execution stage.

## Data Download Instructions

### IFEval (HuggingFace)
```python
from datasets import load_dataset
dataset = load_dataset("google/IFEval")
dataset['train'].to_json("datasets/ifeval.jsonl")
```

### AgentIF (HuggingFace)
```python
from datasets import load_dataset
dataset = load_dataset("THU-KEG/AgentIF")
dataset['test'].to_json("datasets/agentif.jsonl")
```
