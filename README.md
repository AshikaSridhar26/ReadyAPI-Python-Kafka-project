### Project Overview
This project automates end-to-end API and event-driven testing using ReadyAPI, Kafka, Python, and MySQL.
It validates REST APIs, Kafka message production/consumption, and database persistence using a fully containerized setup.

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
