from pathlib import Path
import yaml

BASE_DIR = Path(__file__).resolve().parents[1]

def load_yaml(file_path):
    yaml_path = BASE_DIR / file_path
    
    with open(yaml_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)
    