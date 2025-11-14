#!/usr/bin/env python3
"""
Convert all JSONL files to a single combined JSON file for deployment.
This makes the web app load faster by requiring only 1 HTTP request instead of 6.
"""

import json
from pathlib import Path

def load_jsonl(filepath):
    """Load a JSONL file and return list of objects."""
    data = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                data.append(json.loads(line))
    return data

def main():
    # Define paths
    data_dir = Path(__file__).parent.parent / 'NVE_DATA'
    output_file = Path(__file__).parent / 'vannkraft-data.json'

    # Create output directory if it doesn't exist
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Load all JSONL files
    print("Loading JSONL files...")
    combined_data = {
        'vannkraftverk': load_jsonl(data_dir / 'vannkraftverk.jsonl'),
        'dammer': load_jsonl(data_dir / 'dammer.jsonl'),
        'magasiner': load_jsonl(data_dir / 'magasiner.jsonl'),
        'vannveier': load_jsonl(data_dir / 'vannveier.jsonl'),
        'inntakspunkt': load_jsonl(data_dir / 'inntakspunkt.jsonl'),
        'utlopspunkt': load_jsonl(data_dir / 'utlopspunkt.jsonl')
    }

    # Print statistics
    print("\nData loaded:")
    for key, value in combined_data.items():
        print(f"  {key}: {len(value):,} items")

    # Write combined JSON file
    print(f"\nWriting combined JSON to: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(combined_data, f, ensure_ascii=False, separators=(',', ':'))

    # Print file size
    file_size_mb = output_file.stat().st_size / (1024 * 1024)
    print(f"✓ Done! File size: {file_size_mb:.2f} MB")
    print(f"\nDeploy these files to Azure Static Web Apps:")
    print(f"  - index_vann.html")
    print(f"  - vannkraft-data.json")

if __name__ == '__main__':
    main()
