from collections import Counter
from aurora.config.paths import state_path, important_updates_path
import json
from aurora.responses import low_severity, medium_severity, high_severity, critical_severty
import random

RISK_ORDER = {
    "low": 1,
    "medium": 2,
    "high": 3,
    "critical": 4,
    }

def find_highest_risk(lst):
    
    risks = []
    for item in lst:
        risk = item["risk"]
        if risk not in risks:
            risks.append(risk)
    highest = max(risks, key=lambda r: RISK_ORDER[r])
    return highest
    

def aurora_status() -> None:
    with open(important_updates_path, "r", encoding="utf-8") as f:
        dist = json.load(f)
    with open(state_path, "r") as f:
        updateable_packages = int(f.read().strip())
    important_updates = dist.get("important_updates", [])
    
    print(f"Updates: {updateable_packages}")
    risk_level = find_highest_risk(important_updates)
    print(f"Severity: {risk_level}")
    
    affected_areas = []
    for item in important_updates:
        category = item["category"]
        if category not in affected_areas:
            affected_areas.append(category)
    areas = ", ".join(affected_areas)
    print(f"Affected Areas: {areas}")
    
    if risk_level == "low":
        recomendation = random.choice(low_severity)
    elif risk_level == "medium":
        recomendation = random.choice(medium_severity)
    elif risk_level == "high":
        recomendation = random.choice(high_severity)
    elif risk_level == "critical":
        recomendation = random.choice(critical_severty)
    
    print(f"Recomendation: {recomendation}")
        
   
        
    
   
   
if __name__ == "__main__":
    aurora_status()