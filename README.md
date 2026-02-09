### ReadyAPI – Python – Kafka End-to-End Test Framework

This project demonstrates a true end-to-end testing framework for event-driven systems using ReadyAPI, Kafka, Python, MySQL, JMeter, and Jenkins.
It validates not just APIs, but the entire data flow across layers under both functional and load conditions.

#### Architecture Overview

The framework is deliberately layered to keep responsibilities clear:

ReadyAPI orchestrates API-level testing

MockServer / API publishes asynchronous Kafka events

Kafka handles event propagation

Python (pytest) validates backend truth asynchronously

MySQL stores system state

JMeter generates load and publishes Kafka messages

Jenkins runs everything in CI and publishes reports


Logical Flow

    CLIENT / READYAPI
            |
            | POST /customers (correlationId)
            v
    MOCKSERVER / API
            |
            | async event
            v
    KAFKA  <---- JMeter (load with runId)
            |
            | consume + retry
            v
    PYTHON (pytest)
            |
            | poll until consistent
            v
    MYSQL


This setup reflects how real distributed systems behave — asynchronous, eventually consistent, and event-driven.

### Core Design Principles

- Correlation-driven testing
Uses correlationId and runId consistently across API, Kafka, and database layers.

- Contract testing at multiple layers
Prevents breaking changes at both API and event levels.

- Eventual consistency handling
Uses polling with timeouts instead of brittle static waits.

- Cross-layer validation
Verifies correctness across API → Kafka → Database, not just surface responses.

- Parallel-safe execution
Isolated Kafka consumer groups and test data enable safe concurrent runs.

- CI observability
Jenkins publishes reports and archives artifacts for traceability.

### Contract Testing Strategy

-API Contracts
Validated in ReadyAPI using JSON Schema and field-level assertions.

-Kafka Event Contracts
Validated in Python by asserting:
Required fields
Data types
Semantic correctness
This ensures producer–consumer compatibility and catches breaking changes early.
### Tech Used

    ReadyAPI (API + Kafka testing)
    Python (test utilities and validations)
    Apache Kafka (event streaming)
    MySQL (data verification)
    Docker (execution environment)

### Prerequisites

    Docker
    Docker Compose

### Project Structure

    KafkaAPItesting-readyapi-project.xml – ReadyAPI test project
    Dockerfile-readyapi.txt – Runs ReadyAPI tests
    Dockerfile-pytest.txt – Runs Python tests
    docker-compose.yml – Kafka, Zookeeper, MySQL setup
    requirements.txt – Python dependencies
    src – Python test logic and helpers

### How to Run Tests (Docker Only)

    **Step 1**: Start Kafka and MySQL
    Run this once to start all dependencies:
    docker compose up -d
    
    **Step 2**: Run ReadyAPI Tests
    Build the ReadyAPI test runner image:
    docker build -f Dockerfile-readyapi.txt -t readyapi-tests .
    
    Run the ReadyAPI tests:
    docker run --rm --network host readyapi-tests
    
    This executes all test suites defined in KafkaAPItesting-readyapi-project.xml.
    
    **Step 3**: Run Python Tests
    Build the Python test image:
    docker build -f Dockerfile-pytest.txt -t python-tests .
    
    Run Python validations:
    docker run --rm --network host python-tests
    
    **Step 4**: Stop Services (after tests)
    docker compose down

### What Gets Validated

        API request and response correctness
        Kafka message production and consumption
        Data persistence in MySQL
        End-to-end system integrity

### Notes

    Kafka bootstrap server is expected on localhost:9092
    MySQL is expected on localhost:3306
    Adjust environment values inside Dockerfiles if needed
    Use host networking to simplify Kafka connectivity

### CI Ready
Project includes a Jenkins pipeline file for automated execution in CI environments.
