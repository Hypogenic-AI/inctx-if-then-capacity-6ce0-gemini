
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def analyze_eval(eval_path, model_name):
    with open(eval_path, "r") as f:
        data = json.load(f)
        
    all_rules = []
    for item in data:
        for reval in item["rule_evals"]:
            if reval["score"] is not None:
                all_rules.append({
                    "id": item["id"],
                    "model": model_name,
                    "trigger_type": reval["trigger_type"],
                    "action_type": reval["action_type"],
                    "score": reval["score"],
                    "num_triggers": reval["num_triggers"]
                })
                
    df = pd.DataFrame(all_rules)
    return df

def main():
    df_4o = analyze_eval("results/gpt-4o_eval.json", "gpt-4o")
    df_mini = analyze_eval("results/gpt-4o-mini_eval.json", "gpt-4o-mini")
    
    df = pd.concat([df_4o, df_mini])
    
    # Summary by Model and Trigger Type
    summary_trigger = df.groupby(["model", "trigger_type"])["score"].mean().unstack()
    print("Summary by Trigger Type:")
    print(summary_trigger)
    
    # Summary by Model and Action Type
    summary_action = df.groupby(["model", "action_type"])["score"].mean().unstack()
    print("\nSummary by Action Type:")
    print(summary_action)
    
    # Plotting
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df, x="trigger_type", y="score", hue="model")
    plt.title("Conditional Adherence Score by Trigger Type")
    plt.ylim(0, 1.1)
    plt.savefig("figures/trigger_comparison.png")
    
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df, x="action_type", y="score", hue="model")
    plt.title("Conditional Adherence Score by Action Type")
    plt.ylim(0, 1.1)
    plt.savefig("figures/action_comparison.png")
    
    # Matrix of Trigger x Action
    matrix = df[df["model"] == "gpt-4o"].groupby(["trigger_type", "action_type"])["score"].mean().unstack()
    plt.figure(figsize=(8, 6))
    sns.heatmap(matrix, annot=True, cmap="YlGnBu", vmin=0, vmax=1)
    plt.title("GPT-4o Performance Matrix (Trigger x Action)")
    plt.savefig("figures/gpt4o_matrix.png")
    
    # Num Triggers vs Score
    plt.figure(figsize=(10, 6))
    sns.regplot(data=df[df["model"] == "gpt-4o"], x="num_triggers", y="score")
    plt.title("GPT-4o: Number of Triggers vs. Adherence Score")
    plt.savefig("figures/num_triggers_vs_score.png")
    
    # Correlation between Trigger Types (per prompt)
    pivot_trigger = df[df["model"] == "gpt-4o"].pivot_table(index="id", columns="trigger_type", values="score", aggfunc='mean')
    corr_trigger = pivot_trigger.corr()
    print("\nCorrelation between Trigger Types (GPT-4o):")
    print(corr_trigger)
    
    # Correlation between Action Types (per prompt)
    pivot_action = df[df["model"] == "gpt-4o"].pivot_table(index="id", columns="action_type", values="score", aggfunc='mean')
    corr_action = pivot_action.corr()
    print("\nCorrelation between Action Types (GPT-4o):")
    print(corr_action)

if __name__ == "__main__":
    main()
