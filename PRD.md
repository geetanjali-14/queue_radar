# 📡 Product Requirements Document (PRD): Queue Radar

**Document Status:** Draft (MVP Phase)  
**Target Platform:** Mobile-First (iOS & Android)  

---

## 1. Product Vision & Goals

**Problem Statement:**  
Urban Indians waste millions of hours waiting in queues at clinics, salons, government offices (e.g., RTO, Aadhar centers), temples, and popular restaurants. This uncertainty leads to poor daily planning, anxiety, and massive time loss.

**Target Users:**  
Urban Indian smartphone users (18–50 years old) who value their time, primarily working professionals, parents, and students.

**Key Value Proposition:**  
*"Know before you go."* Queue Radar provides real-time crowd visibility and wait-time estimates, empowering users to make informed decisions about when to visit a location, ultimately saving them time and frustration.

Queue Radar doesn’t just show how busy a place is — it tells you the best time to go, using real-time signals from people, businesses, and devices

---

## 2. User Personas

### 👱‍♂️ 1. Ramesh - The Busy Professional (End User)
* **Profile:** 30 years old, IT worker. 
* **Pain Point:** Needs a haircut but hates walking into a salon only to find 5 people waiting. His weekend time is precious.
* **Goal:** Wants to check his local salon's wait time on the app and get an alert when the crowd clears.

### 👩‍👧 2. Priya - The Anxious Parent (End User)
* **Profile:** 32 years old, mother of a toddler.
* **Pain Point:** Visiting the pediatrician means sitting in a crowded, infectious waiting room for 45+ minutes.
* **Goal:** Wants to arrive exactly 5 minutes before her turn to minimize exposure and toddler tantrums.

### 👨‍⚕️ 3. Dr. Suresh - The Clinic Manager (Business User)
* **Profile:** 45 years old, runs a busy neighborhood clinic.
* **Pain Point:** Patients constantly call the front desk asking "How long will it take?" or complain in the waiting area.
* **Goal:** Wants a 1-tap solution for the receptionist to broadcast the current queue length to patients so they manage their own arrivals.

---

## 3. Core Features

### 🟢 Phase 1: MVP (First 2-3 Weeks)
* **Map & List Radar View:** Discover nearby places (Clinics, Salons, Govt Offices) categorised by crowd status (Red = Packed, Yellow = Busy, Green = Empty).
* **Manual User Check-ins:** Users manually report the current crowd level or wait time.
* **Business "Quick-Update" Dashboard:** A simple web/mobile portal for business receptionists to tap and update the active queue size.
* **Basic Wait-Time Engine:** A weighted-average calculator taking user and business inputs to output an ETA.

### 🟡 Phase 2: Growth & Automation
* **Smart Alerts:** "Notify me when the clinic wait time drops below 15 mins."
* **Favorites/Bookmarks:** Save frequently visited places (gym, regular doctor, neighborhood ATM).
* **GPS Density Ping (Opt-in):** Background location pinging to passively detect how many active app users are dwelling in a specific venue.
* **Gamification:** Karma scores and badges for users who frequently verify and report accurate crowd levels.

### 🚀 Future: Advanced Tech
* **AI-Driven Prediction:** ML models analyzing historical crowd data, weather, and traffic to forecast "Best time to visit tomorrow."
* **Virtual Queuing Integration:** "Join the queue" digitally from the app before leaving home.
* **Deep POS Integrations:** Integrating directly with token/ticketing systems (e.g., Practo, standard token machines).

---

## 4. User Flows

### A. Checking Crowd Before Visiting
1. Open App → Prompted immediately with nearby saved/favorite places.
2. Search for "Apollo Clinic Koramangala".
3. View Place Card showing: `Current Status: High Crowd`, `Est. Wait: 45 Mins`, `Last updated: 3 mins ago by Clinic`.
4. User opts to tap **"Alert me when wait is < 15 mins"**.

### B. User Check-In (Crowd Reporting)
1. User arrives at "Star Salon".
2. App pushes a geofenced notification: *"Are you at Star Salon? How's the crowd?"*
3. User opens app and selects from simple options: `Empty`, `Usually Busy`, `Packed`. 
4. User earns +10 Karma points for community contribution.

### C. Business Updating Queue Data
1. Receptionist logs into the lightweight web app on their counter tablet.
2. Dashboard displays large `+` and `-` buttons for "Currently Waiting".
3. Receptionist taps `+` when a new person walks in and `-` when one enters the doctor's cabin.
4. The system automatically recalculates wait time (Queue Size × Avg Service Time) and broadcasts to consumer apps.

---

## 5. Data & Intelligence Layer

Because MVP cannot rely on complex ML or raw telecom data, the Wait Time Engine will use a **Confidence-Weighted Algorithm**:

**Data Hierarchy (Highest to Lowest Trust):**
1. **Business Input:** Highest priority. If the reception updates the queue, this overwrites everything. (Decays after 45 mins of inactivity).
2. **Recent User Check-ins:** Medium priority. A user check-in from 5 minutes ago carries a 90% confidence weight. At 60 minutes, the weight drops to 10%.
3. **Historical Baseline:** Lowest priority. If no live data exists, show historical averages (e.g., "Usually busy at 6 PM on Fridays") seeded via basic web scraping or Google Places API proxy.

**Wait Time Math (Simple MVP):**
* `Wait_Time` = `People_in_Queue` × `Location_Average_Service_Time` (e.g., 10 mins for haircuts, 15 mins for doctors).

---

## 6. Technical Considerations (High-Level)

* **Architecture:** Node.js (Express) or Python (FastAPI) backend for high concurrency. PostgreSQL for standard relational data (Users, Venues).
* **Real-Time Layer:** Redis + WebSockets (Socket.io) to push real-time queue changes from businesses directly to users browsing the app. 
* **Frontend:** Flutter or React Native. Need cross-platform reach immediately.
* **Data Accuracy Engine:** Anti-spam system rate-limits user check-ins. If a user is not physically within a 50m geofence (GPS check), their input weight is drastically reduced.

---

## 7. MVP Scope Definition

**What to Build (Strict 3-Week Scope):**
* Cross-platform mobile app (Map/List view, Place pages, Manual Check-in).
* Basic authentication (Phone/OTP via Firebase).
* Simple Web Portal for Businesses (Counter dashboard).
* Basic weighted decay algorithm for wait calculation.
* Push notifications (basic alerts).

**What NOT to Build (Avoid until PMF):**
* AI prediction models.
* Passive background location tracking (too complex, battery drain issues).
* In-app booking or payments.
* Direct hospital/salon POS integrations.

---

## 8. Monetization Strategy

1. **B2B SaaS Subscriptions (Primary):** "Queue Radar For Business." Clinics/Salons pay a small monthly fee (e.g., ₹999/month) for the queue management dashboard, automated patient ETA SMS routing, and detailed analytics on peak hours.
2. **Sponsored Visibility:** Businesses with empty waiting rooms can pay to be highlighted. E.g., *"No wait time at Dr. Reddy's Dental – 1km away."*
3. **Future - Virtual Tokens:** Charging a micro-convenience fee (₹10-20) to users for fetching a remote token without being physically present.

---

## 9. Go-To-Market & Cold Start Strategy

* **Hyperlocal Focus:** Do not launch pan-India. Launch only in one dense neighborhood (e.g., HSR Layout, Bangalore) and strictly one category (e.g., Outpatient Clinics).
* **Solving the Cold Start Problem:** 
    * *The "Gig Worker" Seeding:* For the first 2 weeks, hire interns/college students to physically sit near the top 20 busiest clinics to manually report accurate data in the app. This creates immediate value for the first few hundred downloaded users.
    * *Business Onboarding:* Pre-sell the problem to 15 clinics. Give them the business dashboard for free for 6 months.

---

## 10. Risks & Challenges

1. **Cold Start Data Vacuum:** If users open the app and see "No Data available" for wait times, they will uninstall immediately. *(Mitigation: Seed with historically derived data and gig-worker reporting).*
2. **Data Decay:** Queue moves fast. An update from 2 hours ago is useless and dangerous. *(Mitigation: Aggressive data half-life. Display "Data may be stale" if > 1 hr old).*
3. **Change in User Habit:** Users are used to just showing up or calling. *(Mitigation: Position heavily inside high-pain bottlenecks—health clinics).*
4. **Privacy:** Location tracking makes users wary. *(Mitigation: MVP relies on manual, explicit user check-ins rather than passive background tracking).*

---

## 11. Success Metrics (KPIs)

* **Daily/Weekly Active Users (DAU/WAU):** Indicates if checking the app is becoming a habit.
* **Check-in Conversion Rate:** `%` of users who visit a location and actually submit a crowd report (target > 10% with gamification).
* **Business Active Rate:** The number of registered businesses updating their queues daily.
* **Estimated vs. Actual Variance:** Feedback loop validating if our 30-min estimate was actually 30 mins (target: +/- 20% variance).
* **Retention (Day 1 / Day 7 / Day 30):** Ultimate indicator of product-market fit.
