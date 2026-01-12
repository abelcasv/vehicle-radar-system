# 🚗 Vehicle Radar System

Real-time vehicle radar system for detection, counting and future speed estimation.

## 📌 Overview

This project implements a vehicle radar system designed to detect and count cars while avoiding duplicate detections.  
It simulates how a traffic radar processes incoming events and applies temporal tracking logic to ensure that each vehicle is counted only once.

The project is focused on **data engineering concepts**, such as event processing, noise reduction, state tracking and clean code organization.

---

## 🎯 Features

- Vehicle detection
- Accurate vehicle counting
- Duplicate detection filtering
- Temporal tracking logic
- Modular and extensible design
- Prepared for future speed estimation

---

## 🧠 How It Works

1. Vehicles are detected as events entering the radar system
2. Each detection is timestamped
3. A tracking mechanism filters duplicate detections using temporal windows
4. Only valid vehicle events are counted

The system is designed to behave similarly to real-world traffic radars, where noise and repeated detections must be handled carefully.

---

## 🧱 Project Structure

```
vehicle-radar-system/
├── src/
│ ├── radar.py
│ ├── tracker.py
│ ├── vehicle.py
│ └── queue.py
├── README.md
├── .gitignore
└── LICENSE
```

> ⚠️ Note: The internal structure is currently under refactoring and will evolve as new features are added.

---

## 🚧 Project Status

This project is **under active development**.

Current version:
- Vehicle detection and counting
- Duplicate filtering logic

Planned improvements:
- Vehicle speed estimation
- Improved class separation
- Cleaner architecture
- Integration with real sensor or video data
- Traffic analytics and metrics

---

## 🔍 Key Concepts

- Real-time event processing
- Temporal windows
- State tracking
- Duplicate filtering
- Data structures (queues, priority queues)
- Clean and maintainable code

---

## 🛠️ Technologies

- Python
- Object-Oriented Programming
- Data Structures

---

## 🚀 Future Work

- Speed estimation using multi-point detection
- Persistent storage for traffic data
- Real-time streaming simulation
- Visualization of traffic metrics

---

## 📄 License

This project is licensed under the MIT License.
