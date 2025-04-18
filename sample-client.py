import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def create_sample_resources():
    """Create some sample resources with different characteristics"""
    resources = [
        {
            "title": "Important Project Documentation",
            "content_type": "document",
            "content": "This is a detailed documentation of an important project.",
            "tags": ["project", "documentation", "important", "reference"],
            "context": {
                "importance": 0.9,
                "preservation_importance": 0.8
            }
        },
        {
            "title": "Meeting Notes - Weekly Standup",
            "content_type": "document",
            "content": "Notes from the weekly standup meeting discussing routine tasks.",
            "tags": ["meeting", "notes", "routine"],
            "context": {
                "importance": 0.4,
                "preservation_importance": 0.2
            }
        },
        {
            "title": "Family Vacation Photo",
            "content_type": "image",
            "content": "reference://photos/family_vacation.jpg",
            "tags": ["photo", "vacation", "family", "memories"],
            "context": {
                "importance": 0.7,
                "preservation_importance": 0.9
            }
        },
        {
            "title": "Shopping List",
            "content_type": "note",
            "content": "Milk, eggs, bread, cheese, apples",
            "tags": ["shopping", "temporary"],
            "context": {
                "importance": 0.3,
                "preservation_importance": 0.1
            }
        },
        {
            "title": "Code Snippet - API Implementation",
            "content_type": "code",
            "content": "def example_function():\n    return 'Hello World'",
            "tags": ["code", "api", "reference"],
            "context": {
                "importance": 0.8,
                "preservation_importance": 0.7
            }
        }
    ]
    
    created_resources = []
    for resource in resources:
        response = requests.post(f"{BASE_URL}/resources/", json=resource)
        if response.status_code == 200:
            created_resources.append(response.json())
            print(f"Created resource: {response.json()['title']}")
        else:
            print(f"Failed to create resource: {response.text}")
    
    return created_resources

def simulate_resource_access(resources, access_patterns):
    """Simulate access patterns to resources to affect their Memory Buoyancy"""
    for resource_id, access_count in access_patterns.items():
        for _ in range(access_count):
            log_data = {
                "resource_id": resource_id,
                "timestamp": datetime.now().isoformat(),
                "access_type": "view"
            }
            response = requests.post(f"{BASE_URL}/access-log", json=log_data)
            if response.status_code != 200:
                print(f"Failed to log access: {response.text}")
    
    # Update all metrics
    requests.post(f"{BASE_URL}/update-metrics")
    print("Updated all resource metrics")

def check_metrics():
    """Check current metrics for all resources"""
    response = requests.get(f"{BASE_URL}/resources/")
    if response.status_code == 200:
        resources = response.json()
        print("\nCurrent Resource Metrics:")
        print("-" * 80)
        print(f"{'Title':<40} {'MB':<10} {'PV':<10}")
        print("-" * 80)
        for resource in resources:
            print(f"{resource['title']:<40} {resource['memory_buoyancy']:<10.2f} {resource['preservation_value']:<10.2f}")
    else:
        print(f"Failed to get resources: {response.text}")

def check_managed_forgetting_recommendations():
    """Get recommendations for managed forgetting actions"""
    # Archive candidates (low MB, high PV)
    response = requests.get(f"{BASE_URL}/metrics/archive-candidates")
    if response.status_code == 200:
        candidates = response.json()
        print("\nArchive Candidates (Low relevance but high preservation value):")
        for candidate in candidates:
            print(f"- {candidate['title']} (MB: {candidate['memory_buoyancy']:.2f}, PV: {candidate['preservation_value']:.2f})")
    
    # Deletion candidates (low MB, low PV)
    response = requests.get(f"{BASE_URL}/metrics/deletion-candidates")
    if response.status_code == 200:
        candidates = response.json()
        print("\nDeletion Candidates (Low relevance and low preservation value):")
        for candidate in candidates:
            print(f"- {candidate['title']} (MB: {candidate['memory_buoyancy']:.2f}, PV: {candidate['preservation_value']:.2f})")

def main():
    """Run a sample workflow demonstrating ForgetIT concepts"""
    print("Creating sample resources...")
    resources = create_sample_resources()
    
    # Get resource IDs
    resource_ids = {r["title"]: r["id"] for r in resources}
    
    # Check initial metrics
    check_metrics()
    
    # Simulate different access patterns
    print("\nSimulating access patterns...")
    access_patterns = {
        resource_ids["Code Snippet - API Implementation"]: 10,  # Frequently accessed
        resource_ids["Meeting Notes - Weekly Standup"]: 1,     # Rarely accessed
        resource_ids["Family Vacation Photo"]: 5,              # Occasionally accessed
        resource_ids["Important Project Documentation"]: 7,    # Regularly accessed
        resource_ids["Shopping List"]: 0                       # Not accessed after creation
    }
    simulate_resource_access(resources, access_patterns)
    
    # Check updated metrics
    check_metrics()
    
    # Get managed forgetting recommendations
    check_managed_forgetting_recommendations()

if __name__ == "__main__":
    main()
