
import os
import json
from openai import OpenAI
from tqdm import tqdm

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def run_model(model_name, bench_path, output_path):
    with open(bench_path, "r") as f:
        bench = json.load(f)
        
    results = []
    print(f"Running model {model_name} on {len(bench)} test cases...")
    for item in tqdm(bench):
        prompt = item["full_prompt"]
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0
            )
            output = response.choices[0].message.content
        except Exception as e:
            print(f"Error running {model_name} on {item['id']}: {e}")
            output = None
            
        results.append({
            "id": item["id"],
            "model": model_name,
            "prompt": prompt,
            "response": output,
            "rules": item["rules"]
        })
        
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    # Run GPT-4o
    run_model("gpt-4o", "datasets/condif_bench.json", "results/gpt-4o_results.json")
    # Run GPT-4o-mini
    run_model("gpt-4o-mini", "datasets/condif_bench.json", "results/gpt-4o-mini_results.json")
