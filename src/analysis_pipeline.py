"""Reproducible cleaning and analysis pipeline for the NOAA marine microplastics dataset."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW_CSV = ROOT / "data" / "raw" / "Hub_Microplastics_Replace_6120810666638033289.csv"
PROCESSED_DIR = ROOT / "data" / "processed"


def _ensure_dirs() -> Path:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    return PROCESSED_DIR


def load_data(raw_csv_path: str | Path | None = None) -> pd.DataFrame:
    """Load the NOAA marine microplastics dataset and add analysis-ready fields.

    If a cleaned master file already exists, reuse it to avoid reprocessing. Otherwise,
    read the raw CSV, normalize fields, and produce the standard analytic features used
    across the project notebooks and dashboard.
    """
    resolved_path = Path(raw_csv_path) if raw_csv_path else RAW_CSV
    processed_path = PROCESSED_DIR / "cleaned_master.csv"

    if processed_path.exists() and not raw_csv_path:
        df = pd.read_csv(processed_path, low_memory=False)
        if "Sample Date Parsed" in df.columns:
            df["Sample Date Parsed"] = pd.to_datetime(df["Sample Date Parsed"], errors="coerce")
        return df

    if not resolved_path.exists():
        raise FileNotFoundError(f"Dataset not found: {resolved_path}")

    df = pd.read_csv(resolved_path, low_memory=False)
    df = df.rename(columns={"Standardized Nurdle  Amount": "Standardized Nurdle Amount"})

    date_col = "Sample Date"
    df["Sample Date Parsed"] = pd.to_datetime(df[date_col], format="%m/%d/%Y %I:%M:%S %p", errors="coerce")
    df["Year"] = pd.to_numeric(df["Sample Date Parsed"].dt.year, errors="coerce")
    df["Month"] = pd.to_numeric(df["Sample Date Parsed"].dt.month, errors="coerce")
    df["Decade"] = (df["Year"] // 10) * 10

    df["Latitude Numeric"] = pd.to_numeric(df["Latitude (degree)"], errors="coerce")
    df["Longitude Numeric"] = pd.to_numeric(df["Longitude (degree)"], errors="coerce")
    df["Measurement Numeric"] = pd.to_numeric(df["Microplastics Measurement"], errors="coerce")
    df["Nurdle Numeric"] = pd.to_numeric(df["Standardized Nurdle Amount"], errors="coerce")
    df["Mesh Numeric"] = pd.to_numeric(df["Mesh Size (mm)"], errors="coerce")

    df["Valid Coordinates"] = (
        df["Latitude Numeric"].between(-90, 90)
        & df["Longitude Numeric"].between(-180, 180)
        & ~(df["Latitude Numeric"].eq(0) & df["Longitude Numeric"].eq(0))
    )

    df["Repeated Location Date Reference"] = df.duplicated(
        subset=["Latitude Numeric", "Longitude Numeric", "Sample Date Parsed", "Short Reference"],
        keep=False,
    )

    df["Measurement For Analysis"] = np.where(
        df["Measurement Numeric"].notna(),
        df["Measurement Numeric"],
        np.where(df["Marine Setting"].eq("Nurdle Patrol"), df["Nurdle Numeric"], np.nan),
    )

    df["Log1p Measurement"] = np.log1p(df["Measurement For Analysis"].replace(0, np.nan))

    return df


def data_quality(df: pd.DataFrame) -> dict[str, Any]:
    """Summarize the dataset quality and analytical profile."""
    parsed_dates = pd.to_datetime(df["Sample Date Parsed"], errors="coerce")
    date_min = parsed_dates.min()
    date_max = parsed_dates.max()
    original_columns = len(pd.read_csv(RAW_CSV, nrows=1).columns)
    return {
        "records": int(len(df)),
        "original_columns": int(original_columns),
        "date_min": date_min.strftime("%Y-%m-%d") if pd.notna(date_min) else None,
        "date_max": date_max.strftime("%Y-%m-%d") if pd.notna(date_max) else None,
        "valid_coordinates": int(df["Valid Coordinates"].sum()),
        "duplicate_rows": int(df.duplicated().sum()),
        "duplicate_ids": int(df["Unique ID"].duplicated().sum()),
        "nurdle_records": int(df["Marine Setting"].eq("Nurdle Patrol").sum()),
        "water_records": int(df["Marine Setting"].eq("Ocean water").sum()),
    }


def _write_context_exports(df: pd.DataFrame) -> None:
    exports = {
        "beach_pieces_m3.csv": df[(df["Marine Setting"] == "Beach") & (df["Unit"] == "pieces/m3")],
        "ocean_water_pieces_m3.csv": df[(df["Marine Setting"] == "Ocean water") & (df["Unit"] == "pieces/m3")],
        "ocean_sediment_pieces_kg_dw.csv": df[(df["Marine Setting"] == "Ocean sediment") & (df["Unit"] == "pieces kg-1 d.w.")],
        "nurdle_patrol_standardized_10min.csv": df[(df["Marine Setting"] == "Nurdle Patrol") & (df["Unit"] == "pieces/10 mins")],
    }

    for filename, frame in exports.items():
        if not frame.empty:
            frame.to_csv(PROCESSED_DIR / filename, index=False)

    dashboard = df[[
        "Unique ID",
        "Sample Date Parsed",
        "Year",
        "Latitude Numeric",
        "Longitude Numeric",
        "Ocean",
        "Region",
        "Marine Setting",
        "Sampling Method",
        "Mesh Numeric",
        "Unit",
        "Measurement For Analysis",
        "Concentration Class",
        "Valid Coordinates",
    ]].copy()
    dashboard["Measurement For Analysis"] = pd.to_numeric(dashboard["Measurement For Analysis"], errors="coerce")
    dashboard.to_csv(PROCESSED_DIR / "dashboard_records.csv", index=False)


def run(raw_csv_path: str | Path | None = None) -> pd.DataFrame:
    """Run the full cleaning pipeline and persist the processed outputs used by the notebook and dashboard."""
    _ensure_dirs()
    df = load_data(raw_csv_path)
    light = df.copy()
    light = light.loc[:, ~light.columns.duplicated()]
    light.to_csv(PROCESSED_DIR / "cleaned_master.csv", index=False)
    _write_context_exports(light)

    metrics = data_quality(light)
    (PROCESSED_DIR / "verified_metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    return light


def main() -> None:
    df = run()
    metrics = data_quality(df)
    print(f"Shape after analysis features: {df.shape}")
    print(f"Original source columns: {metrics['original_columns']}")
    print(f"Columns: {df.columns.tolist()}")


if __name__ == "__main__":
    main()
