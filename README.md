# ForgetIT API

A practical implementation of the ForgetIT project's Memory Buoyancy and Preservation Value concepts, designed to help digital systems learn to forget intelligently.

## About

ForgetIT proposes that digital systems should mimic the beneficial aspects of human memory by intelligently "forgetting" information based on relevance and preservation value, rather than storing everything indiscriminately. This API implements two core metrics:

- **Memory Buoyancy (MB)**: Measures how accessible information should be based on current relevance, usage patterns, and context
- **Preservation Value (PV)**: Determines the long-term importance of information for archiving purposes

These metrics allow systems to make nuanced information management decisions beyond simple "keep or delete" binaries.

## Features

- Create, read, update, and delete resources with automatic MB and PV calculations
- Track resource access patterns to dynamically update Memory Buoyancy
- Identify candidates for archiving (low MB, high PV) or deletion (low MB, low PV)
- Filter and sort resources based on their metrics
- Simple in-memory implementation for demonstration purposes

## Getting Started

### Prerequisites

- Python 3.7+
- FastAPI
- Uvicorn
- Pydantic
- Python-dateutil

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/forgetit.git
cd forgetit

# Install dependencies
pip install -r requirements.txt
```

### Usage

1. Start the API server:

```bash
uvicorn forgetit-api:app --reload
```

2. The API will be available at http://localhost:8000
3. Access the interactive API documentation at http://localhost:8000/docs

4. Run the sample client to see ForgetIT concepts in action:

```bash
python sample-client.py
```

## API Endpoints

- `GET /resources/`: List all resources with optional filtering
- `POST /resources/`: Create a new resource
- `GET /resources/{resource_id}`: Get a specific resource
- `PUT /resources/{resource_id}`: Update a resource
- `DELETE /resources/{resource_id}`: Delete a resource
- `GET /metrics/low-buoyancy`: Get resources with low Memory Buoyancy
- `GET /metrics/archive-candidates`: Get archiving candidates (low MB, high PV)
- `GET /metrics/deletion-candidates`: Get deletion candidates (low MB, low PV)
- `POST /access-log`: Log a resource access event
- `POST /update-metrics`: Update metrics for all resources

## License

MIT