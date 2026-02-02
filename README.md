ReadyAPI + Python + Kafka Automation Project

This repository contains an automation project that combines:

ReadyAPI (SoapUI/ReadyAPI) for SOAP/REST functional tests

Python for automation utilities (data handling, validations, scripts)

Apache Kafka for messaging/event-driven test scenarios (topic, producer/consumer validations)

The goal is to demonstrate an end-to-end QA automation approach: API testing + scripting + message verification in a microservices-style architecture.

Tech Stack

ReadyAPI / SoapUI (SOAP + REST API tests, assertions, Groovy scripting)

Python 3.x (test utilities, request automation, validations)

Apache Kafka (event streaming & message verification)

Optional: Docker (Kafka local setup), CI/CD (Jenkins/GitHub Actions)

Project Highlights

SOAP and REST requests with assertions (status code, schema, field validation)

Correlation between requests/responses using extracted values

Kafka validations:

topic creation/listing

producing test messages

consuming and verifying messages (payload, headers, key, ordering)

Reusable scripts/utilities for automation workflow


Test Scenarios Covered
API Tests (ReadyAPI)

SOAP request/response validation

REST request/response validation

Assertions: status, body fields, schema, fault handling

Dynamic chaining: extract value from one response → use in next request

Kafka Tests

Producer message publishing verification

Consumer message reading validation

Duplicate/Idempotency checks (if implemented)

Basic ordering checks (if using keys/partitions)
