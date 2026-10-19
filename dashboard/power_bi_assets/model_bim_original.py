"""
Generate complete native Power BI Project (.pbip) with pre-configured visuals in report.json.
"""
import json, uuid
from pathlib import Path

ROOT = Path(r"d:\marine_microplastic_pollution_analytics")
ASSETS_DIR = ROOT / "dashboard" / "power_bi_assets"
PBIP_ROOT = ASSETS_DIR / "Marine_Microplastics_Executive"
DATASET_DIR = PBIP_ROOT / "Marine_Microplastics_Executive.Dataset"
REPORT_DIR = PBIP_ROOT / "Marine_Microplastics_Executive.Report"

DATASET_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

def uid():
    return str(uuid.uuid4()).replace("-", "")[:20]

# 1. Root .pbip pointer
pbip_meta = {
    "version": "1.0",
    "artifacts": [
        {
            "report": {
                "path": "Marine_Microplastics_Executive.Report"
            }
        }
    ],
    "settings": {
        "enableAutoRecovery": True
    }
}
(PBIP_ROOT / "Marine_Microplastics_Executive.pbip").write_text(json.dumps(pbip_meta, indent=2), encoding="utf-8")

# 2. definition.pbir
pbir_meta = {
    "version": "1.0",
    "datasetReference": {
        "byPath": {
            "path": "../Marine_Microplastics_Executive.Dataset"
        },
        "byConnection": None
    }
}
(REPORT_DIR / "definition.pbir").write_text(json.dumps(pbir_meta, indent=2), encoding="utf-8")

# 3. definition.pbism
(DATASET_DIR / "definition.pbism").write_text(json.dumps({"version": "1.0"}, indent=2), encoding="utf-8")

# 4. Tabular model.bim with M expression partitions
CSV_PATH_ESCAPED = str(ASSETS_DIR).replace("\\", "\\\\")

model_bim = {
    "name": "Marine_Microplastics_Model",
    "compatibilityLevel": 1567,
    "model": {
        "culture": "en-US",
        "defaultPowerBIDataSourceVersion": "powerBI_V3",
        "tables": [
            {
                "name": "Fact_Observations",
                "lineageTag": "f90d1760-eac1-4596-8d26-00d159497ec5",
                "columns": [
                    {"name": "ObservationID", "dataType": "string", "sourceColumn": "ObservationID"},
                    {"name": "DateKey", "dataType": "int64", "sourceColumn": "DateKey"},
                    {"name": "DateStr", "dataType": "string", "sourceColumn": "DateStr"},
                    {"name": "OceanID", "dataType": "int64", "sourceColumn": "OceanID"},
                    {"name": "SettingID", "dataType": "int64", "sourceColumn": "SettingID"},
                    {"name": "MethodID", "dataType": "int64", "sourceColumn": "MethodID"},
                    {"name": "OrganizationID", "dataType": "int64", "sourceColumn": "OrganizationID"},
                    {"name": "Latitude", "dataType": "double", "sourceColumn": "Latitude"},
                    {"name": "Longitude", "dataType": "double", "sourceColumn": "Longitude"},
                    {"name": "ValidCoordinates", "dataType": "boolean", "sourceColumn": "ValidCoordinates"},
                    {"name": "MeasurementNumeric", "dataType": "double", "sourceColumn": "MeasurementNumeric"},
                    {"name": "NurdleNumeric", "dataType": "double", "sourceColumn": "NurdleNumeric"},
                    {"name": "MeasurementForAnalysis", "dataType": "double", "sourceColumn": "MeasurementForAnalysis"},
                    {"name": "Log10p1Measurement", "dataType": "double", "sourceColumn": "Log10p1Measurement"},
                    {"name": "ConcentrationClass", "dataType": "string", "sourceColumn": "ConcentrationClass"},
                    {"name": "MeshSize_mm", "dataType": "double", "sourceColumn": "MeshSize_mm"},
                    {"name": "ShortReference", "dataType": "string", "sourceColumn": "ShortReference"}
                ],
                "partitions": [
                    {
                        "name": "Fact_Observations",
                        "mode": "import",
                        "source": {
                            "type": "m",
                            "expression": [
                                "let",
                                f'    Source = Csv.Document(File.Contents("{CSV_PATH_ESCAPED}\\\\Fact_Observations.csv"), [Delimiter=",", Columns=17, Encoding=65001, QuoteStyle=QuoteStyle.None]),',
                                '    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
                                '    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers", {{"ObservationID", type text}, {"DateKey", Int64.Type}, {"DateStr", type text}, {"OceanID", Int64.Type}, {"SettingID", Int64.Type}, {"MethodID", Int64.Type}, {"OrganizationID", Int64.Type}, {"Latitude", type number}, {"Longitude", type number}, {"ValidCoordinates", type logical}, {"MeasurementNumeric", type number}, {"NurdleNumeric", type number}, {"MeasurementForAnalysis", type number}, {"Log10p1Measurement", type number}, {"ConcentrationClass", type text}, {"MeshSize_mm", type number}, {"ShortReference", type text}})',
                                "in",
                                '    #"Changed Type"'
                            ]
                        }
                    }
                ],
                "measures": [
                    {"name": "Total Observations", "expression": "COUNTROWS('Fact_Observations')"},
                    {"name": "Valid Geo Records", "expression": "CALCULATE([Total Observations], 'Fact_Observations'[ValidCoordinates] = TRUE())"},
                    {"name": "Geo-Coverage %", "expression": "DIVIDE([Valid Geo Records], [Total Observations], 0)", "formatString": "0.0%"},
                    {"name": "Northern Hemisphere Share %", "expression": "DIVIDE(CALCULATE([Total Observations], 'Fact_Observations'[Latitude] >= 0), [Total Observations], 0)", "formatString": "0.0%"},
                    {"name": "Context Guarded Median", "expression": "IF(HASONEVALUE('Dim_MarineSetting'[MarineSetting]) && HASONEVALUE('Dim_MarineSetting'[Unit]), MEDIAN('Fact_Observations'[MeasurementForAnalysis]), BLANK())", "formatString": "#,##0.0000"},
                    {"name": "Context Guarded Q25", "expression": "IF(HASONEVALUE('Dim_MarineSetting'[MarineSetting]) && HASONEVALUE('Dim_MarineSetting'[Unit]), PERCENTILE.INC('Fact_Observations'[MeasurementForAnalysis], 0.25), BLANK())", "formatString": "#,##0.0000"},
                    {"name": "Context Guarded Q75", "expression": "IF(HASONEVALUE('Dim_MarineSetting'[MarineSetting]) && HASONEVALUE('Dim_MarineSetting'[Unit]), PERCENTILE.INC('Fact_Observations'[MeasurementForAnalysis], 0.75), BLANK())", "formatString": "#,##0.0000"},
                    {"name": "Context Guarded IQR", "expression": "[Context Guarded Q75] - [Context Guarded Q25]", "formatString": "#,##0.0000"},
                    {"name": "Zero-Inflation %", "expression": "DIVIDE(CALCULATE([Total Observations], 'Fact_Observations'[MeasurementForAnalysis] = 0), [Total Observations], 0)", "formatString": "0.0%"},
                    {"name": "Standard Net Share %", "expression": "DIVIDE(CALCULATE([Total Observations], 'Fact_Observations'[MeshSize_mm] >= 0.330 && 'Fact_Observations'[MeshSize_mm] <= 0.340), [Total Observations], 0)", "formatString": "0.0%"}
                ]
            },
            {
                "name": "Dim_Calendar",
                "columns": [
                    {"name": "DateKey", "dataType": "int64", "sourceColumn": "DateKey"},
                    {"name": "DateStr", "dataType": "string", "sourceColumn": "DateStr"},
                    {"name": "FullDate", "dataType": "string", "sourceColumn": "FullDate"},
                    {"name": "Year", "dataType": "int64", "sourceColumn": "Year"},
                    {"name": "Month", "dataType": "int64", "sourceColumn": "Month"},
                    {"name": "MonthName", "dataType": "string", "sourceColumn": "MonthName"},
                    {"name": "Quarter", "dataType": "string", "sourceColumn": "Quarter"},
                    {"name": "Decade", "dataType": "string", "sourceColumn": "Decade"},
                    {"name": "Era", "dataType": "string", "sourceColumn": "Era"}
                ],
                "partitions": [
                    {
                        "name": "Dim_Calendar",
                        "mode": "import",
                        "source": {
                            "type": "m",
                            "expression": [
                                "let",
                                f'    Source = Csv.Document(File.Contents("{CSV_PATH_ESCAPED}\\\\Dim_Calendar.csv"), [Delimiter=",", Columns=9, Encoding=65001, QuoteStyle=QuoteStyle.None]),',
                                '    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
                                '    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers", {{"DateKey", Int64.Type}, {"DateStr", type text}, {"FullDate", type text}, {"Year", Int64.Type}, {"Month", Int64.Type}, {"MonthName", type text}, {"Quarter", type text}, {"Decade", type text}, {"Era", type text}})',
                                "in",
                                '    #"Changed Type"'
                            ]
                        }
                    }
                ]
            },
            {
                "name": "Dim_Ocean",
                "columns": [
                    {"name": "OceanID", "dataType": "int64", "sourceColumn": "OceanID"},
                    {"name": "OceanName", "dataType": "string", "sourceColumn": "OceanName"},
                    {"name": "HemisphereRegion", "dataType": "string", "sourceColumn": "HemisphereRegion"},
                    {"name": "BasinArea_Mkm2", "dataType": "double", "sourceColumn": "BasinArea_Mkm2"},
                    {"name": "PrimaryFocus", "dataType": "string", "sourceColumn": "PrimaryFocus"}
                ],
                "partitions": [
                    {
                        "name": "Dim_Ocean",
                        "mode": "import",
                        "source": {
                            "type": "m",
                            "expression": [
                                "let",
                                f'    Source = Csv.Document(File.Contents("{CSV_PATH_ESCAPED}\\\\Dim_Ocean.csv"), [Delimiter=",", Columns=5, Encoding=65001, QuoteStyle=QuoteStyle.None]),',
                                '    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
                                '    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers", {{"OceanID", Int64.Type}, {"OceanName", type text}, {"HemisphereRegion", type text}, {"BasinArea_Mkm2", type number}, {"PrimaryFocus", type text}})',
                                "in",
                                '    #"Changed Type"'
                            ]
                        }
                    }
                ]
            },
            {
                "name": "Dim_MarineSetting",
                "columns": [
                    {"name": "SettingID", "dataType": "int64", "sourceColumn": "SettingID"},
                    {"name": "MarineSetting", "dataType": "string", "sourceColumn": "MarineSetting"},
                    {"name": "Unit", "dataType": "string", "sourceColumn": "Unit"},
                    {"name": "Compartment", "dataType": "string", "sourceColumn": "Compartment"},
                    {"name": "ClassThreshold_VeryHigh", "dataType": "string", "sourceColumn": "ClassThreshold_VeryHigh"},
                    {"name": "PhysicalMatrix", "dataType": "string", "sourceColumn": "PhysicalMatrix"}
                ],
                "partitions": [
                    {
                        "name": "Dim_MarineSetting",
                        "mode": "import",
                        "source": {
                            "type": "m",
                            "expression": [
                                "let",
                                f'    Source = Csv.Document(File.Contents("{CSV_PATH_ESCAPED}\\\\Dim_MarineSetting.csv"), [Delimiter=",", Columns=6, Encoding=65001, QuoteStyle=QuoteStyle.None]),',
                                '    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
                                '    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers", {{"SettingID", Int64.Type}, {"MarineSetting", type text}, {"Unit", type text}, {"Compartment", type text}, {"ClassThreshold_VeryHigh", type text}, {"PhysicalMatrix", type text}})',
                                "in",
                                '    #"Changed Type"'
                            ]
                        }
                    }
                ]
            },
            {
                "name": "Dim_SamplingMethod",
                "columns": [
                    {"name": "MethodID", "dataType": "int64", "sourceColumn": "MethodID"},
                    {"name": "SamplingMethod", "dataType": "string", "sourceColumn": "SamplingMethod"},
                    {"name": "DeviceCategory", "dataType": "string", "sourceColumn": "DeviceCategory"}
                ],
                "partitions": [
                    {
                        "name": "Dim_SamplingMethod",
                        "mode": "import",
                        "source": {
                            "type": "m",
                            "expression": [
                                "let",
                                f'    Source = Csv.Document(File.Contents("{CSV_PATH_ESCAPED}\\\\Dim_SamplingMethod.csv"), [Delimiter=",", Columns=3, Encoding=65001, QuoteStyle=QuoteStyle.None]),',
                                '    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
                                '    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers", {{"MethodID", Int64.Type}, {"SamplingMethod", type text}, {"DeviceCategory", type text}})',
                                "in",
                                '    #"Changed Type"'
                            ]
                        }
                    }
                ]
            },
            {
                "name": "Dim_Organization",
                "columns": [
                    {"name": "OrganizationID", "dataType": "int64", "sourceColumn": "OrganizationID"},
                    {"name": "OrganizationName", "dataType": "string", "sourceColumn": "OrganizationName"},
                    {"name": "SectorType", "dataType": "string", "sourceColumn": "SectorType"},
                    {"name": "TotalRecords", "dataType": "int64", "sourceColumn": "TotalRecords"},
                    {"name": "ContributionTier", "dataType": "string", "sourceColumn": "ContributionTier"}
                ],
                "partitions": [
                    {
                        "name": "Dim_Organization",
                        "mode": "import",
                        "source": {
                            "type": "m",
                            "expression": [
                                "let",
                                f'    Source = Csv.Document(File.Contents("{CSV_PATH_ESCAPED}\\\\Dim_Organization.csv"), [Delimiter=",", Columns=5, Encoding=65001, QuoteStyle=QuoteStyle.None]),',
                                '    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
                                '    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers", {{"OrganizationID", Int64.Type}, {"OrganizationName", type text}, {"SectorType", type text}, {"TotalRecords", Int64.Type}, {"ContributionTier", type text}})',
                                "in",
                                '    #"Changed Type"'
                            ]
                        }
                    }
                ]
            }
        ],
        "relationships": [
            {
                "name": "Rel_Fact_Calendar",
                "fromTable": "Fact_Observations",
                "fromColumn": "DateKey",
                "toTable": "Dim_Calendar",
                "toColumn": "DateKey"
            },
            {
                "name": "Rel_Fact_Ocean",
                "fromTable": "Fact_Observations",
                "fromColumn": "OceanID",
                "toTable": "Dim_Ocean",
                "toColumn": "OceanID"
            },
            {
                "name": "Rel_Fact_Setting",
                "fromTable": "Fact_Observations",
                "fromColumn": "SettingID",
                "toTable": "Dim_MarineSetting",
                "toColumn": "SettingID"
            },
            {
                "name": "Rel_Fact_Method",
                "fromTable": "Fact_Observations",
                "fromColumn": "MethodID",
                "toTable": "Dim_SamplingMethod",
                "toColumn": "MethodID"
            },
            {
                "name": "Rel_Fact_Org",
                "fromTable": "Fact_Observations",
                "fromColumn": "OrganizationID",
                "toTable": "Dim_Organization",
                "toColumn": "OrganizationID"
            }
        ]
    }
}

(DATASET_DIR / "model.bim").write_text(json.dumps(model_bim, indent=2), encoding="utf-8")
print("Wrote model.bim with M expression partitions")

# 5. Build rich report.json with actual visual containers
def make_card(x, y, w, h, table, measure, label):
    v_id = uid()
    cfg = {
        "name": v_id,
        "layouts": [{"id": 0, "position": {"x": x, "y": y, "z": 0, "width": w, "height": h, "tabOrder": 0}}],
        "singleVisual": {
            "visualType": "card",
            "projections": {
                "Values": [{"queryRef": f"{table}.{measure}"}]
            },
            "prototypeQuery": {
                "Version": 2,
                "From": [{"Name": "t", "Entity": table, "Type": 0}],
                "Select": [
                    {
                        "Measure": {
                            "Expression": {"SourceRef": {"Source": "t"}},
                            "Property": measure
                        },
                        "Name": f"{table}.{measure}"
                    }
                ]
            }
        }
    }
    return {
        "x": x, "y": y, "z": 0, "width": w, "height": h,
        "config": json.dumps(cfg)
    }

def make_bar_chart(x, y, w, h, cat_table, cat_col, val_table, val_measure):
    v_id = uid()
    cfg = {
        "name": v_id,
        "layouts": [{"id": 0, "position": {"x": x, "y": y, "z": 0, "width": w, "height": h, "tabOrder": 1}}],
        "singleVisual": {
            "visualType": "clusteredBarChart",
            "projections": {
                "Category": [{"queryRef": f"{cat_table}.{cat_col}"}],
                "Y": [{"queryRef": f"{val_table}.{val_measure}"}]
            },
            "prototypeQuery": {
                "Version": 2,
                "From": [
                    {"Name": "c", "Entity": cat_table, "Type": 0},
                    {"Name": "v", "Entity": val_table, "Type": 0}
                ],
                "Select": [
                    {
                        "Column": {
                            "Expression": {"SourceRef": {"Source": "c"}},
                            "Property": cat_col
                        },
                        "Name": f"{cat_table}.{cat_col}"
                    },
                    {
                        "Measure": {
                            "Expression": {"SourceRef": {"Source": "v"}},
                            "Property": val_measure
                        },
                        "Name": f"{val_table}.{val_measure}"
                    }
                ]
            }
        }
    }
    return {
        "x": x, "y": y, "z": 0, "width": w, "height": h,
        "config": json.dumps(cfg)
    }

def make_pie_chart(x, y, w, h, cat_table, cat_col, val_table, val_measure):
    v_id = uid()
    cfg = {
        "name": v_id,
        "layouts": [{"id": 0, "position": {"x": x, "y": y, "z": 0, "width": w, "height": h, "tabOrder": 2}}],
        "singleVisual": {
            "visualType": "pieChart",
            "projections": {
                "Category": [{"queryRef": f"{cat_table}.{cat_col}"}],
                "Y": [{"queryRef": f"{val_table}.{val_measure}"}]
            },
            "prototypeQuery": {
                "Version": 2,
                "From": [
                    {"Name": "c", "Entity": cat_table, "Type": 0},
                    {"Name": "v", "Entity": val_table, "Type": 0}
                ],
                "Select": [
                    {
                        "Column": {
                            "Expression": {"SourceRef": {"Source": "c"}},
                            "Property": cat_col
                        },
                        "Name": f"{cat_table}.{cat_col}"
                    },
                    {
                        "Measure": {
                            "Expression": {"SourceRef": {"Source": "v"}},
                            "Property": val_measure
                        },
                        "Name": f"{val_table}.{val_measure}"
                    }
                ]
            }
        }
    }
    return {
        "x": x, "y": y, "z": 0, "width": w, "height": h,
        "config": json.dumps(cfg)
    }

def make_column_chart(x, y, w, h, cat_table, cat_col, val_table, val_measure):
    v_id = uid()
    cfg = {
        "name": v_id,
        "layouts": [{"id": 0, "position": {"x": x, "y": y, "z": 0, "width": w, "height": h, "tabOrder": 3}}],
        "singleVisual": {
            "visualType": "clusteredColumnChart",
            "projections": {
                "Category": [{"queryRef": f"{cat_table}.{cat_col}"}],
                "Y": [{"queryRef": f"{val_table}.{val_measure}"}]
            },
            "prototypeQuery": {
                "Version": 2,
                "From": [
                    {"Name": "c", "Entity": cat_table, "Type": 0},
                    {"Name": "v", "Entity": val_table, "Type": 0}
                ],
                "Select": [
                    {
                        "Column": {
                            "Expression": {"SourceRef": {"Source": "c"}},
                            "Property": cat_col
                        },
                        "Name": f"{cat_table}.{cat_col}"
                    },
                    {
                        "Measure": {
                            "Expression": {"SourceRef": {"Source": "v"}},
                            "Property": val_measure
                        },
                        "Name": f"{val_table}.{val_measure}"
                    }
                ]
            }
        }
    }
    return {
        "x": x, "y": y, "z": 0, "width": w, "height": h,
        "config": json.dumps(cfg)
    }

# Page 1 Visuals
p1_visuals = [
    # Top KPI Row (4 Cards)
    make_card(20, 20, 290, 110, "Fact_Observations", "Total Observations", "Total Observations"),
    make_card(330, 20, 290, 110, "Fact_Observations", "Valid Geo Records", "Valid Coordinates"),
    make_card(640, 20, 290, 110, "Fact_Observations", "Northern Hemisphere Share %", "North Hemisphere"),
    make_card(950, 20, 310, 110, "Fact_Observations", "Standard Net Share %", "Standard Net Share"),

    # Main Visuals Row 2
    make_bar_chart(20, 150, 600, 270, "Dim_Ocean", "OceanName", "Fact_Observations", "Total Observations"),
    make_pie_chart(640, 150, 620, 270, "Dim_MarineSetting", "MarineSetting", "Fact_Observations", "Total Observations"),

    # Main Visuals Row 3: Timeline & Method
    make_column_chart(20, 440, 750, 260, "Dim_Calendar", "Year", "Fact_Observations", "Total Observations"),
    make_bar_chart(790, 440, 470, 260, "Dim_SamplingMethod", "SamplingMethod", "Fact_Observations", "Total Observations"),
]

# Page 2 Visuals
p2_visuals = [
    # Top KPI Row
    make_card(20, 20, 380, 110, "Fact_Observations", "Total Observations", "Records"),
    make_card(430, 20, 380, 110, "Fact_Observations", "Zero-Inflation %", "Zero Inflation"),
    make_card(840, 20, 420, 110, "Fact_Observations", "Standard Net Share %", "Standard Mesh Share"),

    # Charts Row 2
    make_bar_chart(20, 150, 650, 550, "Dim_Organization", "OrganizationName", "Fact_Observations", "Total Observations"),
    make_column_chart(690, 150, 570, 550, "Fact_Observations", "ConcentrationClass", "Fact_Observations", "Total Observations"),
]

report_layout = {
    "config": json.dumps({"version": "5.37", "themeCollection": {}, "activeSectionIndex": 0, "linguisticSchemaSyncVersion": 2}),
    "layoutOptimization": 0,
    "sections": [
        {
            "name": "Section_Overview",
            "displayName": "1. Global Sampling Overview",
            "ordinal": 0,
            "width": 1280.0,
            "height": 720.0,
            "filters": "[]",
            "visualContainers": p1_visuals
        },
        {
            "name": "Section_Provenance",
            "displayName": "2. Provenance & Severity Analysis",
            "ordinal": 1,
            "width": 1280.0,
            "height": 720.0,
            "filters": "[]",
            "visualContainers": p2_visuals
        }
    ]
}

(REPORT_DIR / "report.json").write_text(json.dumps(report_layout, indent=2), encoding="utf-8")
print(f"Created complete native Power BI Project with visuals at: {PBIP_ROOT}")
