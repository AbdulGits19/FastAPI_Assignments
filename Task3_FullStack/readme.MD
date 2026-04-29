🏥 Winterfell Hospitals Management Portal

A full-stack medical dashboard featuring smart doctor tracking and secure patient management.

## 🚀 Tech Stack
- **Backend:** FastAPI, Python, SQLAlchemy ORM, SQLite.
- **Frontend:** React.js, Vite, Lucide-React (Icons).
- **Security:** JWT (JSON Web Tokens) with OAuth2.
- **Connection:** Axios with Global Interceptors.

## 📊 Dashboards & UI
- **Stats Header:** Live count of Total Patients and Active Appointments.
- **Doctor Dashboard:** Spacious, card-based table with dynamic availability.
- **Patient Directory:** Clean, high-readability list for managing hospital records.
- **Appointment Portal:** Real-time booking system with frontend validation.

## 🧠 Core Logic: Smart Status
The system uses "Stateless Availability." Instead of a fixed DB column, the API checks for active appointments within a 30-minute window of the current time. If a match is found, the doctor's status automatically flips to **Busy** in the UI.

## 🔗 Connection & Security
- **Vite Proxy:** Configured to bridge Port 5173 (React) and Port 8000 (FastAPI).
- **Axios Interceptor:** Automatically attaches the JWT `Bearer` token from localStorage to every API call.
- **WebSocket:** Real-time broadcasting of new/cancelled appointments.

## ⚙️ Quick Setup
1. **Backend:**
   ```bash
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```
2. **Frontend:**
   ```bash
   npm install
   npm run dev
   ```
