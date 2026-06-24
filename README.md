# Honeypot-Based Intrusion Detection and Deception System

## Overview

This project is a Flask-based cybersecurity honeypot system designed to detect, analyze, and divert suspicious users away from legitimate services. The system acts as an intelligent gateway between users and backend services, using risk scoring techniques to identify potential attackers.

Legitimate users are routed to the real API, while suspicious users are redirected to a honeypot environment that simulates a successful login, allowing attack behavior to be monitored and logged without exposing actual resources.

---

## Features

### Risk-Based Request Analysis

The gateway evaluates incoming login requests and assigns a risk score based on:

* Invalid or missing API keys
* SQL injection attempts
* Suspicious usernames
* Excessive request frequency (rate limiting)

### Intelligent Routing

* Safe users → Real API
* Suspicious users → Honeypot API

### SQL Injection Detection

Detects common attack patterns such as:

* `' OR 1=1`
* `UNION SELECT`
* `DROP TABLE`
* SQL comments (`--`)
* Other malicious SQL expressions

### Rate Limiting

Tracks requests per IP address and identifies abnormal login attempts.

### Honeypot Environment

Creates a fake authentication service that:

* Mimics successful logins
* Returns fake access tokens
* Delays responses to appear realistic
* Keeps attackers engaged

### Attack Logging

Stores attacker information including:

* Timestamp
* IP address
* Username
* Password
* API Key
* Risk Score
* Detection Reasons
* Routing Decision

### Monitoring Dashboard

Provides visibility into captured attack attempts and honeypot activity.


## System Architecture

User Request
↓
Gateway Server
↓
Risk Analysis Engine
↓
┌───────────────┬───────────────┐
│               │
▼               ▼
Real API      Honeypot API
(Legitimate)  (Suspicious)
↓               ↓
Real Data      Fake Data
↓               ↓
User        Attacker

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
* Python Collections (defaultdict)

### Networking

* REST APIs
* HTTP Requests
* Requests Library

### Frontend

* HTML
* Flask Templates (Jinja2)

### Monitoring

* Log Analysis Dashboard
* Attack Tracking

---

## Project Structure

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

## Default Credentials

Username: user

Password: pass123

API Key: SECURE-KEY-999

---

## Security Workflow

1. User submits login credentials.
2. Gateway calculates a risk score.
3. Detection checks include:

   * API key validation
   * SQL injection detection
   * Rate limit verification
   * Username reputation checks
4. If score < threshold:

   * User is routed to Real API.
5. If score ≥ threshold:

   * User is routed to Honeypot API.
6. Activity is logged for analysis.

---

## Future Enhancements

* Machine Learning based threat detection
* Real-time alerting system
* Geo-location based attack tracking
* Threat intelligence integration
* Admin analytics dashboard
* Database support (MySQL/PostgreSQL)
* Docker deployment
* SIEM integration

---

## Author

Developed as a cybersecurity project to demonstrate intrusion detection, deception technologies, and secure API gateway implementation using Python and Flask.

