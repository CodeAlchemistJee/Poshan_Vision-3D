# 🏥 Poshan-Vision 3D

### Intelligent Rural Child Health & Nutrition Management System for Anganwadi Workers

> **Measure smarter. Work faster. Identify risk earlier.**

**Poshan-Vision 3D** is an offline-first, AI-powered mobile and cloud platform designed to support **Anganwadi Workers (AWWs)** in rural child health, nutrition monitoring, field data collection, and centre-level inventory management.

The platform combines **computer vision, MediaPipe pose estimation, OpenCV-based geometric calibration, WHO growth assessment, AI confidence scoring, multilingual interfaces, offline synchronization, and digital inventory workflows** into a single field-oriented application.

Rather than replacing the broader POSHAN ecosystem, Poshan-Vision 3D focuses on creating an **AI-powered operational and measurement layer for frontline workers**.

---

## 🎯 Problem Statement

Anganwadi Workers perform a wide range of activities including:

* Child growth monitoring
* Nutrition-related activities
* Beneficiary follow-ups
* Home visits
* Data recording
* Reporting
* Supplementary Nutrition Program activities
* Centre-level inventory management

In rural and connectivity-constrained environments, these activities can involve:

* Manual anthropometric measurements
* Repeated data entry
* Poor or inconsistent measurement conditions
* Network dependency
* Difficulty tracking pending follow-ups
* Inventory recording friction
* Language and accessibility barriers

### 💡 Our Approach

Poshan-Vision 3D aims to reduce this operational burden through:

**AI-assisted measurement + offline-first data collection + multilingual interaction + intelligent workflow management.**

---

# 🚀 Key Features

## 1. 🤖 AI-Powered Child Measurement

The computer vision pipeline combines **MediaPipe Pose** with **OpenCV-based image processing**.

The system:

1. Captures an image using the smartphone camera.
2. Detects the A4 reference sheet.
3. Establishes a pixel-to-centimeter scale.
4. Detects body landmarks using MediaPipe.
5. Validates the child's measurement posture.
6. Estimates height.
7. Generates a measurement confidence score.

### Measurement Pipeline

```text
Smartphone Camera
       ↓
Image Preprocessing
       ↓
A4 Reference Detection
       ↓
Pixel-to-CM Calibration
       ↓
MediaPipe Pose Detection
       ↓
Pose Validation
       ↓
Height Estimation
       ↓
Confidence Scoring
```

---

# 2. 📐 A4 Dynamic Reference Calibration

Poshan-Vision 3D uses a standard **A4 sheet as a visual reference anchor**.

The system identifies the rectangular reference object using:

* Grayscale conversion
* Gaussian Blur
* Canny Edge Detection
* Contour detection
* Polygon approximation
* Area-based filtering

The known physical dimensions of an A4 sheet provide a reference for converting image pixels into real-world measurements.

### Concept

```text
Known Reference
A4 Sheet
210mm × 297mm
       ↓
Pixel Measurement
       ↓
Pixel / CM Ratio
       ↓
Child Measurement
```

This enables the system to operate without relying on dedicated depth sensors such as LiDAR.

---

# 3. 🎯 AI Measurement Confidence Score

Every measurement receives a **0–100 confidence score** based on image and pose quality.

Potential factors include:

* A4 reference visibility
* Body landmark visibility
* Pose alignment
* Image sharpness
* Lighting quality
* Body visibility
* Camera positioning

Example:

```text
Measurement Quality
━━━━━━━━━━━━━━━━━━━━

A4 Detection       98%
Pose Quality       94%
Body Visibility    97%
Image Quality      91%
Lighting           88%

━━━━━━━━━━━━━━━━━━━━

Overall Confidence
       94%
```

This allows the AWW to understand not only the measurement but also **how reliable the capture conditions were**.

---

# 4. 🔄 Intelligent Retake Assistant

Poor images can produce unreliable measurements.

Instead of silently accepting a low-quality capture, the system identifies potential issues and provides corrective instructions.

Examples:

> ⚠️ Both feet are not visible.

> ⚠️ A4 reference is partially obstructed.

> ⚠️ Lighting is insufficient.

> ⚠️ Child posture is unsuitable.

> ⚠️ Image is too blurry.

The worker can immediately retake the image.

---

# 5. 📊 Growth & Nutrition Assessment

After measurement, the system can combine:

* Age
* Sex
* Height
* Weight
* Historical measurements

to generate growth-related indicators and screening information based on configured **WHO Child Growth Standards**.

Example:

```text
Child Profile
────────────────────
Age       : 3 years
Sex       : Female
Height    : 87.4 cm
Weight    : 10.1 kg

Growth Assessment
────────────────────
Height-for-age
Weight-for-age
Weight-for-height

Screening Status
🟠 Requires Attention
```

> **Important:** Poshan-Vision 3D is intended as a screening and decision-support tool, not a replacement for professional medical diagnosis.

---

# 6. 📈 Child Growth History

Each beneficiary can have a longitudinal growth record.

```text
January   → 81.2 cm
February  → 82.0 cm
March     → 82.7 cm
April     → 83.0 cm
May       → 83.1 cm
```

The system can visualize:

* Previous measurements
* Growth trends
* Measurement confidence
* Screening history
* Follow-up status

This helps move from **single-point measurement** toward **trajectory-based monitoring**.

---

# 7. 🧠 Growth Trend Intelligence

Historical data can be analyzed to identify patterns such as:

* Improving growth
* Stable growth
* Slowing growth
* Declining trajectory

Example:

> ⚠️ **Growth trajectory requires monitoring**

This allows frontline workers to pay attention to changes over time rather than relying only on a single measurement.

---

# 8. 🌐 23-Language Localization

The application is designed for India's multilingual environment.

It supports:

* English
* Hindi
* Assamese
* Bengali
* Bodo
* Dogri
* Gujarati
* Kannada
* Kashmiri
* Konkani
* Maithili
* Malayalam
* Manipuri
* Marathi
* Nepali
* Odia
* Punjabi
* Sanskrit
* Santali
* Sindhi
* Tamil
* Telugu
* Urdu

The localization architecture separates language dictionaries from application logic, making additional languages easier to integrate.

---

# 9. 📴 Offline-First Architecture

Connectivity should not prevent an AWW from recording field activities.

When the network is unavailable:

```text
AWW
 ↓
Mobile Application
 ↓
Local Queue
 ↓
AsyncStorage
 ↓
Network Restored
 ↓
Bulk Synchronization
 ↓
Cloud Database
```

The application maintains locally queued records until synchronization becomes possible.

### Example

```text
📴 Offline Mode

7 records pending synchronization

        ↓

🌐 Connection Restored

Synchronizing...

✓ 7/7 records synchronized
```

---

# 10. ☁️ Cloud Synchronization

The application uses a FastAPI backend to synchronize field records with the cloud.

### Core endpoints

```text
POST /api/analyze
POST /api/sync
```

The synchronization architecture is designed to support:

* Retry mechanisms
* Bulk synchronization
* Duplicate prevention
* Transactional database updates
* Network interruption recovery

---

# 11. 📦 Digital Nutrition Inventory

The platform includes centre-level inventory management for supplementary nutrition-related workflows.

AWWs can:

* View current stock
* Record incoming stock
* Record distribution
* Track remaining quantities
* Identify low-stock situations

Example:

```text
Nutrition Inventory
━━━━━━━━━━━━━━━━━━

Rice       18 kg
Dal        12 kg
Milk        8 L

⚠️ Dal stock is low
```

---

# 12. 👶 Beneficiary-Linked Distribution Records

Inventory activities can be associated with beneficiary records.

Example:

```text
Beneficiary
     ↓
Nutrition Allocation
     ↓
Distribution Record
     ↓
Inventory Update
```

This creates a more traceable digital workflow between **beneficiaries and nutrition distribution records**.

---

# 13. 📋 AWW Daily Work Dashboard

The application can provide a centralized view of daily activities.

```text
GOOD MORNING 👋

Today's Work
━━━━━━━━━━━━━━━━

🔴 4 Follow-ups
🟡 8 Measurements
🟢 12 Home Visits
📚 1 ECCE Activity
📦 Nutrition Activity

━━━━━━━━━━━━━━━━

Progress

████████░░ 78%

25 / 32 Completed
```

The goal is to reduce the need for AWWs to manually remember pending activities.

---

# 14. 🧠 AI Priority Queue

The system can prioritize activities based on:

* Screening status
* Growth trajectory
* Follow-up status
* Measurement due dates
* Data quality
* Urgency

Example:

```text
TODAY'S PRIORITIES

🔴 Child #1042
Follow-up overdue

🔴 Child #1091
Declining growth trajectory

🟠 Child #1024
Measurement required

🟢 Routine monitoring
```

---

# 15. 🏠 Digital Home Visit Workflow

AWWs can record home visits digitally.

```text
Select Beneficiary
       ↓
Start Home Visit
       ↓
Record Observations
       ↓
Nutrition / Growth Information
       ↓
Add Follow-Up
       ↓
Submit
```

Future versions can support voice-based entry to reduce typing.

---

# 16. 🎙️ Voice-Assisted Data Entry

The platform is designed to support natural-language interaction.

Example:

> “Aaj Riya ka home visit kiya. Weight 10.2 kilo tha aur nutrition counselling di.”

The system can convert the speech into structured information:

```text
Child: Riya
Activity: Home Visit
Weight: 10.2 kg
Counselling: Nutrition
Date: Today

[Confirm]
```

This creates a:

### **Speak → Structure → Verify → Save**

workflow.

---

# 17. 🔍 Data Quality Intelligence

Before records are finalized, the system can identify:

* Missing information
* Unrealistic measurements
* Duplicate records
* Sudden measurement changes
* Low-confidence captures
* Incomplete activities

Example:

```text
DATA QUALITY CHECK

⚠ 2 records missing age
⚠ 1 unusual measurement
⚠ 3 incomplete activities

[Review Records]
```

---

# 18. 🔐 Privacy & Security

The architecture is designed around privacy-by-design principles.

Security considerations include:

* HTTPS API communication
* Authenticated access
* Role-based permissions
* Audit logging
* Minimal raw-image retention
* Secure database connectivity
* Controlled access to beneficiary records

Future production deployments should additionally undergo appropriate security, privacy, clinical, and government compliance reviews.

---

# 🏗️ System Architecture

```text
┌──────────────────────────────────────────┐
│        AWW Smartphone / Edge Device      │
│                                          │
│     React Native + Expo                  │
│                                          │
│  ┌───────────────┐   ┌────────────────┐ │
│  │ Camera        │   │ Local Queue    │ │
│  │ Capture       │   │ AsyncStorage   │ │
│  └───────┬───────┘   └───────┬────────┘ │
└──────────┼────────────────────┼──────────┘
           │                    │
           │ HTTPS              │ Sync
           ▼                    ▼
┌──────────────────────────────────────────┐
│             FastAPI Backend              │
│                                          │
│  ┌──────────────┐  ┌─────────────────┐  │
│  │ OpenCV       │  │ MediaPipe Pose  │  │
│  │ Calibration  │  │ Validation      │  │
│  └──────────────┘  └─────────────────┘  │
│                                          │
│         Measurement & Risk Engine        │
└───────────────────────┬──────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────┐
│             Neon PostgreSQL              │
│                                          │
│  Beneficiaries                           │
│  Measurements                            │
│  Growth History                           │
│  Inventory                               │
│  Activities                              │
│  Follow-ups                              │
│  Audit Logs                              │
└──────────────────────────────────────────┘
```

---

# 🧩 Technology Stack

| Layer           | Technology        | Purpose                        |
| --------------- | ----------------- | ------------------------------ |
| Mobile          | React Native      | Cross-platform application     |
| Framework       | Expo              | Rapid mobile development       |
| Backend         | FastAPI           | REST API and processing        |
| Language        | Python            | AI/CV backend                  |
| Computer Vision | OpenCV            | Image processing & calibration |
| Pose Estimation | MediaPipe         | Body landmark detection        |
| Database        | PostgreSQL        | Relational data persistence    |
| Cloud Database  | Neon              | Managed PostgreSQL             |
| ORM             | SQLAlchemy        | Database abstraction           |
| Local Storage   | AsyncStorage      | Offline queue                  |
| API             | REST / HTTPS      | Client-server communication    |
| Localization    | JSON dictionaries | Multilingual UI                |

---

# 📂 Repository Structure

```text
poshan-vision-3d/
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── screens/
│   │   ├── localization/
│   │   └── services/
│   │
│   └── App.js
│
├── backend/
│   ├── routers/
│   │   ├── analyze.py
│   │   └── sync.py
│   │
│   ├── services/
│   │   ├── pose_detection.py
│   │   ├── image_processing.py
│   │   └── measurement.py
│   │
│   ├── models/
│   │   └── database_models.py
│   │
│   └── main.py
│
├── docs/
│   ├── architecture/
│   ├── diagrams/
│   └── hackathon/
│
└── README.md
```

---

# ⚙️ Getting Started

## Prerequisites

Install the following:

* Node.js 18+
* npm or Yarn
* Python 3.10+
* Expo Go
* Android Studio or Xcode (optional)

---

## 1. Clone the Repository

```bash
git clone https://github.com/your-username/poshan-vision-3d.git

cd poshan-vision-3d
```

---

# 2. Backend Setup

```bash
cd backend
```

Create a virtual environment:

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# 3. Environment Variables

Create a `.env` file inside the backend directory.

```env
DATABASE_URL=your_neon_postgresql_connection_string
```

Additional API keys/configuration can be added according to the deployment environment.

> Never commit `.env` files or production credentials to GitHub.

---

# 4. Start FastAPI

```bash
uvicorn main:app --reload --port 8000
```

The backend will be available locally at:

```text
http://localhost:8000
```

---

# 5. Frontend Setup

Open another terminal:

```bash
cd frontend
npm install
```

Configure the API base URL according to your development environment.

For physical-device testing, use the host machine's local network IP rather than `localhost`.

Start Expo:

```bash
npx expo start
```

Scan the generated QR code using **Expo Go**.

---

# 🧪 Testing

The project includes testing across multiple dimensions.

## Computer Vision Testing

The measurement pipeline can be evaluated using:

* Standard A4 references
* Different backgrounds
* Different lighting conditions
* Different camera distances
* Different child poses
* Partial occlusion scenarios

---

## Offline Testing

Test using:

```text
Online
  ↓
Capture Data
  ↓
Enable Airplane Mode
  ↓
Capture More Data
  ↓
Restore Network
  ↓
```
