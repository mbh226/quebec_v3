import json
import sys

def convert_safety_to_sarif(safety_json, sarif_file):
    # Read the Safety JSON output
    with open(safety_json, 'r') as f:
        safety_data = json.load(f)
    
    # Initialize SARIF data structure
    sarif_data = {
        "version": "2.1.0",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "Safety",
                        "version": "1.0"
                    }
                },
                "results": []
            }
        ]
    }
    
    # Convert each Safety result into a SARIF result
    for issue in safety_data.get('vulnerabilities', []):
        sarif_data['runs'][0]['results'].append({
            "ruleId": issue['vuln_id'],
            "message": {
                "text": issue['description']
            },
            "locations": [
                {
                    "physicalLocation": {
                        "artifactLocation": {
                            "uri": issue['package_name']
                        },
                        "region": {
                            "startLine": 1  # Assuming all issues are reported at the start of the file
                        }
                    }
                }
            ],
            "severity": issue['severity'].upper() if 'severity' in issue else "LOW"
        })
    
    # Write SARIF output
    with open(sarif_file, 'w') as f:
        json.dump(sarif_data, f, indent=2)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python convert_safety_to_sarif.py <input_json> <output_sarif>")
        sys.exit(1)

    safety_json = sys.argv[1]
    sarif_file = sys.argv[2]
    
    convert_safety_to_sarif(safety_json, sarif_file)
    print(f"Converted Safety results to SARIF and saved to {sarif_file}")
