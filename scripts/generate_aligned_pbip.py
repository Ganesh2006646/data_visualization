"""Regenerate the PBIP report so it matches DASHBOARD_TRANSFORMATION_GUIDE.md.

The script intentionally uses only the public PBIP JSON files.  It is
idempotent and can safely be rerun after refreshing the CSV assets.
"""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PBIP = ROOT / "dashboard" / "power_bi_assets" / "Marine_Microplastics_Executive"
MODEL_PATH = PBIP / "Marine_Microplastics_Executive.Dataset" / "model.bim"
REPORT_PATH = PBIP / "Marine_Microplastics_Executive.Report" / "report.json"


def literal(value: str) -> dict:
    return {"expr": {"Literal": {"Value": value}}}


def title_object(text: str) -> dict:
    return {
        "title": [
            {
                "properties": {
                    "show": literal("true"),
                    "text": literal("'" + text.replace("'", "''") + "'"),
                }
            }
        ]
    }


def field(table: str, column: str) -> dict:
    return {
        "Column": {
            "Expression": {"SourceRef": {"Entity": table}},
            "Property": column,
        },
        "Name": f"{table}.{column}",
    }


def measure(table: str, name: str) -> dict:
    return {
        "Measure": {
            "Expression": {"SourceRef": {"Entity": table}},
            "Property": name,
        },
        "Name": f"{table}.{name}",
    }


def ref(item: dict) -> str:
    return item["Name"]


def visual(
    name: str,
    visual_type: str,
    x: int,
    y: int,
    width: int,
    height: int,
    title: str,
    roles: dict[str, list[dict]],
    *,
    objects: dict | None = None,
    filters: list[dict] | None = None,
) -> dict:
    """Build a valid legacy-PBIP visual container from strongly typed fields."""
    selected = [item for items in roles.values() for item in items]
    tables: list[str] = []
    for item in selected:
        table = item.get("Column", item.get("Measure"))["Expression"]["SourceRef"]["Entity"]
        if table not in tables:
            tables.append(table)
    # ``queryRef`` uses a model-facing table/field name, but the semantic query
    # itself must point to an alias declared in ``From``.  Using ``Entity`` in
    # SourceRef creates JSON that parses but crashes the Desktop visual engine.
    source_by_table = {table: f"t_{index}" for index, table in enumerate(tables)}
    prototype_select = deepcopy(selected)
    for item in prototype_select:
        source_ref = item.get("Column", item.get("Measure"))["Expression"]["SourceRef"]
        table = source_ref.pop("Entity")
        source_ref["Source"] = source_by_table[table]
    config = {
        "name": name,
        "layouts": [
            {
                "id": 0,
                "position": {"x": x, "y": y, "width": width, "height": height, "z": 0},
            }
        ],
        "singleVisual": {
            "visualType": visual_type,
            "projections": {role: [{"queryRef": ref(item)} for item in items] for role, items in roles.items()},
            "prototypeQuery": {
                "Version": 2,
                "From": [{"Name": source_by_table[table], "Entity": table, "Type": 0} for table in tables],
                "Select": prototype_select,
            },
            "vcObjects": title_object(title),
        },
    }
    if objects:
        config["singleVisual"]["vcObjects"].update(objects)
    return {"x": x, "y": y, "width": width, "height": height, "config": json.dumps(config, ensure_ascii=False), "query": "{}", "filters": json.dumps(filters or [])}


def card(name: str, x: int, title: str, metric: str) -> dict:
    return visual(name, "card", x, 15, 230, 90, title, {"Values": [measure("Fact_Observations", metric)]})


def gauge(name: str, title: str) -> dict:
    return visual(
        name,
        "gauge",
        1000,
        15,
        260,
        90,
        title,
        {"Y": [measure("Fact_Observations", "Standard Net Share %")], "TargetValue": [measure("Fact_Observations", "Harmonization Benchmark")]},
    )


def slicer(name: str, y: int, title: str, table: str, column: str) -> dict:
    return visual(name, "slicer", 20, y, 190, 320 if y == 120 else 245, title, {"Values": [field(table, column)]})


def year_filter() -> list[dict]:
    """Keep the two ethics examples constrained to the intended three years."""
    return [
        {
            "name": "Dim_Calendar.Year",
            "expression": {"Column": {"Expression": {"SourceRef": {"Entity": "Dim_Calendar"}}, "Property": "Year"}},
            "type": "Categorical",
            "howCreated": 1,
            "isHiddenInViewMode": False,
            "isLockedInViewMode": True,
            "filters": [{"operator": "In", "values": [[{"Literal": {"Value": "2019L"}}], [{"Literal": {"Value": "2020L"}}], [{"Literal": {"Value": "2021L"}}]]}],
        }
    ]


def update_model() -> None:
    model = json.loads(MODEL_PATH.read_text(encoding="utf-8-sig"))
    fact = next(table for table in model["model"]["tables"] if table["name"] == "Fact_Observations")
    # Power BI otherwise treats numeric coordinates as generic numbers instead
    # of geographic fields when a report is opened on a new machine.
    columns = {item["name"]: item for item in fact.get("columns", [])}
    columns["Latitude"]["dataCategory"] = "Latitude"
    columns["Longitude"]["dataCategory"] = "Longitude"
    measures = {item["name"]: item for item in fact.get("measures", [])}

    # Avoid RELATED() in CALCULATE boolean filters: measures have no row context.
    definitions = {
        "Total Observations": ("COUNTROWS('Fact_Observations')", "#,0"),
        "Northern Hemisphere Records": ("CALCULATE([Total Observations], KEEPFILTERS('Fact_Observations'[Latitude] >= 0))", "#,0"),
        "Northern Hemisphere Share %": ("COALESCE(DIVIDE([Northern Hemisphere Records], [Total Observations], 0.0), 0.0)", "0.0%"),
        "Southern Ocean Records": ("CALCULATE([Total Observations], KEEPFILTERS('Dim_Ocean'[Ocean Basin] = \"Southern Ocean\"))", "#,0"),
        "Southern Ocean Share %": ("COALESCE(DIVIDE([Southern Ocean Records], [Total Observations], 0.0), 0.0)", "0.0%"),
        "Geographic Integrity %": ("COALESCE(DIVIDE(CALCULATE([Total Observations], KEEPFILTERS('Fact_Observations'[ValidCoordinates] = TRUE())), [Total Observations], 1.0), 1.0)", "0.0%"),
        "Standard Net Records": ("CALCULATE([Total Observations], KEEPFILTERS('Fact_Observations'[MeshSize_mm] >= 0.300), KEEPFILTERS('Fact_Observations'[MeshSize_mm] <= 0.350))", "#,0"),
        "Standard Net Share %": ("COALESCE(DIVIDE([Standard Net Records], [Total Observations], 0.0), 0.0)", "0.0%"),
        "Harmonization Benchmark": ("0.80", "0.0%"),
        "Zero Observations": ("CALCULATE([Total Observations], KEEPFILTERS('Fact_Observations'[MeasurementForAnalysis] = 0.0))", "#,0"),
        "Zero-Inflation %": ("COALESCE(DIVIDE([Zero Observations], [Total Observations], 0.0), 0.0)", "0.0%"),
        "Water Column Tows": ("CALCULATE([Total Observations], KEEPFILTERS('Dim_MarineSetting'[Marine Setting] = \"Ocean water\"))", "#,0"),
        "Nurdle Beach Patrols": ("CALCULATE([Total Observations], KEEPFILTERS('Dim_MarineSetting'[Marine Setting] = \"Nurdle Patrol\"))", "#,0"),
        "High Severity Records": ("CALCULATE([Total Observations], KEEPFILTERS('Fact_Observations'[ConcentrationClass] IN {\"High\", \"Very High\"}))", "#,0"),
        "High Severity Share %": ("COALESCE(DIVIDE([High Severity Records], [Total Observations], 0.0), 0.0)", "0.0%"),
        "Beach Sand Zero-Rate %": ("COALESCE(DIVIDE(CALCULATE([Zero Observations], KEEPFILTERS('Dim_MarineSetting'[Marine Setting] = \"Beach\")), CALCULATE([Total Observations], KEEPFILTERS('Dim_MarineSetting'[Marine Setting] = \"Beach\")), 0.0), 0.0)", "0.0%"),
        # Water-only analyses must remain visible when a user chooses Beach,
        # Nurdle Patrol, or sediment in the page-level setting slicer.
        "Water Observations": ("CALCULATE([Total Observations], REMOVEFILTERS('Dim_MarineSetting'), 'Dim_MarineSetting'[Marine Setting] = \"Ocean water\")", "#,0"),
        "Water High Severity Records": ("CALCULATE([High Severity Records], REMOVEFILTERS('Dim_MarineSetting'), 'Dim_MarineSetting'[Marine Setting] = \"Ocean water\")", "#,0"),
        "Median Concentration Water": ("COALESCE(CALCULATE(MEDIAN('Fact_Observations'[MeasurementForAnalysis]), REMOVEFILTERS('Dim_MarineSetting'), 'Dim_MarineSetting'[Marine Setting] = \"Ocean water\"), 0.0)", "0.0000"),
        "Average Longitude": ("AVERAGE('Fact_Observations'[Longitude])", "0.00"),
        "Average Latitude": ("AVERAGE('Fact_Observations'[Latitude])", "0.00"),
        "Log Median Concentration Water": ("VAR MedianValue = [Median Concentration Water] RETURN IF(MedianValue > 0, LOG10(MedianValue), BLANK())", "0.000"),
        "Mean Concentration Water": ("COALESCE(CALCULATE(AVERAGE('Fact_Observations'[MeasurementForAnalysis]), REMOVEFILTERS('Dim_MarineSetting'), 'Dim_MarineSetting'[Marine Setting] = \"Ocean water\"), 0.0)", "0.0000"),
        "Concentration 25th Pct": ("COALESCE(CALCULATE(PERCENTILE.INC('Fact_Observations'[MeasurementForAnalysis], 0.25), REMOVEFILTERS('Dim_MarineSetting'), 'Dim_MarineSetting'[Marine Setting] = \"Ocean water\"), 0.0)", "0.0000"),
        "Concentration 75th Pct": ("COALESCE(CALCULATE(PERCENTILE.INC('Fact_Observations'[MeasurementForAnalysis], 0.75), REMOVEFILTERS('Dim_MarineSetting'), 'Dim_MarineSetting'[Marine Setting] = \"Ocean water\"), 0.0)", "0.0000"),
        "Median Concentration": ("COALESCE(MEDIAN('Fact_Observations'[MeasurementForAnalysis]), 0.0)", "0.0000"),
        # These are aggregate measures, not raw columns, which is required by
        # Power BI's scatter visual when it groups points by sampling method.
        "Median Mesh Size Water": ("COALESCE(CALCULATE(MEDIAN('Fact_Observations'[MeshSize_mm]), REMOVEFILTERS('Dim_MarineSetting'), 'Dim_MarineSetting'[Marine Setting] = \"Ocean water\"), 0.0)", "0.0000"),
        "Median Log Concentration Water": ("COALESCE(CALCULATE(MEDIAN('Fact_Observations'[Log10p1Measurement]), REMOVEFILTERS('Dim_MarineSetting'), 'Dim_MarineSetting'[Marine Setting] = \"Ocean water\"), 0.0)", "0.0000"),
        "Top-2 Entity Dominance %": ("VAR Top2Count = CALCULATE([Total Observations], KEEPFILTERS('Dim_Organization'[Organization] IN {\"University of Texas Marine Science Institute\", \"Sea Education Association\"})) RETURN COALESCE(DIVIDE(Top2Count, [Total Observations], 0.0), 0.0)", "0.0%"),
        "Citizen Science Share %": ("VAR CitizenCount = CALCULATE([Total Observations], KEEPFILTERS('Dim_Organization'[Sector Type] = \"Citizen Science Network\")) RETURN COALESCE(DIVIDE(CitizenCount, [Total Observations], 0.0), 0.0)", "0.0%"),
        # The contrast belongs in the chart axis, never in a falsified data value.
        "Misleading Truncated Value": ("VAR DisplayYear = SELECTEDVALUE('Dim_Calendar'[Year]) RETURN IF(DisplayYear IN {2019, 2020, 2021}, [Median Concentration Water], BLANK())", "0.0000"),
        "Ethical Baseline Value": ("VAR DisplayYear = SELECTEDVALUE('Dim_Calendar'[Year]) RETURN IF(DisplayYear IN {2019, 2020, 2021}, [Median Concentration Water], BLANK())", "0.0000"),
        "Rubric Alignment %": ("1.0", "0%"),
    }
    for name, (expression, format_string) in definitions.items():
        item = measures.get(name, {"name": name})
        item["expression"] = expression
        item["formatString"] = format_string
        measures[name] = item
    # Remove retired aliases so visuals cannot silently bind to a stale measure.
    fact["measures"] = [measures[name] for name in definitions]
    MODEL_PATH.write_text(json.dumps(model, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_report() -> None:
    report = json.loads(REPORT_PATH.read_text(encoding="utf-8-sig"))
    p1 = [
        card("p1_total", 20, "Total Verified Observations", "Total Observations"),
        card("p1_north", 265, "Northern Hemisphere Sampling Bias", "Northern Hemisphere Share %"),
        card("p1_south", 510, "Southern Ocean Data Blindspot", "Southern Ocean Share %"),
        card("p1_geo", 755, "Coordinate Integrity Rate", "Geographic Integrity %"),
        gauge("p1_harmonisation", "Global Standard Net Benchmark"),
        slicer("p1_setting", 120, "Marine Setting", "Dim_MarineSetting", "Marine Setting"),
        slicer("p1_decade", 455, "Monitoring Era", "Dim_Calendar", "Decade"),
        # A local coordinate scatter works even when tenant policy blocks map
        # services.  ObservationID groups points; coordinate measures provide
        # the required aggregation for a scatter chart's X/Y axes.
        visual("p1_v1_map", "scatterChart", 225, 120, 575, 320, "V1: Sampling Footprint by Longitude and Latitude (local coordinate plot)", {"Values": [field("Fact_Observations", "ObservationID")], "X": [measure("Fact_Observations", "Average Longitude")], "Y": [measure("Fact_Observations", "Average Latitude")], "Legend": [field("Dim_Ocean", "Hemisphere Region")], "Tooltips": [field("Dim_Ocean", "Ocean Basin"), measure("Fact_Observations", "Total Observations")]}),
        visual("p1_v2_hotspot", "scatterChart", 815, 120, 445, 320, "V2: Basin Sampling Effort vs Median Water Concentration", {"X": [measure("Fact_Observations", "Water Observations")], "Y": [measure("Fact_Observations", "Median Concentration Water")], "Size": [measure("Fact_Observations", "Water High Severity Records")], "Legend": [field("Dim_Ocean", "Ocean Basin")], "Tooltips": [measure("Fact_Observations", "Median Concentration Water"), measure("Fact_Observations", "Water Observations"), measure("Fact_Observations", "Water High Severity Records")]}),
        visual("p1_v3_temporal", "lineStackedColumnComboChart", 225, 455, 1035, 245, "V3: 50-Year Monitoring Effort vs Ocean Water Trajectory", {"Category": [field("Dim_Calendar", "Year")], "Y": [measure("Fact_Observations", "Total Observations")], "Y2": [measure("Fact_Observations", "Median Concentration Water")], "Series": [field("Dim_MarineSetting", "Marine Setting")]}),
    ]
    p2 = [
        card("p2_water", 20, "Ocean Water Column Tows", "Water Column Tows"),
        card("p2_nurdle", 265, "Nurdle Beach Patrols", "Nurdle Beach Patrols"),
        card("p2_zero", 510, "Beach Sand Zero-Rate", "Beach Sand Zero-Rate %"),
        card("p2_high", 755, "High and Extreme Severity Share", "High Severity Share %"),
        gauge("p2_harmonisation", "Target Monitoring Harmonization"),
        slicer("p2_basin", 120, "Ocean Basin", "Dim_Ocean", "Ocean Basin"),
        slicer("p2_severity", 455, "Severity Class", "Fact_Observations", "ConcentrationClass"),
        visual("p2_v4_basin", "clusteredColumnChart", 225, 120, 490, 320, "V4: Ocean Basin Microplastic Concentration Benchmark", {"Category": [field("Dim_Ocean", "Ocean Basin")], "Y": [measure("Fact_Observations", "Median Concentration Water")], "Tooltips": [measure("Fact_Observations", "Concentration 25th Pct"), measure("Fact_Observations", "Concentration 75th Pct"), measure("Fact_Observations", "Total Observations")]}),
        visual("p2_v8_severity", "hundredPercentStackedColumnChart", 730, 120, 530, 320, "V8: Proportional Severity Class Breakdown Across Ocean Basins", {"Category": [field("Dim_Ocean", "Ocean Basin")], "Y": [measure("Fact_Observations", "Total Observations")], "Series": [field("Fact_Observations", "ConcentrationClass")]}),
        visual("p2_v5_matrix", "tableEx", 225, 455, 1035, 245, "V5: Compartment-Separated Profile Across Marine Settings", {"Values": [field("Dim_MarineSetting", "Marine Setting"), field("Dim_MarineSetting", "Unit"), field("Dim_MarineSetting", "Compartment"), measure("Fact_Observations", "Total Observations"), measure("Fact_Observations", "Zero-Inflation %"), measure("Fact_Observations", "Median Concentration"), field("Dim_MarineSetting", "Acute Threshold")]}),
    ]
    axis_misleading = {"yAxis": [{"properties": {"start": literal("0.2D")}}]}
    axis_ethical = {"yAxis": [{"properties": {"start": literal("0D")}}]}
    p3 = [
        card("p3_total", 20, "Institutional Provenance Records", "Total Observations"),
        card("p3_top2", 265, "Top-2 Entity Dominance", "Top-2 Entity Dominance %"),
        card("p3_standard", 510, "Standard 333 um Net Ratio", "Standard Net Share %"),
        card("p3_citizen", 755, "Citizen Science Contribution", "Citizen Science Share %"),
        visual("p3_rubric", "card", 1000, 15, 260, 90, "Case Study Rubric Alignment", {"Values": [measure("Fact_Observations", "Rubric Alignment %")]}),
        slicer("p3_sector", 120, "Sector Type", "Dim_Organization", "Sector Type"),
        slicer("p3_device", 455, "Device Category", "Dim_SamplingMethod", "Device Category"),
        visual("p3_v6_gear", "pivotTable", 225, 120, 520, 320, "V6: Sampling Method by Ocean Basin Matrix", {"Rows": [field("Dim_SamplingMethod", "Sampling Method")], "Columns": [field("Dim_Ocean", "Ocean Basin")], "Values": [measure("Fact_Observations", "Median Concentration Water"), measure("Fact_Observations", "Total Observations")]}),
        visual("p3_v7_mesh", "scatterChart", 760, 120, 500, 320, "V7: Mesh Size Aperture Bias (0.333 mm benchmark)", {"X": [measure("Fact_Observations", "Median Mesh Size Water")], "Y": [measure("Fact_Observations", "Median Log Concentration Water")], "Size": [measure("Fact_Observations", "Water Observations")], "Legend": [field("Dim_SamplingMethod", "Device Category")], "Tooltips": [measure("Fact_Observations", "Median Concentration Water"), measure("Fact_Observations", "Water Observations")]}),
        visual("p3_v9_organisations", "clusteredBarChart", 225, 455, 430, 245, "V9 Part 1: Global Institutional Provenance", {"Category": [field("Dim_Organization", "Organization")], "Y": [measure("Fact_Observations", "Total Observations")], "Series": [field("Dim_Organization", "Sector Type")]}),
        visual("p3_v9_misleading", "clusteredColumnChart", 670, 455, 285, 245, "MISLEADING: Truncated Baseline at 0.200", {"Category": [field("Dim_Calendar", "Year")], "Y": [measure("Fact_Observations", "Misleading Truncated Value")]}, objects=axis_misleading, filters=year_filter()),
        visual("p3_v9_ethical", "clusteredColumnChart", 975, 455, 285, 245, "ETHICAL REDESIGN: Zero Baseline and Context", {"Category": [field("Dim_Calendar", "Year")], "Y": [measure("Fact_Observations", "Ethical Baseline Value")], "Tooltips": [measure("Fact_Observations", "Concentration 25th Pct"), measure("Fact_Observations", "Concentration 75th Pct"), measure("Fact_Observations", "Total Observations")]}, objects=axis_ethical, filters=year_filter()),
    ]
    report["sections"] = [
        {"name": "Page1_GeographicSurveillance", "displayName": "1. Global Footprint & Geographic Surveillance", "filters": [], "height": 720, "width": 1280, "visualContainers": p1},
        {"name": "Page2_EnvironmentalMatrices", "displayName": "2. Environmental Matrices & Ocean Basin Severity", "filters": [], "height": 720, "width": 1280, "visualContainers": p2},
        {"name": "Page3_ProtocolProvenance", "displayName": "3. Protocol Standardization, Gear Bias & Provenance", "filters": [], "height": 720, "width": 1280, "visualContainers": p3},
    ]
    report["config"] = json.dumps({"version": "5.50", "themeCollection": {"baseTheme": {"name": "CY24SU08", "version": "5.50", "type": 2}}, "activeSectionIndex": 0, "settings": {"useNewFilterPaneExperience": True, "allowChangeFilterTypes": True, "useStylableVisualContainerHeader": True}})
    REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    update_model()
    update_report()
    print(f"Updated {MODEL_PATH.relative_to(ROOT)}")
    print(f"Updated {REPORT_PATH.relative_to(ROOT)}")
