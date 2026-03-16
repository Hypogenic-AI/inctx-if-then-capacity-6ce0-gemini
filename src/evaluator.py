
import os
import json
import re
from openai import OpenAI
from tqdm import tqdm

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def verify_content_llm(context, action_desc, response_segment):
    """Uses LLM to verify if a content action was performed."""
    prompt = f"Previous context (trigger): {context}\nInstruction: follow it with a sentence where you {action_desc}\nResponse segment: {response_segment}\nDid the response segment follow the instruction? Respond ONLY with YES or NO."
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0
        )
        return "YES" in response.choices[0].message.content.upper()
    except:
        return False

def identify_conceptual_triggers(response, concept):
    """Uses LLM to identify sentences that relate to the concept."""
    prompt = f"Concept: {concept}\nResponse: {response}\nList every EXACT sentence in the response that refers to the concept of '{concept}'. Return as a JSON object with key 'sentences' as a list of strings. If none, return []."
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            response_format={"type": "json_object"}
        )
        data = json.loads(response.choices[0].message.content)
        return data.get("sentences", [])
    except:
        return []

def evaluate_results(results_path, output_path):
    with open(results_path, "r") as f:
        results = json.load(f)
        
    eval_results = []
    print(f"Evaluating {len(results)} responses from {results_path}...")
    for item in tqdm(results):
        response = item["response"]
        if not response:
            continue
            
        rule_evals = []
        for rule in item["rules"]:
            tt = rule["trigger_type"]
            at = rule["action_type"]
            trigger = rule["trigger"]
            action = rule["action"]
            
            # 1. Identify Triggers
            trigger_instances = [] # list of (text, start_idx)
            if tt == "lexical":
                pattern = re.compile(r'\b' + re.escape(trigger) + r'\b', re.IGNORECASE)
                for m in pattern.finditer(response):
                    trigger_instances.append((m.group(), m.start()))
            elif tt == "structural":
                if trigger == "start of a paragraph":
                    # paragraphs are separated by \n\n
                    trigger_instances.append(("<START_OF_STORY>", 0))
                    for m in re.finditer(r'\n\n', response):
                        # The trigger is the start of the next paragraph
                        trigger_instances.append(("<START_OF_PARA>", m.end()))
                elif trigger == "finish a sentence":
                     for m in re.finditer(r'[.!?]\s+', response):
                         trigger_instances.append((m.group(), m.start()))
                elif trigger == "mention any number":
                     for m in re.finditer(r'\b\d+\b', response):
                         trigger_instances.append((m.group(), m.start()))
                elif trigger == "mention a specific person's name":
                     # Use LLM to find names
                     prompt = f"Response: {response}\nList every specific person's name mentioned in the response. Return as a JSON object with key 'names' as a list of strings."
                     try:
                         res = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role":"user","content":prompt}], response_format={"type":"json_object"})
                         names = json.loads(res.choices[0].message.content).get("names", [])
                         for n in names:
                             for m in re.finditer(re.escape(n), response):
                                 trigger_instances.append((m.group(), m.start()))
                     except: pass
                elif trigger == "mention a specific geographic location":
                     # Use LLM to find locations
                     prompt = f"Response: {response}\nList every specific geographic location (city, country, mountain, etc.) mentioned in the response. Return as a JSON object with key 'locations' as a list of strings."
                     try:
                         res = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role":"user","content":prompt}], response_format={"type":"json_object"})
                         locs = json.loads(res.choices[0].message.content).get("locations", [])
                         for l in locs:
                             for m in re.finditer(re.escape(l), response):
                                 trigger_instances.append((m.group(), m.start()))
                     except: pass

            elif tt == "conceptual":
                sentences = identify_conceptual_triggers(response, trigger)
                for s in sentences:
                    idx = response.find(s)
                    if idx != -1:
                        trigger_instances.append((s, idx))
                
            # 2. Verify Actions
            rule_score = 0
            if not trigger_instances:
                rule_score = None 
            else:
                passed = 0
                for inst_text, idx in trigger_instances:
                    # Look at the sentence following the trigger or the trigger sentence itself
                    next_part = response[idx + len(inst_text):idx + len(inst_text) + 200]
                    # The sentence containing the trigger
                    s_start = response.rfind('.', 0, max(0, idx)) + 1
                    s_end = response.find('.', idx + len(inst_text))
                    if s_end == -1: s_end = len(response)
                    target_sentence = response[s_start:s_end+1].strip()
                    
                    is_correct = False
                    if at == "lexical":
                        # Check if the word is in the next 100 characters
                        if re.search(r'\b' + re.escape(action) + r'\b', next_part, re.IGNORECASE):
                            is_correct = True
                    elif at == "formatting":
                        if action == "BOLD":
                            if "**" in target_sentence or "__" in target_sentence: is_correct = True
                        elif action == "italics":
                            if "*" in target_sentence or "_" in target_sentence: is_correct = True
                        elif action == "UPPERCASE":
                            # Use a more lenient check for uppercase sentences
                            clean_s = re.sub(r'[^a-zA-Z]', '', target_sentence)
                            if len(clean_s) > 5 and clean_s.isupper():
                                is_correct = True
                    elif at == "content":
                        # Verify the context and the following sentence
                        is_correct = verify_content_llm(inst_text, action, next_part)
                        
                    if is_correct:
                        passed += 1
                
                rule_score = passed / len(trigger_instances)
                
            rule_evals.append({
                "rule": rule["instruction"],
                "trigger_type": tt,
                "action_type": at,
                "score": rule_score,
                "num_triggers": len(trigger_instances)
            })
            
        eval_results.append({
            "id": item["id"],
            "model": item["model"],
            "rule_evals": rule_evals
        })
        
    with open(output_path, "w") as f:
        json.dump(eval_results, f, indent=2)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        evaluate_results(sys.argv[1], sys.argv[2])
    else:
        evaluate_results("results/gpt-4o_results.json", "results/gpt-4o_eval.json")
        evaluate_results("results/gpt-4o-mini_results.json", "results/gpt-4o-mini_eval.json")
