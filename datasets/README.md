# Downloaded Datasets

This directory contains samples of the datasets for the "In-context If-Then Capacity" research project. Data files are NOT committed to git due to size.

## Dataset 1: IFEval (google/IFEval)

### Overview
- **Source**: [HuggingFace](https://huggingface.co/datasets/google/IFEval)
- **Task**: Instruction-Following Evaluation
- **Format**: JSONL

### Sample Data
```json
{
  "key": 1000,
  "prompt": "Write a 300+ word summary... Do not use any commas...",
  "instruction_id_list": ["punctuation:no_comma", ...]
}
```

## Dataset 2: AgentIF (THU-KEG/AgentIF)

### Overview
- **Source**: [HuggingFace](https://huggingface.co/datasets/THU-KEG/AgentIF)
- **Task**: Benchmarking Instruction Following in Agentic Scenarios
- **Format**: JSONL

### Sample Data
```json
{
  "id": "agentif:general:20:1:Code_prompt",
  "input": [...],
  "constraints": [
    {
      "desc": "If <task> has multiple goals, only complete the first goal",
      "dimension": "conditional"
    }
  ]
}
```

## Download Instructions

To download the full datasets, use:

```python
from datasets import load_dataset
# IFEval
load_dataset("google/IFEval")['train'].to_json("datasets/ifeval.jsonl")
# AgentIF
load_dataset("THU-KEG/AgentIF")['test'].to_json("datasets/agentif.jsonl")
```
