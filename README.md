# Honeypot-Based Intrusion Detection and Deception System

## Overview

This project is a Flask-based cybersecurity honeypot system designed to detect, analyze, and divert suspicious users away from legitimate services.

The system acts as an intelligent gateway between users and backend services, using risk-scoring techniques to identify potentially malicious activity.

Legitimate users are routed to the real API, while suspicious users are redirected to a honeypot environment that simulates a successful login. This allows attack behavior to be monitored and logged without exposing actual resources.

---

## Features

### Risk-Based Request Analysis

The gateway evaluates incoming login requests and assigns a risk score based on:

* Invalid or missing API keys
* SQL injection attempts
* Suspicious usernames
* Excessive request frequency
* Rate-limit violations

### Intelligent Routing

* **Safe users** → Real API
* **Suspicious users** → Honeypot API

### SQL Injection Detection

Detects common SQL injection patterns, including:

* `' OR 1=1`
* `UNION SELECT`
* `DROP TABLE`
* SQL comments such as `--`
* Other suspicious SQL expressions

### Rate Limiting

Tracks requests by IP address and identifies abnormal or excessive login attempts.

### Honeypot Environment

The honeypot authentication service:

* Mimics successful logins
* Returns fake access tokens
* Delays responses to appear realistic
* Keeps suspicious users engaged
* Prevents access to legitimate resources

### Attack Logging

The system records information about detected attack attempts, including:

* Timestamp
* IP address
* Username
* API key
* Risk score
* Detection reasons
* Routing decision

> **Security Note:** Avoid storing real passwords in plaintext. If passwords are logged for a controlled academic demonstration, ensure the project is never deployed with real credentials or exposed to untrusted users.

### Monitoring Dashboard

Provides visibility into captured attack attempts and honeypot activity through a web-based monitoring dashboard.

---

## System Architecture

```text
                    User Request
                         │
                         ▼
                  ┌─────────────┐
                  │   Gateway   │
                  │   Server    │
                  └──────┬──────┘
                         │
                         ▼
                ┌─────────────────┐
                │  Risk Analysis  │
                │     Engine      │
                └────────┬────────┘
                         │
              ┌──────────┴──────────┐
              │                     │
        Low Risk               High Risk
              │                     │
              ▼                     ▼
       ┌─────────────┐       ┌─────────────┐
       │   Real API  │       │ Honeypot API│
       └──────┬──────┘       └──────┬──────┘
              │                     │
              ▼                     ▼
         Real Data              Fake Data
              │                     │
              ▼                     ▼
        Legitimate User          Attacker
```

---

## Technologies Used

### Backend

* Python 3
* Flask
* Flask-CORS

### Security Components

* Risk Scoring Engine
* SQL Injection Detection
* API Key Validation
* Rate Limiting
* Honeypot Deception Mechanism

### Data Handling

* JSON Logging
* Python `collections.defaultdict`

### Networking

* REST APIs
* HTTP Requests
* Python Requests Library

### Frontend

* HTML
* Jinja2 / Flask Templates

### Monitoring

* Log Analysis Dashboard
* Attack Tracking

---

## Project Structure

```text
Honeypot/
│
├── gateway.py
├── real_api.py
├── honeypot_api.py
│
├── templates/
│   ├── login.html
│   ├── monitor.html
│   ├── fake_dashboard.html
│   └── real_dashboard.html
│
├── logs/
│   └── honeypot_log.json
│
└── requirements.txt
```

---

## Default Credentials

For local development/testing only:

```text
Username: user
Password: pass123
API Key: SECURE-KEY-999
```

> **Warning:** Do not use these credentials in production. Store sensitive credentials in environment variables or a secure secrets manager.

---

## Security Workflow

1. The user submits login credentials.
2. The gateway receives and analyzes the request.
3. The risk analysis engine calculates a risk score.
4. Detection checks are performed, including:

   * API key validation
   * SQL injection detection
   * Rate-limit verification
   * Username reputation checks
5. If the risk score is below the configured threshold:

   * The request is routed to the **Real API**.
6. If the risk score meets or exceeds the threshold:

   * The request is routed to the **Honeypot API**.
7. The activity is logged for monitoring and analysis.

---

## Future Enhancements

* Machine-learning-based threat detection
* Real-time security alerts
* Geo-location-based attack tracking
* Threat intelligence integration
* Advanced admin analytics dashboard
* MySQL/PostgreSQL database support
* Docker deployment
* SIEM integration
* Automated threat reporting

---

## Author

Developed as a cybersecurity project demonstrating:

* Intrusion detection
* Honeypot and deception technologies
* Risk-based request analysis
* Malicious request detection
* Secure API gateway concepts
* Python and Flask-based security architecture
