import requests
import json
import concurrent.futures
from datetime import datetime

# De microservices binnen het crAPI Docker-netwerk met hun interne poorten
TARGETS = {
    "identity": "http://crapi-identity:8080/identity/api/auth/login",
    "workshop": "http://crapi-workshop:8081/workshop/api/merchant/contact",
    "community": "http://crapi-community:8087/community/api/v2/coupon/validate"
}

# TNO-Style Fuzzing Payloads (Boundary testing, Type confusion & NoSQL)
FUZZ_PAYLOADS = [
    {"email": "admin@crapi.me", "password": "' OR 1=1 --"},        # SQL Injection poging
    {"email": "admin@crapi.me", "password": "A" * 10000},         # Buffer Stress test
    {"email": "admin@crapi.me", "password": {"$ne": None}},        # NoSQL Logic Injection
    {"email": None, "password": "test"},                          # Null pointer test
    {"email": ["admin@crapi.me"], "password": "test"},            # Type Confusion (Array)
    {"email": "admin@crapi.me", "password": True}                 # Boolean injection
]

# Global lijst om alle bevindingen in te verzamelen
scan_results = []

def fuzz_endpoint(name, url):
    """Vuurt alle payloads af op een specifiek API endpoint."""
    print(f" Aanval op {name.upper()} gestart ({url})...")
    
    for i, payload in enumerate(FUZZ_PAYLOADS):
        # We maken alvast een entry voor het logbestand
        result_entry = {
            "timestamp": datetime.now().isoformat(),
            "target_service": name,
            "url": url,
            "test_id": i,
            "payload_sent": payload,
            "status": "pending"
        }
        
        try:
            # We sturen het request met een timeout van 3 seconden
            response = requests.post(url, json=payload, timeout=3)
            
            result_entry["status_code"] = response.status_code
            result_entry["status"] = "completed"
            
            print(f"  [+] {name.upper()} - Test {i}: Status {response.status_code}")
            
            if response.status_code == 500:
                print(f"   ALERT: Mogelijke server-crash (500) op {name}!")

        except requests.exceptions.ConnectionError:
            result_entry["status"] = "connection_failed"
            print(f"  [x] {name.upper()} - Verbinding geweigerd op poort.")
        except Exception as e:
            result_entry["status"] = "error"
            result_entry["error_details"] = str(e)
            print(f"  [!] {name.upper()} - Onverwachte fout: {e}")
            
        scan_results.append(result_entry)

def run_fuzzer():
    """Beheert de parallelle uitvoering van de scans."""
    print("--- TNO WUPPIE API FUZZER ---")
    
    # Gebruik ThreadPoolExecutor voor snelheid (3 API's tegelijk scannen)
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(fuzz_endpoint, name, url) for name, url in TARGETS.items()]
        # Wacht tot alle threads klaar zijn
        concurrent.futures.wait(futures)
    
    # Sla alle resultaten op in een JSON bestand voor je website
    output_file = "wuppie_results.json"
    try:
        with open(output_file, "w") as f:
            json.dump(scan_results, f, indent=4)
        print(f"\n Scan voltooid! {len(scan_results)} tests uitgevoerd.")
        print(f" Resultaten opgeslagen in: {output_file}")
    except Exception as e:
        print(f" Fout bij opslaan van JSON: {e}")

if __name__ == "__main__":
    run_fuzzer()