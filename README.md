# Global Marine Microplastic Pollution Analytics

This project implements the CSE355 case study for K Ganesh Giridhar (CB.SC.U4CSE24519) using the NOAA NCEI marine microplastics dataset.

## Verified Source Profile

- 29,076 records and 35 original columns
- Parsed dates: 1972-04-20 through 2026-04-28
- Four settings: Ocean water, Beach, Ocean sediment, and Nurdle Patrol
- Numeric measurements are never pooled across incompatible units or settings
- The original raw CSV is preserved unchanged in `data/raw/`

## Setup

```bash
# Optional: create and activate a virtual environment
python -m venv .venv
# Windows (PowerShell): .venv\Scripts\Activate.ps1
# Linux / macOS:        source .venv/bin/activate

pip install -r requirements.txt
jupyter notebook notebooks/marine_microplastics_analysis.ipynb
```

## Ethical Analysis Rules

`pieces/m3`, `pieces/10 mins`, and `pieces kg-1 d.w.` are kept strictly separate. Beach and Ocean water both use `pieces/m3` but have different concentration-class ranges, so they are separated by marine setting. Nurdle Patrol uses the standardized 10-minute field and its NOAA metadata caveat is retained.

## Project Contents

- `notebooks/marine_microplastics_analysis.ipynb`: self-contained, executed visual analytics notebook with inline V1–V9 visualizations, statistical testing, and forensic data checks
- `data/raw/`: preserved NOAA NCEI source CSV and Phase 1 specification
- `data/processed/`: cleaned dataset partitions
- `src/`: data processing pipeline source code
- `dashboard/`: dashboard directory
