# Research Plan: In-context If-Then Capacity

## Motivation & Novelty Assessment

### Why This Research Matters
As LLMs are increasingly deployed as autonomous agents or in high-stakes environments (e.g., medical advice, legal drafting), their ability to follow conditional safety and formatting rules is paramount. A simple instruction like "If the user mentions symptoms, provide a disclaimer" must be followed consistently. Failures in conditional logic (False Negatives) or over-application (False Positives) undermine the reliability of these systems.

### Gap in Existing Work
Existing benchmarks like **IFEval** focus primarily on static, unconditional constraints. While **AgentIF** and **LSRIF** introduce logical structures, they often focus on "one-off" task execution. The user's specific observation about "every time you mention a dog you also mention a cat" highlights a **Global Persistent Conditional Constraint**. There is a lack of systematic research into whether models are *consistently* good at these across different semantic triggers (lexical vs. conceptual) and actions (formatting vs. content).

### Our Novel Contribution
- **Systematic Taxonomy**: We categorize conditional instructions by Trigger Type (Lexical, Conceptual, Structural) and Action Type (Lexical, Formatting, Content).
- **Global Consistency Analysis**: We measure the correlation between a model's performance on different categories to determine if "conditional capacity" is a unified capability or fragmented.
- **Error Attribution**: We distinguish between "Trigger Miss" (failure to detect the condition) and "Action Failure" (detecting the condition but failing the response).

### Experiment Justification
- **Experiment 1: Baseline Conditional Capacity**: Evaluate SOTA models on our new "Conditional-IF" benchmark to establish current capability floors and ceilings.
- **Experiment 2: Semantic vs. Lexical Consistency**: Compare if models that excel at keyword-based triggers also handle abstract conceptual triggers (e.g., "if you mention sadness...").
- **Experiment 3: Complexity Scaling**: Test how increasing the number of active conditional rules affects performance (Interference).

---

## Research Question
Is the ability of large language models to follow conditional (if-then) instructions consistent over different types of instructions, and can we reliably measure this capacity?

## Hypothesis Decomposition
- **H1 (Inconsistency)**: Models perform significantly better on Lexical Triggers (keywords) than Conceptual Triggers (themes/sentiment).
- **H2 (Correlation)**: There is a positive correlation between performance on Lexical-Action and Content-Action conditional tasks within a model.
- **H3 (False Positive Bias)**: Models exhibit higher False Positive rates for "vague" conceptual triggers.

## Proposed Methodology

### Approach
We will build a specialized evaluation harness called **CondIF-Bench**. We will use LLMs to generate 100 prompts that require long-form creative writing (to allow for multiple trigger opportunities) with 3-5 global conditional rules each.

### Experimental Steps
1. **Dataset Generation**: Use GPT-4o to generate prompts and rules based on our $3 \times 3$ taxonomy (Trigger $\times$ Action).
2. **Model Execution**: Run selected models (GPT-4o, Claude 3.5 Sonnet, etc.) on these prompts.
3. **Automated Evaluation**:
   - Use Regex/Python for Lexical/Formatting verification.
   - Use GPT-4o as a critic for Conceptual/Content verification.
4. **Statistical Analysis**: Calculate Trigger Detection Rate, Conditional Accuracy, and False Positive Rate. Perform correlation analysis (Pearson/Spearman) across categories.

### Baselines
- **Unconditional IF Accuracy**: Performance on the same actions when instructed unconditionally (from IFEval/AgentIF).
- **Random/Majority Baseline**: To measure chance performance.

### Evaluation Metrics
- **Recall (Conditional)**: $P(\text{Action} | \text{Trigger})$
- **Precision (Conditional)**: $P(\text{Trigger} | \text{Action})$
- **Trigger Detection Accuracy**: Does the model correctly identify instances where the condition is met?
- **Consistency Score**: Variance in performance across the 9 categories.

## Success Criteria
- Identifying specific "weak" categories of conditional instructions.
- Establishing a "Conditional Capacity" score for major models.
- Demonstrating whether "System 2" (reasoning) models significantly outperform "System 1" models in this specific domain.
