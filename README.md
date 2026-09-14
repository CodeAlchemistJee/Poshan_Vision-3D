<div align="center">

# 🏥 Poshan-Vision 3D
### *Intelligent Rural Child Health & Nutrition Management System for Anganwadi Workers*

[![Built with React Native](https://img.shields.io/badge/Frontend-React%20Native%20%2F%20Expo-blue?style=for-the-badge&logo=react)](https://reactnative.dev/)
[![FastAPI Backend](https://img.shields.io/badge/Backend-FastAPI%20(Python)-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Database](https://img.shields.io/badge/Database-Neon%20PostgreSQL-336791?style=for-the-badge&logo=postgresql)](https://neon.tech/)
[![AI & Vision](https://img.shields.io/badge/AI%2F%20CV-MediaPipe%20%2F%20OpenCV-orange?style=for-the-badge&logo=opencv)](https://mediapipe.dev/)
[![Localization](https://img.shields.io/badge/Localization-23%20Regional%20Languages-green?style=for-the-badge)]()
[![Hackathon](https://img.shields.io/badge/ByteBuilt-1.0-purple?style=for-the-badge)]()

</div>

---

## 📖 Overview

**Poshan-Vision 3D** is an advanced, offline-first mobile and cloud application engineered to eliminate manual measurement errors and supply chain tracking friction in rural child welfare ecosystems. Designed specifically for **Anganwadi Workers (AWWs)**, the application modernizes the Supplementary Nutrition Program (SNP) and infant stunting tracking through automated computer vision, rigorous AI confidence scoring, full 23-language localization, and student-linked inventory management.

---

## ✨ Key Features & Innovations

* **🤖 AI-Powered Stunting & Pose Validation:** Replaces error-prone manual infantometers with snapshot-based **MediaPipe Pose** and **OpenCV** calibration against an A4 reference sheet, generating instant height measurements and WHO Z-scores.
* **🎯 0–100 AI Confidence Scoring & Retake Assistant:** Automatically evaluates skeletal joint visibility, blur, and lighting, instantly triggering corrective field instructions if a capture is substandard.
* **🌐 Full 23-Language Localization:** Native script translation across all user interfaces, supporting English and all 22 scheduled regional languages of India for maximum grassroots accessibility.
* **⚡ Offline-First Resilience:** Built with local `AsyncStorage` queue persistence to ensure uninterrupted field data collection during network dropouts, paired with bulk synchronization to **Neon PostgreSQL** upon reconnection.
* **📦 Student-Linked Inventory & Restock Management:** Eliminates ration distribution discrepancies by tying food inventory stock counts atomically to individual child beneficiary profiles, alongside one-tap government shipment restock logging (+20 units).
* **📱 Ergonomic UI/UX:** Mobile-optimized interface featuring safe header padding and vertically stacked card layouts to prevent text clipping and button overflows.

---

## 📐 System Architecture & Data Flow

```text
[ Anganwadi Smartphone (Expo / React Native) ]
       │
       ├──► Local Queue Storage (AsyncStorage - Offline Mode)
       │
       └──► HTTPS REST API Payload (/api/analyze & /api/sync)
                  │
                  ▼
       [ FastAPI Python Backend ]
                  │
                  ├──► OpenCV Contour Scaling & A4 Calibration
                  ├──► MediaPipe Pose (static_image_mode=True)
                  │
                  ▼
       [ Neon PostgreSQL Cloud Database ]
