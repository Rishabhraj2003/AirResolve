# ✈️ AirResolve

### Policy-Grounded Airline Customer Resolution Agent

[![React](https://img.shields.io/badge/Frontend-React-61DAFB?logo=react&logoColor=white)](https://react.dev/)
[![Vite](https://img.shields.io/badge/Build-Vite-646CFF?logo=vite&logoColor=white)](https://vite.dev/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Language-Python-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![REST API](https://img.shields.io/badge/API-REST-02569B)]()
[![Status](https://img.shields.io/badge/Status-Working%20Prototype-2EA44F)]()

> **AirResolve is a customer-facing airline resolution agent that understands customer requests, checks supplied booking data, applies deterministic service policies, performs permitted resolution actions, and escalates requests outside its authority.**

---

## 📌 Overview

Airline disruptions such as cancellations and delays require more than a conversational chatbot.

A useful resolution agent should be able to:

- Understand customer intent
- Identify the correct customer and booking
- Use only trusted customer and booking information
- Apply the correct service policy
- Handle frustrated customers professionally
- Perform or recommend permitted actions
- Escalate requests outside its authority
- Maintain a clear action / resolution record

**AirResolve** was built as a customer-facing prototype for the **AIONOS / AGENTICAIFACTORY Customer-Facing Resolution Agent assignment**.

The main design principle is:

> **The language-understanding layer interprets the customer's request, while deterministic policy logic controls what the agent is actually authorized to do.**

---

## 🎯 Problem

Consider a customer whose flight is cancelled or delayed.

The customer may ask for:

- A refund
- Rebooking
- Compensation
- Lounge access
- Hotel accommodation
- A higher-fare flight
- An upgrade
- An exception to the policy

A simple chatbot may respond with something plausible but unauthorized.

AirResolve instead follows a controlled workflow:

```text
Customer Message
       ↓
Intent / Request Understanding
       ↓
Customer Identification
       ↓
Booking Lookup
       ↓
Policy Evaluation
       ↓
Allowed Action / Escalation
       ↓
Customer Response
       ↓
Sources + Action Record
