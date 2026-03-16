# In-context If-Then Capacity: Benchmarking Persistent Conditional Constraints

This project evaluates the ability of Large Language Models (LLMs) to follow persistent conditional rules (e.g., "Every time you mention a dog, mention a cat") within long-form generation tasks. We introduce **CondIF-Bench**, a synthetic benchmark that categorizes conditional instructions by trigger type and action type.

## Key Findings
- **Lexical Superiority**: Models are 30-40% more accurate at keyword-based triggers than structural or conceptual triggers.
- **Structural Fragility**: Models struggle significantly with triggers tied to paragraph starts, numbers, or geographic locations.
- **Formatting Success**: Models are highly reliable at applying conditional formatting (bold/italics).
- **Over-application (False Positives)**: Models exhibit high rates of "leaked" actions, applying the "then" clause even without the "if" trigger.

## How to Reproduce
1. **Environment Setup**:
   ```bash
   uv venv
   source .venv/bin/activate
   uv pip install -r requirements.txt
   ```
2. **Generate Benchmark**:
   ```bash
   python src/generate_bench.py
   ```
3. **Run Inference**:
   ```bash
   python src/model_runner.py
   ```
4. **Run Evaluation**:
   ```bash
   python src/evaluator.py
   ```
5. **Analyze Results**:
   ```bash
   python src/analyze.py
   ```

## File Structure
- `src/`: Python scripts for generation, inference, evaluation, and analysis.
- `datasets/`: Generated `CondIF-Bench` dataset.
- `results/`: Model outputs and evaluation results.
- `figures/`: Visualizations of model performance.
- `REPORT.md`: Comprehensive research report.

## License
MIT
