# Cloned Repositories

## Repo 1: AgentIF
- URL: [https://github.com/THU-KEG/AgentIF](https://github.com/THU-KEG/AgentIF)
- Purpose: Benchmarking instruction following in agentic scenarios.
- Location: `code/AgentIF/`
- Key Files:
    - `data/`: Contains the dataset (same as HuggingFace).
    - `evaluation/`: Scripts for evaluating model responses.
- Notes: Specifically includes "conditional" constraints which are highly relevant to this research.

## Repo 2: IFEval (google-research)
- URL: [https://github.com/google-research/google-research/tree/master/instruction_following_eval](https://github.com/google-research/google-research/tree/master/instruction_following_eval)
- Purpose: The original IFEval implementation.
- Location: (Not cloned due to being part of a larger monorepo)
- Recommended Usage: Download specific verification scripts (`verifiers.py`, `instructions.py`) if needed for custom conditional evaluations.
