import json
import os
from pathlib import Path

def convert_txt_to_json(input_dir="input", output_dir="output"):
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if not file.endswith('.txt'):
                continue

            input_path = Path(root) / file
            output_path = Path(output_dir) / input_path.relative_to(input_dir).with_suffix('.json')
            
            result = process_file(input_path)
            
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=4)

def process_file(file_path):
    data = {}
    current_section = None
    current_dict = {}
    current_list = []

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            
            if line.startswith('## '):
                if current_section:
                    finalize_section(data, current_section, current_dict, current_list)
                current_section = line[3:].strip()
                current_dict = {}
                current_list = []
                continue

            if ',' in line:
                key, _, value = line.partition(',')
                key = key.strip()
                value = value.strip()
                if key and value:
                    current_dict[key] = value
                continue

            if line:
                current_list.append(line)

        if current_section:
            finalize_section(data, current_section, current_dict, current_list)

    return data

def finalize_section(data, section, section_dict, section_list):
    if section_dict:
        data[section] = section_dict
    elif section_list:
        data[section] = section_list

if __name__ == "__main__":
    convert_txt_to_json()