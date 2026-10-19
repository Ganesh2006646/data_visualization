# 🎓 Viva & Dashboard Demonstration Guide (CSE355)
## High-Scoring Defense Answers for Case Study Evaluation (3 / 3 Marks)

Use this quick-reference guide during your practical demonstration and viva to justify your analytical, statistical, and design decisions confidently.

---

### Q1: What is the problem statement of your case study, and why is it significant?
> **Answer:**  
> "Global marine microplastic surveillance is fragmented and plagued by three major distortions:
> 1. **Unit Incompatibility:** Surface waters ($\text{pieces/m}^3$) cannot be averaged with beach counts or sediment cores ($\text{pieces/kg}$).
> 2. **Geographical Inequality:** 93.8% of global data comes from the Northern Hemisphere, while the Southern Ocean represents a major blindspot ($0.2\%$).
> 3. **Equipment Bias:** Net apertures vary between $0.05\text{ mm}$ and $1.0\text{ mm}$, meaning observed differences often reflect gear rather than true pollution.  
> Our case study harmonizes 29,076 NOAA records across 54 years to decouple monitoring effort from true ecological risk."

---

### Q2: What three visualization tools did you use, and why?
> **Answer:**  
> "We used three distinct tools to satisfy the rubric:
> 1. **Python (Matplotlib & Seaborn):** Used in the Jupyter Notebook for statistical modeling, marginal KDE density maps, symlog scaling, and Kruskal-Wallis hypothesis testing.
> 2. **Microsoft Power BI Desktop:** Used for the 4-page executive interactive dashboard (`.pbip`) featuring a Star Schema, 22 certified DAX measures, and synchronized cross-filtering.
> 3. **Plotly (JavaScript/HTML):** Used for the responsive web dashboard (`power_bi_interactive_dashboard.html`), enabling zero-install, client-side exploration with 14 interactive charts."

---

### Q3: Explain your intentionally misleading visualization and how your ethical redesign corrects it.
> **Answer:**  
> "In Visualization V9 (and Page 4 of our Power BI dashboard):
> - **The Misleading Chart:** We intentionally truncated the Y-axis to start at $0.200$ instead of $0.000$ for the years 2019–2021. This made a minor $10\%$ shift ($0.210 \rightarrow 0.231\text{ pieces/m}^3$) appear as an alarming **300% visual spike**. It also concealed the drop in sample size ($589 \rightarrow 289$ tows) due to COVID-19 and omitted distribution spread.
> - **The Ethical Redesign:** We restored the true zero baseline ($0.000$) and displayed 25th–75th percentile Interquartile Range (IQR) error bounds ($\sim 0.97$). This proved that annual medians were virtually flat, and that natural spatial oceanic variance completely dwarfs year-over-year differences."

---

### Q4: Why did you use non-parametric statistics (Medians, IQR, Kruskal-Wallis) instead of Means and Standard Deviations?
> **Answer:**  
> "Environmental particle concentrations are heavily right-skewed and zero-inflated ($22.7\%$ zeros in water, $46.5\%$ in beach walks). A few extreme outliers (e.g. $>40,000\text{ pieces/m}^3$ in convergence zones) artificially inflate the arithmetic mean, making it unrepresentative of typical conditions. Non-parametric medians and IQRs provide robust, unbiased measures of central tendency."

---

### Q5: How did you prove that net mesh size creates sampling bias?
> **Answer:**  
> "In Visualization V7, we performed a Spearman rank correlation between net mesh aperture ($\text{mm}$) and reported concentration. We obtained a strong, statistically significant inverse relationship ($r_s = -0.415, p < 10^{-100}$). Standard nets ($0.333\text{ mm}$) miss fine microplastics (median $0.0080\text{ pieces/m}^3$), while fine nets ($<0.10\text{ mm}$) capture **100× to 1,000× more particles** ($2.4–16.0+\text{ pieces/m}^3$). This proves that regional differences often reflect equipment rather than actual pollution."

---

### Q6: How is your Power BI data model structured, and how did you prevent `(Blank)` visual errors?
> **Answer:**  
> "We engineered a clean Star Schema in `model.bim` consisting of one central fact table (`Fact_Observations`, 29,076 rows) and six dimension tables (`Dim_Calendar`, `Dim_Ocean`, `Dim_MarineSetting`, `Dim_SamplingMethod`, `Dim_Organization`, and `Dim_EthicalAudit`).  
> To guarantee zero `(Blank)` cards during slicer interactions, every single DAX measure is hardened with `COALESCE` and `DIVIDE(..., 0.0)`. Furthermore, all CSV partitions use `QuoteStyle.Csv` to prevent delimiter errors."

---

### Q7: What are the key takeaways from your 4-page Power BI dashboard?
> **Answer:**  
> - **Page 1 (Surveillance):** Highlights the 93.8% Northern Hemisphere bias and separates the 2018+ citizen science volume surge from stable ocean water baselines.
> - **Page 2 (Basin Risks):** Features our 8-column Ocean Basin Scorecard Matrix, showing Indian and Arctic Oceans have the highest median levels ($p < 10^{-90}$).
> - **Page 3 (Governance):** Reveals that two entities (UTMSI and SEA) account for 66.3% of global surveillance, calling for decentralized monitoring.
> - **Page 4 (Ethics):** Demonstrates our side-by-side misleading vs. ethical redesign and formalizes the Four Cardinal Rules of Environmental Data Visualization."
