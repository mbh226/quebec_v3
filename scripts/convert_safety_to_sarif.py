import json
import sys

def convert_safety_to_sarif(safety_json, sarif_file):
    #read json results of safety scan from workflow
    with open(safety_json, 'r') as f:
        safety_data = json.load(f)
    
    #setting up the data structure to hold the results of the safety scan
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
    
    #converting the results of safety scan to sarif format
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
                            "startLine": 1  
                        }
                    }
                }
            ],
            "severity": issue['severity'].upper() if 'severity' in issue else "LOW"
        })
    
    #write the data into the the sarif file that will get uploaded
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
