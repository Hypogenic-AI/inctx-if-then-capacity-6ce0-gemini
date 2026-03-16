# In-context If-Then Capacity: A Systematic Analysis

## Executive Summary
This research investigates the ability of Large Language Models (LLMs) to follow **Global Persistent Conditional Constraints** (e.g., "Every time you mention X, do Y"). We find that model capacity is highly inconsistent across different types of triggers and actions. While models excel at keyword-based (lexical) triggers, they struggle significantly with structural triggers (e.g., "at the start of a paragraph") and conceptual triggers (e.g., "referring to nature"). Furthermore, we observe a high rate of **False Positives**, where models over-apply conditional actions even in the absence of the trigger.

## Goal
The primary goal was to measure the reliability and consistency of LLMs' "If-Then" capacity across a taxonomy of triggers (Lexical, Conceptual, Structural) and actions (Lexical, Formatting, Content). We hypothesized that performance would be inconsistent and that models would exhibit a bias towards over-application.

## Data Construction

### Dataset Description
We created **CondIF-Bench**, a synthetic benchmark consisting of 30 long-form creative writing prompts (300+ words). Each prompt contains 2-3 global conditional rules randomly sampled from our taxonomy:
- **Triggers**: Lexical (e.g., "mountain"), Conceptual (e.g., "nature"), Structural (e.g., "start of a paragraph").
- **Actions**: Lexical (e.g., "say 'Aha!'"), Formatting (e.g., "BOLD"), Content (e.g., "describe a smell").

### Example Sample
**Base Prompt**: "Write a historical drama about a secret meeting between two rival queens."
**Rules**:
1. Every time you mention the word 'silver', you must immediately add the word 'DANGER'. (Lexical Trigger -> Lexical Action)
2. Every time you refer to the concept of 'betrayal', you must write that entire sentence in italics. (Conceptual Trigger -> Formatting Action)
3. Every time you start a new paragraph, you must follow it with a sentence where you ask a question. (Structural Trigger -> Content Action)

## Experiment Description

### Methodology
We evaluated two models from the OpenAI family: **GPT-4o** (Large) and **GPT-4o-mini** (Small/Efficient).
- **Inference**: Temperature 0.0 to ensure reproducibility.
- **Evaluation**: 
  - Programmatic verification for Lexical/Formatting actions.
  - LLM-as-a-judge (GPT-4o-mini) for Conceptual triggers and Content actions.

### Evaluation Metrics
- **Conditional Adherence Score**: $P(\text{Action} | \text{Trigger})$ - The probability that the action is performed given the trigger occurred.
- **False Positive Count**: Instances where the action occurred without the trigger.

## Raw Results

### Summary by Trigger Type
| Model | Lexical | Conceptual | Structural |
|-------|---------|------------|------------|
| GPT-4o | 0.66 | 0.52 | 0.38 |
| GPT-4o-mini | 0.65 | 0.37 | 0.33 |

### Summary by Action Type
| Model | Lexical | Formatting | Content |
|-------|---------|------------|---------|
| GPT-4o | 0.32 | 0.78 | 0.68 |
| GPT-4o-mini | 0.22 | 0.79 | 0.52 |

## Result Analysis

### Key Findings
1. **Lexical Superiority**: Both models find lexical (keyword) triggers significantly easier to monitor than conceptual or structural ones.
2. **Structural Fragility**: Models exhibit a "blind spot" for structural triggers like paragraph boundaries or sentence completions, often failing to trigger the required action.
3. **The "Action Paradox"**: While models are excellent at conditional formatting (italics/bold), they are surprisingly poor at conditional lexical insertion ("say word X"). This suggests that "X" feels like a hallucination or an interruption that the model's fluency filters out.
4. **Scale Matters**: GPT-4o significantly outperforms GPT-4o-mini on conceptual triggers (+40%) and content actions (+30%), but both models remain unreliable on structural triggers.

### False Positive Analysis
We observed an average of **~0.8 Lexical False Positives per rule** for GPT-4o. This indicates that models often "leak" conditional actions into parts of the text where the trigger was never present, suggesting that the rule becomes a "global bias" rather than a precise logical condition.

## Conclusions
LLMs' ability to follow conditional instructions is **not consistent**. Capacity is heavily weighted towards lexical patterns and falls off sharply for abstract or structural conditions. For reliable deployment, developers should prefer lexical triggers and formatting actions, while remaining cautious about "over-triggering" behaviors.

## Next Steps
- **Interference Analysis**: Test how performance degrades as the number of conditional rules increases (e.g., from 3 to 10).
- **Reasoning Models**: Evaluate if "System 2" models (e.g., o1) show better structural adherence.
- **Mitigation**: Develop prompting strategies (e.g., "Check-your-work" loops) specifically for conditional logic.
