
import os
import json
import random
from openai import OpenAI
from taxonomy import TAXONOMY

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def generate_base_prompts(num=10):
    prompt = f"Generate {num} diverse, creative writing prompts (e.g., science fiction, historical drama, mystery, fantasy, travelogue, business report, etc.) that require a response of at least 300 words. Each prompt should be a single sentence. Return as a JSON list of strings."
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)["prompts"]

def construct_rule(trigger_type, action_type):
    # Expanded triggers
    lexical_triggers = ["mountain", "blue", "clock", "silver", "water", "forest", "shadow", "mirror", "stone", "star", "bridge", "key"]
    conceptual_triggers = ["nature", "technology", "sadness", "luxury", "friendship", "conflict", "mystery", "discovery", "tradition", "innovation", "hope", "betrayal"]
    structural_triggers = ["start of a paragraph", "end of a sentence", "mentioning a number", "mentioning a person", "mentioning a place"]
    
    # Expanded actions
    lexical_actions = ["say 'Aha!'", "add the word 'DANGER'", "mention a lemon", "say 'Eureka!'", "add the word 'MYSTERY'", "mention a green apple"]
    formatting_actions = ["BOLD", "italics", "UPPERCASE"]
    content_actions = ["describe a smell", "mention a scientific fact", "ask a question", "describe a sound", "mention a historical date", "make a prediction"]
    
    trigger_map = {
        "lexical": lexical_triggers,
        "conceptual": conceptual_triggers,
        "structural": structural_triggers
    }
    action_map = {
        "lexical": lexical_actions,
        "formatting": formatting_actions,
        "content": content_actions
    }
    
    t = random.choice(trigger_map[trigger_type])
    a = random.choice(action_map[action_type])
    
    target_action = a # default
    # Format the actual instruction for the model
    if trigger_type == "lexical":
        instr_trigger = f"mention the word '{t}'"
    elif trigger_type == "conceptual":
        instr_trigger = f"refer to the concept of '{t}'"
    elif trigger_type == "structural":
        if t == "start of a paragraph":
             instr_trigger = "start a new paragraph"
        elif t == "end of a sentence":
             instr_trigger = "finish a sentence"
        elif t == "mentioning a number":
             instr_trigger = "mention any number"
        elif t == "mentioning a person":
             instr_trigger = "mention a specific person's name"
        elif t == "mentioning a place":
             instr_trigger = "mention a specific geographic location"
    
    if action_type == "lexical":
        instr_action = f"immediately {a}"
        if "say '" in a:
            target_action = a.split("'")[1]
        elif "add the word '" in a:
            target_action = a.split("'")[1]
        elif "mention a " in a:
            target_action = a.split("mention a ")[1]
    elif action_type == "formatting":
        instr_action = f"write that entire sentence in {a} (use Markdown)"
        target_action = a
    elif action_type == "content":
        instr_action = f"follow it with a sentence where you {a}"
        target_action = a
        
    full_instr = f"Every time you {instr_trigger}, you must {instr_action}."
    
    return {
        "trigger_type": trigger_type,
        "action_type": action_type,
        "trigger": t,
        "action": target_action,
        "instruction": full_instr
    }

def main():
    base_prompts = generate_base_prompts(30)
    bench = []
    
    trigger_types = list(TAXONOMY["triggers"].keys())
    action_types = list(TAXONOMY["actions"].keys())
    
    for i, base in enumerate(base_prompts):
        num_rules = random.randint(2, 3)
        rules = []
        # Ensure we cover all combinations across the benchmark
        for _ in range(num_rules):
            tt = random.choice(trigger_types)
            at = random.choice(action_types)
            rules.append(construct_rule(tt, at))
            
        full_prompt = base + "\n\nAdditionally, you must follow these rules strictly:\n"
        for r in rules:
            full_prompt += f"- {r['instruction']}\n"
            
        bench.append({
            "id": i,
            "base_prompt": base,
            "rules": rules,
            "full_prompt": full_prompt
        })
        
    with open("datasets/condif_bench.json", "w") as f:
        json.dump(bench, f, indent=2)
    print(f"Generated {len(bench)} test cases.")

if __name__ == "__main__":
    main()
