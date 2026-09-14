🏥 Poshan-Vision 3DIntelligent Rural Child Health & Nutrition Management System for Anganwadi Workers📖 OverviewPoshan-Vision 3D is an advanced, offline-first mobile and cloud application engineered to eliminate manual measurement errors and supply chain tracking friction in rural child welfare ecosystems. Designed specifically for Anganwadi Workers (AWWs), the application modernizes the Supplementary Nutrition Program (SNP) and infant stunting tracking through automated computer vision, rigorous AI confidence scoring, full 23-language localization, and student-linked inventory management.✨ Key Features & Innovations🤖 AI-Powered Stunting & Pose Validation: Replaces error-prone manual infantometers with snapshot-based MediaPipe Pose and OpenCV calibration against an A4 reference sheet, generating instant height measurements and WHO Z-scores.🎯 0–100 AI Confidence Scoring & Retake Assistant: Automatically evaluates skeletal joint visibility, blur, and lighting, instantly triggering corrective field instructions if a capture is substandard.🌐 Full 23-Language Localization: Native script translation across all user interfaces, supporting English and all 22 scheduled regional languages of India for maximum grassroots accessibility.⚡ Offline-First Resilience: Built with local AsyncStorage queue persistence to ensure uninterrupted field data collection during network dropouts, paired with bulk synchronization to Neon PostgreSQL upon reconnection.📦 Student-Linked Inventory & Restock Management: Eliminates ration distribution discrepancies by tying food inventory stock counts atomically to individual child beneficiary profiles, alongside one-tap government shipment restock logging (+20 units).📱 Ergonomic UI/UX: Mobile-optimized interface featuring safe header padding and vertically stacked card layouts to prevent text clipping and button overflows.📐 System Architecture & Data FlowPlaintext[ Anganwadi Smartphone (Expo / React Native) ]
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
🛠️ Tech Stack & Engineering DesignLayerTechnology / VersionKey ResponsibilityWhy ChosenFrontendReact Native (Expo)Renders localized UI, manages camera snapshot capture and local offline queues.Enables rapid cross-platform deployment with robust native hardware access.BackendFastAPI (Python)Exposes secure REST endpoints (/api/analyze, /api/sync) and coordinates database transactions.High-performance asynchronous execution and seamless integration with Python CV libraries.DatabaseNeon PostgreSQLSecurely stores child profiles, historical stunting records, and cloud audit logs.Serverless relational scalability with robust data integrity and pooling.AI / MLMediaPipe & OpenCVExtracts skeletal joints, computes WHO Z-scores, and runs 0–100 confidence scoring.Lightweight, highly accurate computer vision processing suitable for field hardware.StorageAsyncStorageManages local queue persistence during network dropouts for offline resilience.Ensures 100% data availability in remote rural environments without connectivity.📂 Repository StructurePlaintextposhan-vision-3d/
│
├── frontend/                  # React Native (Expo) Mobile Client
│   ├── src/
│   │   ├── components/        # Reusable UI components & stacked cards
│   │   ├── screens/           # Dashboard, Scanner, Results, & Inventory screens
│   │   ├── localization/      # 23-language translation dictionaries
│   │   └── services/          # API handlers & AsyncStorage offline queue
│   └── App.js                 # Root navigation & state container
│
├── backend/                   # FastAPI Python Server
│   ├── routers/               # /api/analyze & /api/sync endpoints
│   ├── services/              # MediaPipe pose & OpenCV contour logic
│   ├── models/                # Neon PostgreSQL ORM schemas
│   └── main.py                # FastAPI application entry point
│
└── docs/                      # Hackathon product documentation & diagrams
🚀 Getting Started & InstallationPrerequisitesNode.js (v18+) & npm / yarnPython (v3.10+)Expo Go app installed on your physical mobile device (or Android Studio / Xcode Simulator)1. Clone the RepositoryBashgit clone https://github.com/your-username/poshan-vision-3d.git
cd poshan-vision-3d
2. Set Up the BackendBashcd backend
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
Configure your environment variables (.env) with your Neon PostgreSQL connection string.Run the FastAPI server:Bashuvicorn main:app --reload --port 8000
3. Set Up the FrontendBashcd ../frontend
npm install
Update your API base URL configuration in the service client to point to your local backend IP or hosted server.Start the Expo development server:Bashnpx expo start
Scan the generated QR code using the Expo Go app on your smartphone.🧪 Testing & Quality AssuranceThe application undergoes rigorous validation across multiple testing dimensions:Unit & Component Testing: Verified via Python pytest and Expo component inspection.Vision Pipeline Testing: Evaluated against standard A4 floor reference sheets for precise skeletal joint landmark extraction and WHO Z-score mapping.Offline Resilience: Tested via simulated network dropouts (Airplane mode) to confirm zero data loss in local AsyncStorage queues and successful bulk cloud synchronization.Localization Walkthroughs: Ensured flawless script rendering across all 23 official regional languages.📈 RoadmapNow (MVP - ByteBuilt 1.0): Core AI stunting measurement, 23-language localization, offline sync, and student-linked inventory allocation.Next (Pilot Phase): Regional district pilot deployments, advanced administrative analytics dashboards for CDPOs, and automated push notifications.Future (Scale Phase): Nationwide rollout, integration with official government POSHAN portal APIs, and automated biometric child identification.👥 Acknowledgements & TeamDeveloped with passion for ByteBuilt 1.0 hackathon. Special thanks to our mentors and academic guides at Chandigarh University and byteXL.
