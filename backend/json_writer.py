import json

def save_knowledge_base(data, filename="knowledge_base.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
