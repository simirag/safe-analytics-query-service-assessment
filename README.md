# Safe Analytics Query Service

## Description

FastAPI based lightweight analytics service that allows users to query aggregate information from datasets in a safe and reproducible way.
The service load employee data from CSV, expose an API for aggression queries, apply configurable safety rules and generate audit logs.

---
# Objective
This project was developed as part of a Research Software Engineer Take Home Assessment.
The goal of this exercise is to assess practical software engineering, API design, testing, validation logic, and problem solving skills.
---

# Setup
## Requirements
The following software must be installed
* Docker
* Git
## Installation
1. clone the repo
2. Configure Application settings (Optional)
  * Edit root/src/config.py or Add .env file with configured variable to override
  Eg:
    Change SUPPRESSED = 2 in root/src/config.py to use suppression 2 with the project
3. Build the docker image
  Run docker build command from root/src directory
  Eg:
    ```bash
    docker build -t buildname:tag .
    ```
4. Run the container
  After successful build run the container and expose port
   Eg:
    ```bash
    docker run -d -p 8000:8000 buildname:tag
    ```
5. Access the Application 
  Once the application is started, then it can be accessed at the exposed host and port
   Eg: http://localhost:8000/docs

---

# Tests

Run tests using pytest
Test coverage:
   * validation logic
   * suppression behaviour
   * API response
   * Filtering behaviour
   * Model testing
Example: 
```json
pytest tests
```

---

# API Endpoints

## /query
Querying aggregate statistics based on the group_by and filter fields
Request method: POST
Parameter Type: Body
Application type: application/json

Example:

```http
POST /query
```

*Example request:

```json
{
  "group_by": "department"
}
```

Support simple filtering in queries.

Example:

```json
{
  "group_by": "department",
  "filter": {
    "location": "London"
  }
}
```

*Example Response:
Results with suppression threshold = 3
```json
{
  "Engineering": 9,
  "Finance": 3,
  "HR": 3,
  "Marketing": 3,
  "Support": 3,
  "Research": 4,
  "Legal": 3,
  "Executive": "suppressed"
}
```
---
# API Documentation
  API documentation available at following location
  OpenAPI based - /docs
  Alternative - /redoc
  json schema - /openapi.json

---
# Audit Logs & Application Logging

Each query will generate an audit log entry in DB containing:

* timestamp
* query details
* whether suppression was triggered

Example:

```json
{
  "timestamp": "2026-05-26T10:00:00Z",
  "group_by": "department",
  "filters": {
    "location": "London"
  },
  "suppression_triggered": true
}
```
Application logging will be generated in {root}/logs directory
---

## 6. Containerise the Application

Please provide:

* Dockerfile
* simple run instructions

---


# Assumptions

Following assumptions were made during development
1. Dataset is loaded during the application startup
2. Suppression threshould default to 3

---

# Submission Contents
The repository includes:

* source code
* README updates if required
* Dockerfile
* tests
* run instructions

---

