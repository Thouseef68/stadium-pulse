# 🏟️ Stadium Pulse: AI Command Center

An enterprise-grade AI-powered logistics and crisis management dashboard built for high-density sports venues.

Stadium Pulse leverages Google Gemini 2.5 Flash and cloud-native infrastructure to provide:

- Real-time crowd routing
- Emergency response automation
- Crowd risk analytics
- Weather-aware operational decisions
- AI-generated public communication

Designed to maintain safety, operational efficiency, and rapid decision-making during high-pressure sporting events.

---

## 🚀 Live Demo

Experience Stadium Pulse in action:

🌐 Live Application:
https://stadium-pulse-601476426997.asia-south1.run.app/

---

## 📌 Problem Statement

Large stadiums face multiple operational challenges:

- Crowd congestion during entry and exits
- Delayed emergency response
- Difficulty predicting risk situations
- Weather disruptions
- Communication delays

Traditional monitoring systems often react after incidents occur.

Stadium Pulse introduces predictive intelligence and automated decision support.

---

## ✨ Features

### 🔄 Dynamic Routing Matrix
Computes tactical routing workflows to redirect crowd movement during critical events:

- Match toss
- Innings break
- Exit rush
- Emergency evacuation

Outputs structured JSON-based action plans.

---

### 🚨 Emergency Dispatch System

One-click response activation for:

- Medical emergencies
- Fire incidents
- Crowd stampede mitigation
- Security escalation

---

### 👁️ Vision Analytics

AI-powered crowd monitoring using CCTV feeds or uploaded images:

- Crowd density estimation
- Risk detection
- Congestion alerts
- Safety analysis

---

### 🌦️ Meteorology Agent

Integrates live weather data for adaptive planning:

- Rain alerts
- Heat risk detection
- Wind condition monitoring
- Mitigation recommendations

---

### 📢 Automated Communication System

Generates AI-powered stadium announcements:

- Crowd instructions
- Emergency messaging
- Safety alerts
- Event notifications

---

## 🏗️ System Architecture

```text
User Interface (Streamlit)
            │
            ▼
Google Gemini 2.5 Flash
            │
 ┌──────────┼──────────┐
 │          │          │
 ▼          ▼          ▼

Vision    Weather    Emergency
Agent      Agent      Engine

            │
            ▼

JSON Validation Layer
            │
            ▼

Google Cloud Run Deployment
