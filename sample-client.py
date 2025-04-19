import requests
import json
from datetime import datetime
import time

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
    
    # Clear any existing resources first
    try:
        existing_resources = requests.get(f"{BASE_URL}/resources/").json()
        for resource in existing_resources:
            requests.delete(f"{BASE_URL}/resources/{resource['id']}")
        print(f"Cleared {len(existing_resources)} existing resources")
    except Exception as e:
        print(f"Error clearing existing resources: {e}")
    
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
        print(f"{'Title':<40} {'MB':<10} {'PV':<10} {'Access Count':<15}")
        print("-" * 80)
        for resource in resources:
            print(f"{resource['title']:<40} {resource['memory_buoyancy']:<10.2f} {resource['preservation_value']:<10.2f} {resource['access_count']:<15}")
    else:
        print(f"Failed to get resources: {response.text}")

def check_managed_forgetting_recommendations():
    """Get recommendations for managed forgetting actions"""
    # Archive candidates (low MB, high PV)
    response = requests.get(f"{BASE_URL}/metrics/archive-candidates")
    if response.status_code == 200:
        candidates = response.json()
        if candidates:
            print("\nArchive Candidates (Low relevance but high preservation value):")
            for candidate in candidates:
                print(f"- {candidate['title']} (MB: {candidate['memory_buoyancy']:.2f}, PV: {candidate['preservation_value']:.2f})")
        else:
            print("\nNo archive candidates found")
    
    # Deletion candidates (low MB, low PV)
    response = requests.get(f"{BASE_URL}/metrics/deletion-candidates")
    if response.status_code == 200:
        candidates = response.json()
        if candidates:
            print("\nDeletion Candidates (Low relevance and low preservation value):")
            for candidate in candidates:
                print(f"- {candidate['title']} (MB: {candidate['memory_buoyancy']:.2f}, PV: {candidate['preservation_value']:.2f})")
        else:
            print("\nNo deletion candidates found")

def demonstrate_intelligent_condensation():
    """Demonstrate the concept of intelligent condensation based on Memory Buoyancy"""
    response = requests.get(f"{BASE_URL}/resources/")
    if response.status_code == 200:
        resources = response.json()
        
        print("\nIntelligent Condensation Simulation:")
        print("-" * 80)
        print("Resources arranged by access priority and condensation level:")
        
        # Sort resources by memory buoyancy
        resources.sort(key=lambda x: x["memory_buoyancy"], reverse=True)
        
        for i, resource in enumerate(resources):
            mb = resource["memory_buoyancy"]
            
            # Simulate different levels of condensation based on MB value
            if mb > 0.8:
                condensation = "FULL ACCESS - Complete content readily available"
                detail_level = "All details preserved"
            elif mb > 0.6:
                condensation = "PARTIAL CONDENSATION - Important elements highlighted"
                detail_level = "Most details preserved, non-essential elements minimized"
            elif mb > 0.4:
                condensation = "SIGNIFICANT CONDENSATION - Summary view available"
                detail_level = "Core content preserved, details available on demand"
            elif mb > 0.2:
                condensation = "HEAVY CONDENSATION - Metadata and brief overview only"
                detail_level = "Only key points and context preserved"
            else:
                condensation = "ARCHIVED - Reference information only"
                detail_level = "Minimal information preserved, mainly for contextual reference"
            
            print(f"\n{i+1}. {resource['title']} (MB: {mb:.2f}, PV: {resource['preservation_value']:.2f})")
            print(f"   Access Level: {condensation}")
            print(f"   Detail Preservation: {detail_level}")
            
            # Simulate content preview based on condensation level
            content = resource['content']
            if mb > 0.8:
                preview = content
            elif mb > 0.6:
                if len(content) > 100:
                    preview = content[:100] + "... [additional details available]"
                else:
                    preview = content
            elif mb > 0.4:
                if len(content) > 50:
                    preview = content[:50] + "... [condensed]"
                else:
                    preview = content
            elif mb > 0.2:
                preview = f"[Condensed content: {len(content)} characters]"
            else:
                preview = "[Archived content - reference only]"
                
            print(f"   Content Preview: {preview}")

def demonstrate_contextual_organization():
    """Demonstrate contextual organization of resources"""
    response = requests.get(f"{BASE_URL}/resources/")
    if response.status_code == 200:
        resources = response.json()
        
        print("\nContextual Organization Simulation:")
        print("-" * 80)
        
        # Build a simplified semantic context graph
        contexts = {}
        
        # Group by tags (simplified semantic clustering)
        tag_groups = {}
        for resource in resources:
            for tag in resource["tags"]:
                if tag not in tag_groups:
                    tag_groups[tag] = []
                tag_groups[tag].append(resource)
        
        # Show tag-based organization
        print("Tag-Based Clusters:")
        for tag, items in tag_groups.items():
            if len(items) > 1:  # Only show meaningful clusters
                print(f"\n  [{tag.upper()}] Related Resources:")
                for item in items:
                    print(f"    - {item['title']} (MB: {item['memory_buoyancy']:.2f}, PV: {item['preservation_value']:.2f})")
        
        # Content type organization
        print("\nContent Type Organization:")
        type_groups = {}
        for resource in resources:
            content_type = resource["content_type"]
            if content_type not in type_groups:
                type_groups[content_type] = []
            type_groups[content_type].append(resource)
        
        for content_type, items in type_groups.items():
            print(f"\n  [{content_type.upper()}] Resources:")
            for item in items:
                print(f"    - {item['title']} (MB: {item['memory_buoyancy']:.2f}, PV: {item['preservation_value']:.2f})")
        
        # Temporal organization (simulation - in real system would use actual timestamps)
        print("\nTemporal Organization:")
        print("  [RECENT] Frequently accessed resources:")
        for resource in sorted(resources, key=lambda x: x["memory_buoyancy"], reverse=True)[:2]:
            print(f"    - {resource['title']} (Last accessed: recently, Access count: {resource['access_count']})")
        
        print("\n  [HISTORICAL] Infrequently accessed but preserved resources:")
        for resource in sorted(resources, key=lambda x: x["preservation_value"] - x["memory_buoyancy"], reverse=True)[:2]:
            print(f"    - {resource['title']} (Access count: {resource['access_count']}, Preservation value: {resource['preservation_value']:.2f})")

def main():
    """Run a sample workflow demonstrating ForgetIT concepts"""
    print("Creating sample resources...")
    resources = create_sample_resources()
    
    # Give the server a moment to process
    time.sleep(1)
    
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
    
    # Demonstrate intelligent condensation
    demonstrate_intelligent_condensation()
    
    # Demonstrate contextual organization
    demonstrate_contextual_organization()

if __name__ == "__main__":
    main()
