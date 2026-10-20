# 🎙️ Presentation & Viva Speech Script
### Global Marine Microplastic Pollution Analytics (CSE355)
**Speaker:** K. Ganesh Giridhar (CB.SC.U4CSE24519)  
**Style:** Simple Spoken English · Short Bullet Points · Action-Oriented

---

## ⏱️ Quick Summary & Timing Plan (Total: 6–8 Minutes)

| Section | Time | What You Cover |
|---|:---:|---|
| **1. Welcome, Dataset & Problem** | 1.0 min | Who you are, the 29K NOAA dataset, and the core problem. |
| **2. Preprocessing (What & Why)** | 0.5 min | 2 clear statements on coordinates & unit separation. |
| **3. Visualizations Walkthrough (V1 to V8)** | 2.5 min | What it is, which tool was used, and the direct insight. |
| **4. Ethical Redesign (V9)** | 1.0 min | Truncated axis trick vs. honest zero-baseline redesign. |
| **5. Live Dashboard Simulation** | 1.5 min | Exactly what to click and what to say in Power BI. |
| **6. Final Insights & Wrap-Up** | 1.0 min | 3 main takeaways and quick conclusion. |

---

## 1. Introduction: Dataset & Problem (Slide 1, 2 & 3)

### 🗣️ What to Say:
* "Good morning / afternoon everyone. My name is **Ganesh Giridhar**, roll number **CB.SC.U4CSE24519**."
* "Today, I am presenting my case study: **Global Marine Microplastic Pollution Analytics**."

### 📊 About the Dataset:
* "I used the official **NOAA Marine Microplastics Database**."
* "It contains **29,076 verified records** collected over **54 years**, from 1972 to 2026."
* "It covers all **5 major oceans** and **4 different marine settings**."

### ⚠️ The Problem:
* "Millions of tons of plastics enter the ocean every year and break down into microplastics under 5 millimeters."
* "Here is the big challenge in the data:
  * Researchers measured plastics in **3 completely different units** (`pieces/m³` in water, `pieces/10 mins` on beaches, and `pieces/kg` in seabed sediment).
  * Also, some oceans are sampled thousands of times, while others are barely visited."
* **"Our core problem statement is:**  
  *How do we analyze and show this data honestly, without confusing heavy research effort with real pollution hotspots, and without mixing incompatible units?*"

---

## 2. Preprocessing: What We Did & Why We Did It (Slide 4)

*(Keep this to 2 clear, simple statements as requested)*

### 🗣️ What to Say:
1. **Coordinate Check:**  
   * *"First, we checked all 29,076 latitude and longitude points. Every single row had valid coordinates between -90 and +90 latitude, so zero rows were lost."*
2. **Strict Unit Isolation:**  
   * *"Second, we strictly separated the data by marine setting so that water, beach, and sediment units are never averaged together. Mixing them would create fake, meaningless numbers."*

---

## 3. Visualizations Walkthrough: V1 to V8 (Slides 6, 7 & 8)

*(Say what it is · Which tool you used · What the insight is)*

---

### 📍 V1: Global Sampling Map
* **What it is:** A global map plotting all 29,076 sample locations.
* **Tool used:** Python (Matplotlib & GeoPandas) and Power BI Map.
* **The Insight:**
  * *"94% of all samples come from the Northern Hemisphere, mainly around the US and Europe."*
  * *"The Indian Ocean has only 2.7% of samples, and the Southern Ocean has only 0.1%. They are huge data blindspots."*

---

### 📍 V2: Effort-Aware Hotspot Grid
* **What it is:** A 2-degree grid that divides plastic count by the number of research visits.
* **Tool used:** Python (Matplotlib).
* **The Insight:**
  * *"Near tourist beaches like Florida, there are thousands of samples, but the plastic level is actually low-to-medium."*
  * *"True danger zones are in open-ocean gyres like the North Pacific, where very few ships go, but concentration is extremely high."*

---

### 📍 V3: 50-Year Monitoring Trend (1972–2026)
* **What it is:** A timeline tracking sample counts and median water pollution over 5 decades.
* **Tool used:** Python (Matplotlib dual-axis) and Power BI.
* **The Insight:**
  * *"The sudden jump in data after 2010 is because citizen science programs like Nurdle Patrol started, not because pollution exploded overnight."*
  * *"Separating sample count from concentration shows baseline water pollution has stayed high and steady."*

---

### 📍 V4: Pollution Across the 5 Oceans
* **What it is:** Boxplots comparing microplastic levels across all 5 ocean basins.
* **Tool used:** Python (Seaborn log-scale boxplot).
* **The Insight:**
  * *"The Pacific Ocean has the highest median pollution—1.84 pieces per cubic meter. That is over 4 times dirtier than the Atlantic."*
  * *"The Mediterranean Sea has the most extreme coastal spikes, going over 1,000 pieces per cubic meter."*

---

### 📍 V5: Comparison Across 4 Marine Settings
* **What it is:** Comparing microplastics in Ocean Water, Beach Sand, Seabed Sediment, and Nurdle Patrol.
* **Tool used:** Python (Seaborn multi-panel) and Power BI.
* **The Insight:**
  * *"Beach sand has a median of 1,280 pieces per cubic meter, while open water has a median of only 0.01."*
  * *"This proves why these settings can never share the same numeric scale."*

---

### 📍 V6: Sampling Methods by Ocean
* **What it is:** A table matrix showing which sampling gear was used in which ocean.
* **Tool used:** Python (Seaborn heatmap) and Power BI Matrix.
* **The Insight:**
  * *"Gear is tied to geography. Manta nets were mostly used in the open Atlantic, while grab samplers were used in coastal seas."*
  * *"You cannot compare two oceans without checking what gear they used."*

---

### 📍 V7: Net Mesh Size Aperture Bias
* **What it is:** A chart testing microplastics caught versus net hole size.
* **Tool used:** Python (Seaborn regression scatter).
* **The Insight:**
  * *"Standard nets use 333-micron holes. But fine nets under 100 microns catch 4 times more microplastics, especially clothing fibers."*
  * *"This means standard scientific nets have been heavily undercounting ocean plastics for decades."*

---

### 📍 V8: Severity Breakdown Across Oceans
* **What it is:** A 100% stacked bar chart showing the share of Very Low, Low, Medium, High, and Very High pollution in each basin.
* **Tool used:** Python (Matplotlib) and Power BI.
* **The Insight:**
  * *"Globally, 17.7% of samples fall into High and Very High danger categories."*
  * *"The Pacific gyre and Mediterranean Sea carry the largest share of high-severity records."*

---

## 4. Ethical Redesign: V9 (Slide 11)

### 🗣️ What to Say:
* *"In Section 2, we conducted a forensic data ethics audit."*
* **On the Left – The Misleading Chart:**
  * *"Here is the misleading chart. Notice the Y-axis: it does not start at zero. It starts at 0.200."*
  * *"Because of this truncated axis, a tiny 10% difference looks like a massive 800% disaster."*
  * *"It also hides the sample size and hides the spread, creating fake public panic."*
* **On the Right – Our Ethical Redesign:**
  * *"We fixed this by starting the axis at true zero (0.0)."*
  * *"We used boxplots showing the median and IQR whiskers so viewers see the real spread."*
  * *"We also printed the exact sample size (n) and units clearly, using colorblind-safe colors."*

---

## 5. Live Dashboard Simulation: What to Show & What to Say (Slides 9 & 10)

*(Switch to your Power BI Desktop window or the HTML dashboard)*

```
┌────────────────────────────────────────────────────────────────────────┐
│                        LIVE DEMO ACTION GUIDE                          │
├────────┬──────────────────────────────┬────────────────────────────────┤
│ Step   │ What you DO on screen        │ What you SAY out loud          │
├────────┼──────────────────────────────┼────────────────────────────────┤
│ Step 1 │ Show Page 1 (Overview)       │ "Here is our 29K record map..."│
│ Step 2 │ Click Slicer: 'Ocean water'  │ "Notice the unit isolation..." │
│ Step 3 │ Switch to Page 2 (Basins)    │ "Let's filter by Pacific..."   │
│ Step 4 │ Switch to Page 3 (Methods)   │ "Here is the net mesh bias..." │
└────────┴──────────────────────────────┴────────────────────────────────┘
```

### 🔹 Action 1: Show the Overview Page (Page 1)
* **What to Show:** Point your mouse to the top 4 KPI cards and the central map.
* **What to Say:**
  * *"Here is Page 1 of our Power BI dashboard. At the top, you immediately see our verified KPIs: 29,000 observations, 100% valid coordinates, and our 94.2% Northern bias."*
  * *"The map in the center plots every single point without lag."*

### 🔹 Action 2: Click the Marine Setting Slicer
* **What to Show:** Click on the checkbox **`Ocean water`** in the left slicer.
* **What to Say:**
  * *"Now watch what happens when I select 'Ocean water'. All charts and KPIs instantly update to show only the 16,988 water samples."*
  * *"Every measurement on screen is now strictly in `pieces/m³`. This proves our DAX measures prevent any cross-unit pollution."*

### 🔹 Action 3: Go to Page 2 (Basin & Setting Deep-Dive)
* **What to Show:** Switch to Page 2, and click on **`Pacific Ocean`** in the bar chart.
* **What to Say:**
  * *"On Page 2, we compare the ocean basins. When I click on the Pacific Ocean, the severity breakdown cross-filters instantly."*
  * *"You can see the Pacific median is 1.84, which is 4 times higher than the Atlantic. Even though the Atlantic has more dots on the map, the Pacific is where the plastic actually piles up."*

### 🔹 Action 4: Go to Page 3 (Methodology & Ethics)
* **What to Show:** Switch to Page 3, pointing to the mesh size chart and the side-by-side misleading vs. ethical charts.
* **What to Say:**
  * *"Finally, on Page 3, we show our methodology audit. The gear chart shows how 333-micron nets miss fine fibers."*
  * *"And on the right side, we built the live misleading versus ethical comparison directly inside Power BI for stakeholders to see the difference."*

---

## 6. Final Insights & Wrap-Up (Slide 12 & 13)

### 🗣️ What to Say:
* *"To wrap up, here are our **three main conclusions**:"*

1. **More Samples Does Not Mean More Pollution:**
   * *"The Atlantic looks crowded on a map simply because research ships travel there more often. True pollution peaks in the Pacific gyre."*
2. **Never Mix Incompatible Units:**
   * *"Water, beach, and sediment measurements must always be analyzed separately to prevent false conclusions."*
3. **Actionable Policy Recommendation:**
   * *"Pre-production plastic pellets (nurdles) cause massive coastal spills. We recommend that the International Maritime Organization (IMO) officially classifies nurdles as Hazardous Cargo to require secure shipping."*

### 🏁 Closing Line:
* *"This project shows that honest, bias-aware data visualization protects public trust and helps cleanup funds go to the real problem areas."*
* *"Thank you! I am now ready for your questions."*

---

## 💡 Quick Viva Defense Answers (If the Examiner Asks)

* **Q: Why didn't you convert pieces/10 min into pieces/m³?**
  * **Your Answer:** *"Because pieces per 10 minutes is a timed walking search on sand. We do not know the water volume, depth, or speed, so converting it mathematically is impossible and scientifically wrong."*

* **Q: Why did you use Median instead of Mean?**
  * **Your Answer:** *"Because plastic counts have extreme outliers—some samples are 0.001 and some are over 10,000. The mean gets pulled by a few huge spikes, but the median tells you what is normal."*

* **Q: What data model did you use in Power BI?**
  * **Your Answer:** *"We built a Star Schema with 1 Fact table (`Fact_Observations`) and 6 Dimension tables (`Dim_Calendar`, `Dim_Ocean`, `Dim_MarineSetting`, `Dim_SamplingMethod`, `Dim_Organization`, and `Dim_EthicalAudit`)."*
