from fastapi import FastAPI, HTTPException, Depends, Query
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import math
import uuid
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI(
    title="ForgetIT API",
    description="API implementing Memory Buoyancy and Preservation Value metrics from the ForgetIT project",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data models
class ResourceBase(BaseModel):
    title: str
    content_type: str = Field(..., description="Type of content e.g., 'document', 'image', 'email'")
    tags: List[str] = []
    context: Optional[Dict[str, Any]] = None

class ResourceCreate(ResourceBase):
    content: str = Field(..., description="Content or reference to content")

class ResourceResponse(ResourceBase):
    id: str
    content: str
    created_at: datetime
    last_accessed: datetime
    access_count: int = 0
    memory_buoyancy: float = 0.0
    preservation_value: float = 0.0
    
    class Config:
        orm_mode = True

class ResourceUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[List[str]] = None
    context: Optional[Dict[str, Any]] = None

class AccessLog(BaseModel):
    resource_id: str
    timestamp: datetime
    access_type: str = Field(..., description="Type of access e.g., 'view', 'edit', 'share'")

# In-memory database for demonstration purposes
resources_db: Dict[str, Dict] = {}
access_logs: List[Dict] = []

# Helper functions for calculating Memory Buoyancy and Preservation Value
def calculate_memory_buoyancy(resource: Dict) -> float:
    """
    Calculate Memory Buoyancy based on recency, frequency, and context
    
    Higher values mean the resource should be more accessible.
    """
    now = datetime.now()
    
    # Calculate recency factor (decreases with time since last access)
    time_diff = (now - resource["last_accessed"]).total_seconds() / 86400  # Convert to days
    recency_factor = math.exp(-0.1 * time_diff)  # Exponential decay
    
    # Calculate frequency factor (increases with more accesses)
    frequency_factor = min(1.0, resource["access_count"] / 10)  # Cap at 1.0
    
    # Calculate context importance factor (simplified)
    context_factor = 0.5  # Default value
    if resource["context"] and "importance" in resource["context"]:
        context_factor = resource["context"]["importance"]
    
    # Calculate tag relevance factor (simplified)
    tag_factor = min(1.0, len(resource["tags"]) / 5)  # More tags suggest more categorized/important
    
    # Combine factors (this is a simplified model)
    mb = (0.4 * recency_factor) + (0.3 * frequency_factor) + (0.2 * context_factor) + (0.1 * tag_factor)
    
    return min(1.0, max(0.0, mb))  # Ensure value is between 0 and 1

def calculate_preservation_value(resource: Dict) -> float:
    """
    Calculate Preservation Value based on content type, age, tags, and context
    
    Higher values mean the resource is more important for long-term preservation.
    """
    now = datetime.now()
    
    # Calculate age factor (older resources may have higher historical value)
    age_days = (now - resource["created_at"]).days
    age_factor = min(1.0, age_days / 365)  # Increases with age, caps at 1.0 after a year
    
    # Content type factor (some types may have inherently higher preservation value)
    content_type_factors = {
        "document": 0.7,
        "image": 0.8,
        "email": 0.5,
        "note": 0.4,
        "code": 0.6
    }
    content_type_factor = content_type_factors.get(resource["content_type"].lower(), 0.5)
    
    # Calculate context preservation factor
    preservation_factor = 0.5  # Default value
    if resource["context"] and "preservation_importance" in resource["context"]:
        preservation_factor = resource["context"]["preservation_importance"]
    
    # Tag-based factors (certain tags might indicate higher preservation value)
    preservation_tags = ["important", "archive", "historical", "reference"]
    tag_matches = sum(1 for tag in resource["tags"] if tag.lower() in preservation_tags)
    tag_factor = min(1.0, tag_matches / 2)  # Cap at 1.0
    
    # Combine factors
    pv = (0.3 * age_factor) + (0.2 * content_type_factor) + (0.3 * preservation_factor) + (0.2 * tag_factor)
    
    return min(1.0, max(0.0, pv))  # Ensure value is between 0 and 1

# Routes
@app.get("/")
def read_root():
    return {"message": "Welcome to the ForgetIT API", "version": "1.0.0"}

@app.post("/resources/", response_model=ResourceResponse)
def create_resource(resource: ResourceCreate):
    """Create a new resource with initial Memory Buoyancy and Preservation Value"""
    resource_id = str(uuid.uuid4())
    now = datetime.now()
    
    resource_dict = resource.dict()
    resource_dict.update({
        "id": resource_id,
        "created_at": now,
        "last_accessed": now,
        "access_count": 0
    })
    
    # Calculate initial metrics
    resource_dict["memory_buoyancy"] = calculate_memory_buoyancy(resource_dict)
    resource_dict["preservation_value"] = calculate_preservation_value(resource_dict)
    
    resources_db[resource_id] = resource_dict
    
    return resource_dict

@app.get("/resources/", response_model=List[ResourceResponse])
def list_resources(
    min_mb: Optional[float] = Query(None, ge=0.0, le=1.0, description="Minimum Memory Buoyancy"),
    min_pv: Optional[float] = Query(None, ge=0.0, le=1.0, description="Minimum Preservation Value"),
    sort_by: Optional[str] = Query("memory_buoyancy", description="Sort by field")
):
    """List resources with optional filtering by Memory Buoyancy and Preservation Value"""
    filtered_resources = list(resources_db.values())
    
    # Apply filters
    if min_mb is not None:
        filtered_resources = [r for r in filtered_resources if r["memory_buoyancy"] >= min_mb]
    
    if min_pv is not None:
        filtered_resources = [r for r in filtered_resources if r["preservation_value"] >= min_pv]
    
    # Sort resources
    if sort_by == "memory_buoyancy":
        filtered_resources.sort(key=lambda x: x["memory_buoyancy"], reverse=True)
    elif sort_by == "preservation_value":
        filtered_resources.sort(key=lambda x: x["preservation_value"], reverse=True)
    elif sort_by == "last_accessed":
        filtered_resources.sort(key=lambda x: x["last_accessed"], reverse=True)
    
    return filtered_resources

@app.get("/resources/{resource_id}", response_model=ResourceResponse)
def get_resource(resource_id: str):
    """Get a specific resource by ID and update its access metrics"""
    if resource_id not in resources_db:
        raise HTTPException(status_code=404, detail="Resource not found")
    
    resource = resources_db[resource_id]
    
    # Log the access
    access_log = {
        "resource_id": resource_id,
        "timestamp": datetime.now(),
        "access_type": "view"
    }
    access_logs.append(access_log)
    
    # Update resource metrics
    resource["last_accessed"] = access_log["timestamp"]
    resource["access_count"] += 1
    resource["memory_buoyancy"] = calculate_memory_buoyancy(resource)
    
    return resource

@app.put("/resources/{resource_id}", response_model=ResourceResponse)
def update_resource(resource_id: str, update_data: ResourceUpdate):
    """Update a resource and recalculate its metrics"""
    if resource_id not in resources_db:
        raise HTTPException(status_code=404, detail="Resource not found")
    
    resource = resources_db[resource_id]
    
    # Update fields
    update_dict = update_data.dict(exclude_unset=True)
    for field, value in update_dict.items():
        resource[field] = value
    
    # Log the access
    access_log = {
        "resource_id": resource_id,
        "timestamp": datetime.now(),
        "access_type": "edit"
    }
    access_logs.append(access_log)
    
    # Update resource metrics
    resource["last_accessed"] = access_log["timestamp"]
    resource["access_count"] += 1
    resource["memory_buoyancy"] = calculate_memory_buoyancy(resource)
    resource["preservation_value"] = calculate_preservation_value(resource)
    
    return resource

@app.delete("/resources/{resource_id}")
def delete_resource(resource_id: str):
    """Delete a resource"""
    if resource_id not in resources_db:
        raise HTTPException(status_code=404, detail="Resource not found")
    
    del resources_db[resource_id]
    
    return {"status": "success", "message": "Resource deleted"}

@app.get("/metrics/low-buoyancy", response_model=List[ResourceResponse])
def get_low_buoyancy_resources(threshold: float = Query(0.3, ge=0.0, le=1.0)):
    """Get resources with low Memory Buoyancy (candidates for managed forgetting)"""
    low_mb_resources = [r for r in resources_db.values() if r["memory_buoyancy"] < threshold]
    low_mb_resources.sort(key=lambda x: x["memory_buoyancy"])
    
    return low_mb_resources

@app.get("/metrics/archive-candidates", response_model=List[ResourceResponse])
def get_archive_candidates():
    """
    Get resources that are candidates for archiving:
    - Low Memory Buoyancy (not currently relevant)
    - High Preservation Value (worth preserving)
    """
    candidates = [
        r for r in resources_db.values() 
        if r["memory_buoyancy"] < 0.3 and r["preservation_value"] > 0.7
    ]
    candidates.sort(key=lambda x: x["preservation_value"], reverse=True)
    
    return candidates

@app.get("/metrics/deletion-candidates", response_model=List[ResourceResponse])
def get_deletion_candidates():
    """
    Get resources that are candidates for deletion:
    - Low Memory Buoyancy (not currently relevant)
    - Low Preservation Value (not worth preserving)
    """
    candidates = [
        r for r in resources_db.values() 
        if r["memory_buoyancy"] < 0.2 and r["preservation_value"] < 0.2
    ]
    candidates.sort(key=lambda x: (x["memory_buoyancy"] + x["preservation_value"]))
    
    return candidates

@app.post("/access-log")
def log_resource_access(log_entry: AccessLog):
    """Log a resource access event and update metrics"""
    if log_entry.resource_id not in resources_db:
        raise HTTPException(status_code=404, detail="Resource not found")
    
    # Add to access logs
    access_logs.append(log_entry.dict())
    
    # Update resource
    resource = resources_db[log_entry.resource_id]
    resource["last_accessed"] = log_entry.timestamp
    resource["access_count"] += 1
    resource["memory_buoyancy"] = calculate_memory_buoyancy(resource)
    
    return {"status": "success", "message": "Access logged", "resource_id": log_entry.resource_id}

@app.post("/update-metrics")
def update_all_metrics():
    """Update Memory Buoyancy and Preservation Value for all resources"""
    for resource_id, resource in resources_db.items():
        resource["memory_buoyancy"] = calculate_memory_buoyancy(resource)
        resource["preservation_value"] = calculate_preservation_value(resource)
    
    return {
        "status": "success", 
        "message": f"Updated metrics for {len(resources_db)} resources"
    }

# For testing purposes, if run directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
