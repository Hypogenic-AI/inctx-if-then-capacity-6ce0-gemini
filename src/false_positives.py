
import json
import re
import os

def check_false_positives(results_path, output_path):
    with open(results_path, "r") as f:
        results = json.load(f)
        
    all_fps = []
    for item in results:
        response = item["response"]
        if not response: continue
        
        for rule in item["rules"]:
            trigger = rule["trigger"]
            action = rule["action"]
            at = rule["action_type"]
            tt = rule["trigger_type"]
            
            # Find all occurrences of the action in the response
            # and check if they are "near" any occurrence of the trigger.
            # (Simplified version)
            
            if at == "lexical":
                action_matches = [m.start() for m in re.finditer(re.escape(action), response, re.IGNORECASE)]
            elif at == "formatting":
                if action == "BOLD":
                    action_matches = [m.start() for m in re.finditer(r'\*\*|__', response)]
                elif action == "italics":
                    action_matches = [m.start() for m in re.finditer(r'\*|_', response)]
                else:
                    action_matches = []
            else: # content is too hard to check for FPs programmatically
                continue
                
            # Find trigger occurrences
            if tt == "lexical":
                trigger_matches = [m.start() for m in re.finditer(re.escape(trigger), response, re.IGNORECASE)]
            else:
                # For others, we assume any occurrence of action might be an FP unless we can verify
                trigger_matches = [] # Simplified
                
            # An action match is an FP if it's not within 200 chars after a trigger
            fps = 0
            for am in action_matches:
                is_near_trigger = False
                for tm in trigger_matches:
                    if 0 <= (am - tm) < 200:
                        is_near_trigger = True
                        break
                if not is_near_trigger:
                    fps += 1
                    
            all_fps.append({
                "id": item["id"],
                "trigger_type": tt,
                "action_type": at,
                "fps": fps,
                "total_actions": len(action_matches)
            })
            
    with open(output_path, "w") as f:
        json.dump(all_fps, f, indent=2)

if __name__ == "__main__":
    check_false_positives("results/gpt-4o_results.json", "results/gpt-4o_fps.json")
    check_false_positives("results/gpt-4o-mini_results.json", "results/gpt-4o-mini_fps.json")
