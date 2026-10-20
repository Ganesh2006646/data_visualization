import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Professional Color Palette
    C_TEAL = RGBColor(20, 116, 131)       # #147483 Accent Teal
    C_NAVY = RGBColor(24, 51, 79)         # #18334F Primary Navy
    C_DARK = RGBColor(30, 41, 59)         # #1E293B Text Dark Slate
    C_MUTED = RGBColor(100, 116, 139)     # #64748B Secondary Slate
    C_CARD_BG = RGBColor(238, 245, 248)   # #EEF5F8 Soft Ocean Light
    C_CARD_WHITE = RGBColor(255, 255, 255)# Pure White Card
    C_BORDER = RGBColor(203, 213, 225)    # #CBD5E1 Border Gray
    C_RED = RGBColor(192, 41, 43)         # #C0292B Warning Red
    C_GREEN = RGBColor(22, 160, 133)      # #16A085 Success Green
    C_AMBER = RGBColor(211, 84, 0)        # #D35400 Amber

    def add_chrome(slide, section_tag, title_text, slide_num):
        # Top banner line
        top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.12))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = C_TEAL
        top_bar.line.fill.background()

        # Section Pill / Tag
        if section_tag:
            tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.22), Inches(6.0), Inches(0.25))
            tf_tag = tag_box.text_frame
            tf_tag.word_wrap = True
            p_tag = tf_tag.paragraphs[0]
            p_tag.text = section_tag.upper()
            p_tag.font.name = "Calibri"
            p_tag.font.size = Pt(9.5)
            p_tag.font.bold = True
            p_tag.font.color.rgb = C_TEAL

        # Slide Title
        title_top = Inches(0.44) if section_tag else Inches(0.32)
        title_box = slide.shapes.add_textbox(Inches(0.8), title_top, Inches(11.7), Inches(0.55))
        tf = title_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.name = "Calibri"
        p.font.size = Pt(21)
        p.font.bold = True
        p.font.color.rgb = C_NAVY

        # Accent Rule
        rule = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.08), Inches(1.2), Inches(0.04))
        rule.fill.solid()
        rule.fill.fore_color.rgb = C_TEAL
        rule.line.fill.background()

        # Footer
        footer = slide.shapes.add_textbox(Inches(0.8), Inches(7.08), Inches(10.5), Inches(0.25))
        p_foot = footer.text_frame.paragraphs[0]
        p_foot.text = "GLOBAL MARINE MICROPLASTICS  ·  CSE355 CASE STUDY  ·  K. GANESH GIRIDHAR (CB.SC.U4CSE24519)"
        p_foot.font.name = "Calibri"
        p_foot.font.size = Pt(8.5)
        p_foot.font.color.rgb = C_MUTED

        # Slide Number
        num_box = slide.shapes.add_textbox(Inches(12.0), Inches(7.08), Inches(0.6), Inches(0.25))
        p_num = num_box.text_frame.paragraphs[0]
        p_num.alignment = PP_ALIGN.RIGHT
        p_num.text = str(slide_num)
        p_num.font.name = "Calibri"
        p_num.font.size = Pt(9)
        p_num.font.bold = True
        p_num.font.color.rgb = C_MUTED

    # -------------------------------------------------------------
    # SLIDE 1: TITLE SLIDE
    # -------------------------------------------------------------
    s1 = prs.slides.add_slide(blank_layout)
    top_bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.15))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = C_TEAL
    top_bar.line.fill.background()

    # Outer Container Card
    c1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(0.95), Inches(10.933), Inches(5.6))
    c1.fill.solid()
    c1.fill.fore_color.rgb = C_CARD_BG
    c1.line.color.rgb = C_BORDER
    c1.line.width = Pt(1.5)

    tb = s1.shapes.add_textbox(Inches(1.6), Inches(1.25), Inches(10.1), Inches(5.0))
    tf = tb.text_frame
    tf.word_wrap = True

    p0 = tf.paragraphs[0]
    p0.text = "CSE355 · DATA VISUALIZATION CASE STUDY"
    p0.font.name = "Calibri"
    p0.font.size = Pt(11)
    p0.font.bold = True
    p0.font.color.rgb = C_TEAL
    p0.space_after = Pt(12)

    p1 = tf.add_paragraph()
    p1.text = "Global Marine Microplastic Pollution"
    p1.font.name = "Calibri"
    p1.font.size = Pt(32)
    p1.font.bold = True
    p1.font.color.rgb = C_NAVY

    p2 = tf.add_paragraph()
    p2.text = "An Ethical, Bias-Aware Visualization Framework for Hotspot Detection"
    p2.font.name = "Calibri"
    p2.font.size = Pt(17)
    p2.font.color.rgb = C_TEAL
    p2.space_after = Pt(24)

    p3 = tf.add_paragraph()
    p3.text = "Student Author & Submission Information:"
    p3.font.name = "Calibri"
    p3.font.size = Pt(12)
    p3.font.bold = True
    p3.font.color.rgb = C_NAVY
    p3.space_after = Pt(6)

    details = [
        ("Student Name", "K. Ganesh Giridhar"),
        ("Register Number", "CB.SC.U4CSE24519"),
        ("Course & Department", "CSE355 – Data Visualization & Analytics | Dept. of Computer Science & Engineering"),
        ("Institution", "School of Computing, Amrita Vishwa Vidyapeetham"),
        ("Dataset Used", "NOAA NCEI Global Marine Microplastics Database (29,076 records, 1972–2026)")
    ]
    for label, val in details:
        pd = tf.add_paragraph()
        pd.text = f"•  {label}: {val}"
        pd.font.name = "Calibri"
        pd.font.size = Pt(11)
        pd.font.color.rgb = C_DARK
        pd.space_after = Pt(3)

    foot1 = s1.shapes.add_textbox(Inches(1.2), Inches(6.8), Inches(10.933), Inches(0.35))
    p_f1 = foot1.text_frame.paragraphs[0]
    p_f1.text = "PHASE 1 & FINAL EVALUATION REVIEW  ·  AMRITA VISHWA VIDYAPEETHAM  ·  OCTOBER 2026"
    p_f1.font.name = "Calibri"
    p_f1.font.size = Pt(9)
    p_f1.font.color.rgb = C_MUTED

    # -------------------------------------------------------------
    # SLIDE 2: PROBLEM STATEMENT & OBJECTIVES
    # -------------------------------------------------------------
    s2 = prs.slides.add_slide(blank_layout)
    add_chrome(s2, "Section 1 · 5 Marks", "Problem Statement and Analytical Objectives", 2)

    col_w = Inches(3.7)
    col_h = Inches(5.6)
    y_pos = Inches(1.25)

    # Card 1: Context & Problem
    c2_1 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), y_pos, col_w, col_h)
    c2_1.fill.solid()
    c2_1.fill.fore_color.rgb = C_CARD_BG
    c2_1.line.color.rgb = C_BORDER
    tb2_1 = s2.shapes.add_textbox(Inches(0.95), y_pos + Inches(0.12), col_w - Inches(0.3), col_h - Inches(0.24))
    tf2_1 = tb2_1.text_frame
    tf2_1.word_wrap = True

    p = tf2_1.paragraphs[0]
    p.text = "PROBLEM CONTEXT"
    p.font.name = "Calibri"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = C_TEAL
    p.space_after = Pt(6)

    p = tf2_1.add_paragraph()
    p.text = "• >11 million metric tonnes of plastics enter global oceans every year, breaking into microplastics (<5 mm).\n• Particles adsorb toxic pollutants and contaminate marine food webs.\n• Critical Issue: Data is collected across 4 different settings with 3 incompatible measurement units."
    p.font.name = "Calibri"
    p.font.size = Pt(10)
    p.font.color.rgb = C_DARK
    p.space_after = Pt(12)

    p = tf2_1.add_paragraph()
    p.text = "PROBLEM STATEMENT"
    p.font.name = "Calibri"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p.space_after = Pt(4)

    p = tf2_1.add_paragraph()
    p.text = "\"How can 29,000+ global microplastic records across 4 marine settings and 3 incompatible units be visualized without confusing research effort with true pollution hotspots?\""
    p.font.name = "Calibri"
    p.font.size = Pt(10)
    p.font.italic = True
    p.font.color.rgb = C_DARK

    # Card 2: Objectives
    c2_2 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.8), y_pos, col_w, col_h)
    c2_2.fill.solid()
    c2_2.fill.fore_color.rgb = C_CARD_BG
    c2_2.line.color.rgb = C_BORDER
    tb2_2 = s2.shapes.add_textbox(Inches(4.95), y_pos + Inches(0.12), col_w - Inches(0.3), col_h - Inches(0.24))
    tf2_2 = tb2_2.text_frame
    tf2_2.word_wrap = True

    p = tf2_2.paragraphs[0]
    p.text = "ANALYTICAL OBJECTIVES"
    p.font.name = "Calibri"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = C_TEAL
    p.space_after = Pt(6)

    objs = [
        ("O1. Map Global Coverage", "Plot 100% geo-valid records to expose data deserts in Southern/Indian oceans."),
        ("O2. Effort-Normalized Hotspots", "Separate research vessel route frequency from true contamination density."),
        ("O3. Decompose 50-Year Trends", "Deconstruct 1972–2026 data to separate sampling growth from pollution rise."),
        ("O4. Compare Ocean Basins", "Quantify median and IQR concentration strictly within matched units."),
        ("O5. Assess Mesh Aperture Bias", "Measure the 4x detection gap between fine filters (<100 um) and standard nets (333 um).")
    ]
    for title, desc in objs:
        p = tf2_2.add_paragraph()
        p.text = f"• {title}: {desc}"
        p.font.name = "Calibri"
        p.font.size = Pt(9.5)
        p.font.color.rgb = C_DARK
        p.space_after = Pt(4)

    # Card 3: Why it Matters
    c2_3 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.8), y_pos, col_w, col_h)
    c2_3.fill.solid()
    c2_3.fill.fore_color.rgb = C_CARD_BG
    c2_3.line.color.rgb = C_BORDER
    tb2_3 = s2.shapes.add_textbox(Inches(8.95), y_pos + Inches(0.12), col_w - Inches(0.3), col_h - Inches(0.24))
    tf2_3 = tb2_3.text_frame
    tf2_3.word_wrap = True

    p = tf2_3.paragraphs[0]
    p.text = "WHY THIS MATTERS"
    p.font.name = "Calibri"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = C_TEAL
    p.space_after = Pt(6)

    p = tf2_3.add_paragraph()
    p.text = "• Stop Wasting Resources:\nPrevents deploying cleanup operations to heavily surveyed coasts while severe pelagic gyre accumulation zones remain ignored.\n\n• Ethical Data Communication:\nShows how chart manipulation (truncated axes, mixing units) creates false alarms and misinforms the public.\n\n• Policy Support:\nProvides sound empirical evidence for the UN Global Plastics Treaty (INC-5) and IMO plastic pellet rules."
    p.font.name = "Calibri"
    p.font.size = Pt(10)
    p.font.color.rgb = C_DARK

    # -------------------------------------------------------------
    # SLIDE 3: DATASET DESCRIPTION
    # -------------------------------------------------------------
    s3 = prs.slides.add_slide(blank_layout)
    add_chrome(s3, "Section 1 · 5 Marks", "Dataset Description and Structural Profile", 3)

    c3_top = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.25), Inches(11.7), Inches(3.9))
    c3_top.fill.solid()
    c3_top.fill.fore_color.rgb = C_CARD_BG
    c3_top.line.color.rgb = C_BORDER

    tb3 = s3.shapes.add_textbox(Inches(1.0), Inches(1.35), Inches(11.3), Inches(3.7))
    tf3 = tb3.text_frame
    tf3.word_wrap = True

    sections_s3 = [
        ("DATASET SOURCE", "NOAA National Centers for Environmental Information (NCEI) Global Marine Microplastics Database (Parent Collection DOI: 10.25921/d1bs-3m40; Nurdle Patrol Accession: 0259486)."),
        ("DOMAIN & COVERAGE", "Global Marine Environmental Pollution. Spans all 5 major oceans (Atlantic, Pacific, Indian, Arctic, Southern) from latitude -54° to +81°."),
        ("TEMPORAL SCOPE", "54-year continuous baseline from April 20, 1972 through April 28, 2026. Blends professional research voyages and standardized citizen science."),
        ("KEY ATTRIBUTES & TYPES", "Sample Date (DateTime), Lat/Lon (Decimal degrees), Ocean (Categorical), Marine Setting (Categorical: 4 levels), Sampling Method (Categorical), Mesh Size (Numeric mm), Measurement Value (Numeric), Unit (Categorical: 3 distinct units), Concentration Class (Ordinal: Very Low to Very High)."),
        ("DATA QUALITY CONCERNS", "1) Incompatible Units (pieces/m3, pieces/10 mins, pieces kg-1 d.w.) tied to settings. 2) Severe Spatial Sampling Bias (94.2% in Northern Hemisphere). 3) Heavy Right Skew spanning 6 orders of magnitude.")
    ]
    for i, (hdr, body) in enumerate(sections_s3):
        p = tf3.paragraphs[0] if i == 0 else tf3.add_paragraph()
        p.text = f"{hdr}: "
        p.font.name = "Calibri"
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = C_NAVY
        run = p.add_run()
        run.text = body
        run.font.bold = False
        run.font.color.rgb = C_DARK
        p.space_after = Pt(4)

    metrics_s3 = [
        ("29,076", "TOTAL OBSERVATIONS", "100% Valid Coordinates"),
        ("35", "ORIGINAL ATTRIBUTES", "Full Metadata Context"),
        ("4 SETTINGS", "MARINE COMPARTMENTS", "Water, Beach, Sediment, Nurdles"),
        ("54 YEARS", "TEMPORAL RANGE", "1972 through 2026")
    ]
    card_w = Inches(2.75)
    for idx, (m_val, m_lbl, m_sub) in enumerate(metrics_s3):
        x = Inches(0.8) + idx * Inches(2.98)
        card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(5.35), card_w, Inches(1.4))
        card.fill.solid()
        card.fill.fore_color.rgb = C_TEAL if idx == 0 else C_CARD_BG
        card.line.color.rgb = C_TEAL if idx == 0 else C_BORDER

        tb_m = s3.shapes.add_textbox(x, Inches(5.42), card_w, Inches(1.2))
        tf_m = tb_m.text_frame
        tf_m.word_wrap = True

        p = tf_m.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.text = m_val
        p.font.name = "Calibri"
        p.font.size = Pt(20)
        p.font.bold = True
        p.font.color.rgb = C_CARD_WHITE if idx == 0 else C_NAVY

        p2 = tf_m.add_paragraph()
        p2.alignment = PP_ALIGN.CENTER
        p2.text = m_lbl
        p2.font.name = "Calibri"
        p2.font.size = Pt(9.5)
        p2.font.bold = True
        p2.font.color.rgb = C_CARD_WHITE if idx == 0 else C_TEAL

        p3 = tf_m.add_paragraph()
        p3.alignment = PP_ALIGN.CENTER
        p3.text = m_sub
        p3.font.name = "Calibri"
        p3.font.size = Pt(8.5)
        p3.font.color.rgb = C_CARD_WHITE if idx == 0 else C_MUTED

    # -------------------------------------------------------------
    # SLIDE 4: DATA CLEANING & PREPROCESSING
    # -------------------------------------------------------------
    s4 = prs.slides.add_slide(blank_layout)
    add_chrome(s4, "Section 1 · 5 Marks", "Data Cleaning and Preprocessing Protocols", 4)

    steps_s4 = [
        ("1. COORDINATE VALIDATION",
         "• Checked all latitudes in [-90, +90] and longitudes in [-180, +180].\n• 29,076 of 29,076 records (100.0%) passed validation with zero missing coordinates.\n• Reconciled geographic coordinates with pre-projected Web Mercator values."),
        ("2. DATE STANDARDIZATION",
         "• Converted string timestamps into ISO-8601 datetimes.\n• Derived temporal features: Year, Month, Decade, and pre/post-2010 sampling eras.\n• Preserved historical records dating back to 1972."),
        ("3. MISSING VALUE STRATEGY",
         "• Missing-Not-At-Random (MNAR): fields like volunteer count and sample depth are naturally empty for open-ocean net tows.\n• Retained as explicit 'Not Recorded' category rather than using false imputation."),
        ("4. STRICT UNIT SEGREGATION",
         "• CRITICAL RULE: Measurements are strictly separated by Marine Setting:\n  - Ocean Water: pieces/m³ (16,988 records)\n  - Nurdle Patrol: pieces/10 mins (10,615 records)\n  - Beach: pieces/m³ sand (893 records)\n  - Sediment: pieces kg⁻¹ d.w. (580 records)\n• Zero cross-unit numeric pooling."),
        ("5. SKEWNESS & LOG-TRANSFORM",
         "• Microplastic concentrations span 6 orders of magnitude (0.001 to >10,000).\n• Created log10(conc + 1) transformed fields for statistical testing while preserving raw metrics for reporting."),
        ("6. 2°×2° SPATIAL GRID FEATURE",
         "• Created 2°×2° spatial grid bins to calculate observation count per cell.\n• Enables effort-normalization: dividing total particles by sample density to find true hotspots.")
    ]

    card_w4 = Inches(3.7)
    card_h4 = Inches(2.65)
    for idx, (title, text) in enumerate(steps_s4):
        col = idx % 3
        row = idx // 3
        x = Inches(0.8) + col * Inches(3.98)
        y = Inches(1.25) + row * Inches(2.85)

        card = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, card_w4, card_h4)
        card.fill.solid()
        card.fill.fore_color.rgb = C_CARD_BG
        card.line.color.rgb = C_BORDER

        tb = s4.shapes.add_textbox(x + Inches(0.12), y + Inches(0.08), card_w4 - Inches(0.24), card_h4 - Inches(0.16))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = title
        p.font.name = "Calibri"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = C_TEAL
        p.space_after = Pt(4)

        for line in text.split("\n"):
            p = tf.add_paragraph()
            p.text = line
            p.font.name = "Calibri"
            p.font.size = Pt(9.5)
            p.font.color.rgb = C_DARK
            p.space_after = Pt(2)

    # -------------------------------------------------------------
    # SLIDE 5: TOOLS & VISUALIZATION APPROACH
    # -------------------------------------------------------------
    s5 = prs.slides.add_slide(blank_layout)
    add_chrome(s5, "Section 2 · 18 Marks", "Tools and Visualization Approach", 5)

    tools_data = [
        ("TOOL 1: PYTHON VISUALIZATION", "Matplotlib & Seaborn",
         "WHY SELECTED:\n• Full coordinate control for geographic scatter projection.\n• Non-parametric distribution modeling (boxplots, violins, LOESS regression).\n• Enables forensic side-by-side ethical chart redesign.\n\nWHAT IT PRODUCES:\n• V1 Global Map & V2 Effort-Aware Grid\n• V3 50-Year Trajectory & V4 Basin Distributions\n• V5 Setting Profile, V6/V7 Gear & Mesh Biases\n• V8 Severity Matrix & V9 Ethical Redesign"),
        ("TOOL 2: POWER BI DESKTOP", "Enterprise Business Intelligence (.pbip)",
         "WHY SELECTED:\n• Interactive delivery for decision-makers with zero code execution.\n• Certified Star Schema data model (1 Fact table, 6 Dimension tables).\n• 15+ custom DAX measures enforcing unit isolation & dynamic filtering.\n\nWHAT IT PRODUCES:\n• Page 1: Executive KPI Overview & Spatial Map\n• Page 2: Ocean Basin & Setting Deep-Dive\n• Page 3: Provenance & Ethical Audit Visualizer\n• Interactive cross-filtering slicers & drill-down"),
        ("TOOL 3: PLOTLY WEB ENGINE", "WebGL & D3.js Standalone HTML",
         "WHY SELECTED:\n• Zero-dependency web viewing in any standard browser (Chrome, Edge, Safari).\n• Hardware-accelerated rendering of all 29,076 coordinates.\n• Dynamic hover tooltips and interactive zooming for rapid inspection.\n\nWHAT IT PRODUCES:\n• Standalone single-file HTML dashboard\n• Cross-linked scatter and bar views\n• Dynamic multi-select marine setting filters")
    ]

    card_w5 = Inches(3.7)
    card_h5 = Inches(5.5)
    for idx, (title, sub, body) in enumerate(tools_data):
        x = Inches(0.8) + idx * Inches(3.98)
        y = Inches(1.25)
        card = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, card_w5, card_h5)
        card.fill.solid()
        card.fill.fore_color.rgb = C_CARD_BG
        card.line.color.rgb = C_BORDER

        tb = s5.shapes.add_textbox(x + Inches(0.15), y + Inches(0.12), card_w5 - Inches(0.3), card_h5 - Inches(0.24))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = title
        p.font.name = "Calibri"
        p.font.size = Pt(11.5)
        p.font.bold = True
        p.font.color.rgb = C_NAVY

        p_sub = tf.add_paragraph()
        p_sub.text = sub
        p_sub.font.name = "Calibri"
        p_sub.font.size = Pt(9.5)
        p_sub.font.bold = True
        p_sub.font.color.rgb = C_TEAL
        p_sub.space_after = Pt(8)

        for line in body.split("\n"):
            p = tf.add_paragraph()
            p.text = line
            p.font.name = "Calibri"
            p.font.size = Pt(9.5)
            p.font.color.rgb = C_DARK if not line.startswith("•") else C_NAVY
            if line.startswith("WHY") or line.startswith("WHAT"):
                p.font.bold = True
                p.font.color.rgb = C_TEAL
            p.space_after = Pt(2)

    # -------------------------------------------------------------
    # SLIDE 6: EDA – I (V1 & V2)
    # -------------------------------------------------------------
    s6 = prs.slides.add_slide(blank_layout)
    add_chrome(s6, "Section 2 · 18 Marks", "Exploratory Data Analysis – I: Spatial Coverage and Sampling Effort", 6)

    card_w6 = Inches(5.7)
    card_h6 = Inches(5.6)

    # Left Column: V1
    c6_l = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.25), card_w6, card_h6)
    c6_l.fill.solid()
    c6_l.fill.fore_color.rgb = C_CARD_WHITE
    c6_l.line.color.rgb = C_BORDER

    tb6_l = s6.shapes.add_textbox(Inches(0.95), Inches(1.35), card_w6 - Inches(0.3), Inches(1.1))
    tf6_l = tb6_l.text_frame
    tf6_l.word_wrap = True
    p = tf6_l.paragraphs[0]
    p.text = "V1: GLOBAL SAMPLING MAP & GEOGRAPHIC BIAS"
    p.font.name = "Calibri"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p = tf6_l.add_paragraph()
    p.text = "Description: Global scatter plot of all 29,076 sampling locations color-coded by marine setting.\nInsight: 94.2% of records cluster in the Northern Hemisphere (North Atlantic & Gulf of Mexico). Indian Ocean (2.7%) and Southern Ocean (0.1%) are critical data blindspots."
    p.font.name = "Calibri"
    p.font.size = Pt(9.5)
    p.font.color.rgb = C_DARK

    img_v1_path = "dashboard/extracted_visuals/cell_6_out_0.png"
    if os.path.exists(img_v1_path):
        s6.shapes.add_picture(img_v1_path, Inches(0.95), Inches(2.55), width=Inches(5.4))

    # Takeaway Pill V1
    t1_box = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.95), Inches(5.85), Inches(5.4), Inches(0.85))
    t1_box.fill.solid()
    t1_box.fill.fore_color.rgb = C_CARD_BG
    t1_box.line.color.rgb = C_TEAL
    p_t1 = t1_box.text_frame.paragraphs[0]
    p_t1.text = "Key Takeaway: Observation density reflects research cruise routes, not true ecological pollution levels."
    p_t1.font.name = "Calibri"
    p_t1.font.size = Pt(9)
    p_t1.font.bold = True
    p_t1.font.color.rgb = C_TEAL

    # Right Column: V2
    c6_r = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.25), card_w6, card_h6)
    c6_r.fill.solid()
    c6_r.fill.fore_color.rgb = C_CARD_WHITE
    c6_r.line.color.rgb = C_BORDER

    tb6_r = s6.shapes.add_textbox(Inches(6.95), Inches(1.35), card_w6 - Inches(0.3), Inches(1.1))
    tf6_r = tb6_r.text_frame
    tf6_r.word_wrap = True
    p = tf6_r.paragraphs[0]
    p.text = "V2: HOTSPOT ANALYSIS: EFFORT VS. POLLUTION"
    p.font.name = "Calibri"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p = tf6_r.add_paragraph()
    p.text = "Description: 2°×2° binned spatial grid separating sample count from median concentration.\nInsight: Normalizing effort reveals that coastal Florida and English Channel are heavily sampled, not heavily polluted. True hotspots lie in pelagic gyres (e.g. North Pacific) with extreme concentrations."
    p.font.name = "Calibri"
    p.font.size = Pt(9.5)
    p.font.color.rgb = C_DARK

    img_v2_path = "dashboard/extracted_visuals/cell_8_out_0.png"
    if os.path.exists(img_v2_path):
        s6.shapes.add_picture(img_v2_path, Inches(6.95), Inches(2.65), width=Inches(5.4))

    # Takeaway Pill V2
    t2_box = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.95), Inches(5.85), Inches(5.4), Inches(0.85))
    t2_box.fill.solid()
    t2_box.fill.fore_color.rgb = C_CARD_BG
    t2_box.line.color.rgb = C_TEAL
    p_t2 = t2_box.text_frame.paragraphs[0]
    p_t2.text = "Key Takeaway: Effort normalization prevents mistaking well-studied coasts for pollution hotspots."
    p_t2.font.name = "Calibri"
    p_t2.font.size = Pt(9)
    p_t2.font.bold = True
    p_t2.font.color.rgb = C_TEAL

    # -------------------------------------------------------------
    # SLIDE 7: EDA – II (V3 & V4)
    # -------------------------------------------------------------
    s7 = prs.slides.add_slide(blank_layout)
    add_chrome(s7, "Section 2 · 18 Marks", "Exploratory Data Analysis – II: Temporal Trends and Basin Distributions", 7)

    # Left Column: V3
    c7_l = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.25), card_w6, card_h6)
    c7_l.fill.solid()
    c7_l.fill.fore_color.rgb = C_CARD_WHITE
    c7_l.line.color.rgb = C_BORDER

    tb7_l = s7.shapes.add_textbox(Inches(0.95), Inches(1.35), card_w6 - Inches(0.3), Inches(1.1))
    tf7_l = tb7_l.text_frame
    tf7_l.word_wrap = True
    p = tf7_l.paragraphs[0]
    p.text = "V3: 50-YEAR MONITORING TRAJECTORY (1972–2026)"
    p.font.name = "Calibri"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p = tf7_l.add_paragraph()
    p.text = "Description: Dual-axis time series of annual observation count vs. median ocean water concentration.\nInsight: Record counts explode after 2010 due to citizen science (Nurdle Patrol) and research funding. Decoupling count from concentration shows baseline contamination remained steady, not an abrupt overnight surge."
    p.font.name = "Calibri"
    p.font.size = Pt(9.5)
    p.font.color.rgb = C_DARK

    img_v3_path = "dashboard/extracted_visuals/cell_10_out_0.png"
    if os.path.exists(img_v3_path):
        s7.shapes.add_picture(img_v3_path, Inches(0.95), Inches(2.55), width=Inches(4.5))

    t3_box = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.95), Inches(5.95), Inches(5.4), Inches(0.75))
    t3_box.fill.solid()
    t3_box.fill.fore_color.rgb = C_CARD_BG
    t3_box.line.color.rgb = C_TEAL
    p_t3 = t3_box.text_frame.paragraphs[0]
    p_t3.text = "Key Takeaway: Post-2010 surge reflects research expansion and citizen science, not sudden pollution."
    p_t3.font.name = "Calibri"
    p_t3.font.size = Pt(9)
    p_t3.font.bold = True
    p_t3.font.color.rgb = C_TEAL

    # Right Column: V4
    c7_r = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.25), card_w6, card_h6)
    c7_r.fill.solid()
    c7_r.fill.fore_color.rgb = C_CARD_WHITE
    c7_r.line.color.rgb = C_BORDER

    tb7_r = s7.shapes.add_textbox(Inches(6.95), Inches(1.35), card_w6 - Inches(0.3), Inches(1.1))
    tf7_r = tb7_r.text_frame
    tf7_r.word_wrap = True
    p = tf7_r.paragraphs[0]
    p.text = "V4: CONCENTRATION ACROSS 5 OCEAN BASINS"
    p.font.name = "Calibri"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p = tf7_r.add_paragraph()
    p.text = "Description: Log10-scale box and violin plots comparing surface water microplastic levels across ocean basins.\nInsight: Kruskal-Wallis test (H = 142.8, p < 0.001) confirms significant inter-basin differences. Pacific Ocean exhibits the highest median concentration (1.84 pcs/m³); Mediterranean shows extreme upper-tail outliers."
    p.font.name = "Calibri"
    p.font.size = Pt(9.5)
    p.font.color.rgb = C_DARK

    img_v4_path = "dashboard/extracted_visuals/cell_12_out_0.png"
    if os.path.exists(img_v4_path):
        s7.shapes.add_picture(img_v4_path, Inches(6.95), Inches(2.75), width=Inches(5.4))

    t4_box = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.95), Inches(5.95), Inches(5.4), Inches(0.75))
    t4_box.fill.solid()
    t4_box.fill.fore_color.rgb = C_CARD_BG
    t4_box.line.color.rgb = C_TEAL
    p_t4 = t4_box.text_frame.paragraphs[0]
    p_t4.text = "Key Takeaway: Pacific gyre carries 4.4x higher median concentration than the oversampled Atlantic."
    p_t4.font.name = "Calibri"
    p_t4.font.size = Pt(9)
    p_t4.font.bold = True
    p_t4.font.color.rgb = C_TEAL

    # -------------------------------------------------------------
    # SLIDE 8: EDA – III (V5, V6, V7 & V8)
    # -------------------------------------------------------------
    s8 = prs.slides.add_slide(blank_layout)
    add_chrome(s8, "Section 2 · 18 Marks", "Exploratory Data Analysis – III: Settings, Gear & Severity Breakdown", 8)

    card_w8 = Inches(5.7)
    card_h8 = Inches(2.7)

    quads = [
        ("V5: ALL 4 MARINE SETTINGS COMPARED",
         "Distribution across Water, Beach, Sediment, and Nurdles.",
         "Beach sand median (1,280 pcs/m³) is orders of magnitude higher than surface ocean water (0.01 pcs/m³). Proves units must never be pooled.",
         "dashboard/extracted_visuals/cell_14_out_0.png",
         Inches(0.8), Inches(1.25)),

        ("V6: SAMPLING METHOD BY BASIN MATRIX",
         "Cross-tabulation of sampling gear across ocean basins.",
         "Severe method-geography confounding: Manta nets dominate open Atlantic cruises, whereas nearshore grab samples dominate enclosed coastal seas.",
         "dashboard/extracted_visuals/cell_16_out_0.png",
         Inches(6.8), Inches(1.25)),

        ("V7: MESH SIZE APERTURE BIAS (0.333 mm)",
         "Microplastic capture concentration vs. net mesh aperture size.",
         "Nets finer than 100 um detect over 4x higher microplastic concentrations (especially microfibers) than standard 333 um manta nets, proving systematic undercounting.",
         "dashboard/extracted_visuals/cell_17_out_0.png",
         Inches(0.8), Inches(4.15)),

        ("V8: SEVERITY BREAKDOWN ACROSS BASINS",
         "Proportional 100% stacked bar chart of pollution severity categories.",
         "High & Very High severity classes comprise 17.7% of all global records. Pacific gyres and Mediterranean Sea show the highest severe contamination proportions.",
         "dashboard/extracted_visuals/cell_19_out_0.png",
         Inches(6.8), Inches(4.15))
    ]

    for title, desc, insight, img_p, x_q, y_q in quads:
        card = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x_q, y_q, card_w8, card_h8)
        card.fill.solid()
        card.fill.fore_color.rgb = C_CARD_WHITE
        card.line.color.rgb = C_BORDER

        tb_q = s8.shapes.add_textbox(x_q + Inches(0.12), y_q + Inches(0.08), Inches(2.8), Inches(2.5))
        tf_q = tb_q.text_frame
        tf_q.word_wrap = True

        p = tf_q.paragraphs[0]
        p.text = title
        p.font.name = "Calibri"
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = C_NAVY
        p.space_after = Pt(2)

        p = tf_q.add_paragraph()
        p.text = f"Desc: {desc}"
        p.font.name = "Calibri"
        p.font.size = Pt(8.5)
        p.font.color.rgb = C_MUTED
        p.space_after = Pt(3)

        p = tf_q.add_paragraph()
        p.text = f"Insight: {insight}"
        p.font.name = "Calibri"
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = C_DARK

        if os.path.exists(img_p):
            s8.shapes.add_picture(img_p, x_q + Inches(2.95), y_q + Inches(0.15), width=Inches(2.65))

    # -------------------------------------------------------------
    # SLIDE 9: INTERACTIVE DASHBOARD – POWER BI (V10)
    # -------------------------------------------------------------
    s9 = prs.slides.add_slide(blank_layout)
    add_chrome(s9, "Section 2 · 18 Marks", "Interactive Power BI Dashboard: Architecture and Layout (V10)", 9)

    img_pbi1 = "dashboard/extracted_visuals/dashboard_pbi_page1.png"
    if os.path.exists(img_pbi1):
        s9.shapes.add_picture(img_pbi1, Inches(0.8), Inches(1.25), width=Inches(7.8))

    # Bottom 3 Feature Pills under the image
    pbi_highlights = [
        ("Star Schema Architecture", "1 Fact Table (29K rows) linked to 6 Dimensions"),
        ("15+ Custom DAX Measures", "Enforces unit isolation & geometric means"),
        ("Dynamic Slicers", "Multi-select filtering by Setting & Monitoring Era")
    ]
    card_w9_b = Inches(2.5)
    for idx, (h_title, h_sub) in enumerate(pbi_highlights):
        x = Inches(0.8) + idx * Inches(2.65)
        y = Inches(5.35)
        card = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, card_w9_b, Inches(1.4))
        card.fill.solid()
        card.fill.fore_color.rgb = C_CARD_BG
        card.line.color.rgb = C_BORDER

        tb = s9.shapes.add_textbox(x, y + Inches(0.15), card_w9_b, Inches(1.1))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.text = h_title
        p.font.name = "Calibri"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = C_NAVY

        p2 = tf.add_paragraph()
        p2.alignment = PP_ALIGN.CENTER
        p2.text = h_sub
        p2.font.name = "Calibri"
        p2.font.size = Pt(9)
        p2.font.color.rgb = C_TEAL

    # Right side explanation card
    c9_r = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.8), Inches(1.25), Inches(3.7), Inches(5.5))
    c9_r.fill.solid()
    c9_r.fill.fore_color.rgb = C_CARD_BG
    c9_r.line.color.rgb = C_BORDER

    tb9 = s9.shapes.add_textbox(Inches(8.95), Inches(1.35), Inches(3.4), Inches(5.3))
    tf9 = tb9.text_frame
    tf9.word_wrap = True

    p = tf9.paragraphs[0]
    p.text = "EXECUTIVE DASHBOARD SPECS"
    p.font.name = "Calibri"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p.space_after = Pt(6)

    pbi_points = [
        ("Executive KPI Banner", "Instant visibility on Total Samples (29K), Northern Bias (94.2%), Southern Blindspot (0.1%), and Coordinate Integrity (100%)."),
        ("Central Visuals", "• V1: Geographic coordinate plot\n• V2: Basin effort vs median concentration\n• V3: 50-year monitoring trajectory"),
        ("Dynamic Slicers", "Multi-select filtering by Marine Setting (Water, Beach, Sediment, Nurdles) and Monitoring Era (1970s–2020s)."),
        ("Cross-Filtering Engine", "Clicking an ocean basin cross-filters all cards and charts instantly, preserving unit isolation via custom DAX measures."),
        ("Stakeholder Value", "Translates 29,000 raw points into an intuitive decision tool for policy makers.")
    ]
    for lbl, desc in pbi_points:
        p = tf9.add_paragraph()
        p.text = f"• {lbl}: "
        p.font.name = "Calibri"
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = C_TEAL
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = C_DARK
        p.space_after = Pt(4)

    # -------------------------------------------------------------
    # SLIDE 10: DASHBOARD INSIGHTS & STORYTELLING
    # -------------------------------------------------------------
    s10 = prs.slides.add_slide(blank_layout)
    add_chrome(s10, "Section 2 · 18 Marks", "Dashboard Insights and Data Storytelling (What? So What? Now What?)", 10)

    img_pbi2 = "dashboard/extracted_visuals/dashboard_pbi_page2.png"
    if os.path.exists(img_pbi2):
        s10.shapes.add_picture(img_pbi2, Inches(0.8), Inches(1.25), width=Inches(7.2))

    # Bottom 2 Interactive Slicer Examples under the image
    slicer_examples = [
        ("Slicer Interaction: Marine Setting = Ocean Water",
         "Instantly isolates the 16,988 surface water tows. All visuals report strictly in pieces/m³, eliminating cross-unit mixing and revealing genuine open-sea baseline concentrations."),
        ("Slicer Interaction: Ocean Basin = Pacific Ocean",
         "Cross-filters all dashboard cards to Pacific data. Proves that despite having fewer samples than the Atlantic, the Pacific carries 4.4x higher median pollution (1.84 pcs/m³).")
    ]
    card_w10_b = Inches(3.5)
    for idx, (s_title, s_desc) in enumerate(slicer_examples):
        x = Inches(0.8) + idx * Inches(3.7)
        y = Inches(5.1)
        card = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, card_w10_b, Inches(1.7))
        card.fill.solid()
        card.fill.fore_color.rgb = C_CARD_BG
        card.line.color.rgb = C_BORDER

        tb = s10.shapes.add_textbox(x + Inches(0.1), y + Inches(0.1), card_w10_b - Inches(0.2), Inches(1.5))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = s_title
        p.font.name = "Calibri"
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = C_NAVY
        p.space_after = Pt(3)

        p = tf.add_paragraph()
        p.text = s_desc
        p.font.name = "Calibri"
        p.font.size = Pt(9)
        p.font.color.rgb = C_DARK

    # Right side: What? So What? Now What?
    c10_r = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.2), Inches(1.25), Inches(4.3), Inches(5.55))
    c10_r.fill.solid()
    c10_r.fill.fore_color.rgb = C_CARD_BG
    c10_r.line.color.rgb = C_BORDER

    tb10 = s10.shapes.add_textbox(Inches(8.35), Inches(1.35), Inches(4.0), Inches(5.3))
    tf10 = tb10.text_frame
    tf10.word_wrap = True

    p = tf10.paragraphs[0]
    p.text = "DATA STORYTELLING FRAMEWORK"
    p.font.name = "Calibri"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p.space_after = Pt(6)

    story_points = [
        ("WHAT? (The Observed Pattern)",
         "94.2% of global records are concentrated in North America and Western Europe. Pelagic ocean water has a 29.2% zero-rate, while Beach sand has 23.5% zeros with extreme local spikes (>40,000 pcs/m³)."),
        ("SO WHAT? (The Ecological Meaning)",
         "High sample count DOES NOT equal high pollution. Atlantic appears most polluted due to repeated sampling, but Pacific gyres hold far higher median concentrations (1.84 pcs/m³ vs 0.42 pcs/m³)."),
        ("NOW WHAT? (Decision & Action)",
         "1) Stop treating sample count as a proxy for pollution.\n2) Target high-seas cleanup fleets to the Pacific gyre.\n3) Enforce mandatory reporting for industrial nurdle spills in coastal zones.")
    ]
    for lbl, desc in story_points:
        p = tf10.add_paragraph()
        p.text = f"{lbl}\n"
        p.font.name = "Calibri"
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = C_TEAL
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = C_DARK
        p.space_after = Pt(6)

    # -------------------------------------------------------------
    # SLIDE 11: MISLEADING VS ETHICAL REDESIGN (V9)
    # -------------------------------------------------------------
    s11 = prs.slides.add_slide(blank_layout)
    add_chrome(s11, "Section 2 · 18 Marks", "Forensic Data Ethics: Misleading vs. Ethical Redesign (V9)", 11)

    card_w11 = Inches(5.7)
    card_h11 = Inches(5.6)

    # Left: Misleading
    c11_l = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.25), card_w11, card_h11)
    c11_l.fill.solid()
    c11_l.fill.fore_color.rgb = C_CARD_WHITE
    c11_l.line.color.rgb = C_RED
    c11_l.line.width = Pt(1.5)

    tb11_l = s11.shapes.add_textbox(Inches(0.95), Inches(1.35), card_w11 - Inches(0.3), Inches(1.8))
    tf11_l = tb11_l.text_frame
    tf11_l.word_wrap = True
    p = tf11_l.paragraphs[0]
    p.text = "INTENTIONALLY MISLEADING VISUALIZATION"
    p.font.name = "Calibri"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_RED

    p = tf11_l.add_paragraph()
    p.text = "• Distortion: Truncated Y-axis baseline starting at 0.200 instead of 0.0.\n• Visual Exaggeration: Makes a modest ~10% change look like an alarming 800% pollution surge!\n• Concealed Information: Hides sample sizes (n), hides wide dispersion, and conceals unit boundaries.\n• Psychological Effect: Induces unwarranted public panic and distorts environmental priorities."
    p.font.name = "Calibri"
    p.font.size = Pt(9.5)
    p.font.color.rgb = C_DARK

    img_misleading = "dashboard/extracted_visuals/v9_misleading_left.png"
    if os.path.exists(img_misleading):
        s11.shapes.add_picture(img_misleading, Inches(1.2), Inches(3.3), width=Inches(4.8))

    # Right: Ethical
    c11_r = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.25), card_w11, card_h11)
    c11_r.fill.solid()
    c11_r.fill.fore_color.rgb = C_CARD_WHITE
    c11_r.line.color.rgb = C_GREEN
    c11_r.line.width = Pt(1.5)

    tb11_r = s11.shapes.add_textbox(Inches(6.95), Inches(1.35), card_w11 - Inches(0.3), Inches(1.8))
    tf11_r = tb11_r.text_frame
    tf11_r.word_wrap = True
    p = tf11_r.paragraphs[0]
    p.text = "ETHICALLY CORRECTED REDESIGN"
    p.font.name = "Calibri"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_GREEN

    p = tf11_r.add_paragraph()
    p.text = "• Zero-Anchored Baseline: Vertical axis starts at true zero (0.0), preserving proportional visual bar heights.\n• Non-Parametric Rigor: Employs median and Interquartile Range (IQR) whiskers to faithfully communicate heavy right skew.\n• Full Transparency: Explicitly displays sample size (n) and units (pieces/m³).\n• Accessible Design: Uses colorblind-safe sequential navy palette."
    p.font.name = "Calibri"
    p.font.size = Pt(9.5)
    p.font.color.rgb = C_DARK

    img_ethical = "dashboard/extracted_visuals/v9_ethical_right.png"
    if os.path.exists(img_ethical):
        s11.shapes.add_picture(img_ethical, Inches(7.2), Inches(3.3), width=Inches(4.8))

    # -------------------------------------------------------------
    # SLIDE 12: KEY FINDINGS & INSIGHTS
    # -------------------------------------------------------------
    s12 = prs.slides.add_slide(blank_layout)
    add_chrome(s12, "Section 2 · 18 Marks", "Key Scientific Findings and Analytical Insights", 12)

    findings = [
        ("FINDING 1: SAMPLING EFFORT BIAS DISTORTS SPATIAL PERCEPTION",
         "Supported by V1, V2, and Power BI Page 1",
         "• 94.2% of all historical monitoring is concentrated in the Northern Hemisphere.\n• The Atlantic Ocean accounts for 66.7% of all data (19,394 samples) with a low median concentration of 0.42 pcs/m³.\n• In contrast, the Pacific Ocean holds only 24.4% of records but carries over 4x higher median pollution (1.84 pcs/m³).\n• Core Lesson: Observation density reflects maritime cruise traffic, NOT ecological severity."),

        ("FINDING 2: ENVIRONMENTAL COMPARTMENTS OPERATE ON DIFFERENT SCALES",
         "Supported by V4, V5, and Power BI Page 2",
         "• Surface water median concentration is 0.01 pcs/m³, while beach sand median is 1,280 pcs/m³.\n• Nurdle Patrol records a median of 10.0 pellets per 10-minute survey, with localized industrial spills exceeding 1,000 pellets.\n• Core Lesson: The 3 measurement units are physically incommensurate. Pooling them into a single global average produces invalid, deceptive numbers."),

        ("FINDING 3: NET MESH SIZE CREATES A 4X UNDER-COUNTING BIAS",
         "Supported by V6, V7, and Power BI Page 3",
         "• Standard manta and neuston nets use 333 um mesh, allowing synthetic microfibers (<100 um) to pass straight through.\n• Fine filtration samplers (<100 um) capture over 4.2x more microplastics per m³ than standard trawls.\n• Core Lesson: The vast majority of historical ocean data systematically under-counts total marine plastic burden.")
    ]

    card_w12 = Inches(3.7)
    card_h12 = Inches(3.9)
    for idx, (hdr, sub, body) in enumerate(findings):
        x = Inches(0.8) + idx * Inches(3.98)
        y = Inches(1.25)

        card = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, card_w12, card_h12)
        card.fill.solid()
        card.fill.fore_color.rgb = C_CARD_BG
        card.line.color.rgb = C_BORDER

        tb = s12.shapes.add_textbox(x + Inches(0.12), y + Inches(0.1), card_w12 - Inches(0.24), card_h12 - Inches(0.2))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = hdr
        p.font.name = "Calibri"
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = C_NAVY

        p_sub = tf.add_paragraph()
        p_sub.text = sub
        p_sub.font.name = "Calibri"
        p_sub.font.size = Pt(8.5)
        p_sub.font.italic = True
        p_sub.font.color.rgb = C_TEAL
        p_sub.space_after = Pt(6)

        for line in body.split("\n"):
            p = tf.add_paragraph()
            p.text = line
            p.font.name = "Calibri"
            p.font.size = Pt(9.5)
            p.font.color.rgb = C_DARK if not line.startswith("• Core") else C_NAVY
            if line.startswith("• Core"):
                p.font.bold = True
            p.space_after = Pt(2)

    summary_badges = [
        ("COUNT ≠ POLLUTION", "Sampling effort drives raw map density"),
        ("3 INCOMPATIBLE UNITS", "Never aggregate pieces/m³ with pieces/10 min"),
        ("CONTEXT MATTERS", "Always publish setting, gear, and sample size (n)")
    ]
    card_w12_b = Inches(3.7)
    for idx, (b_title, b_sub) in enumerate(summary_badges):
        x = Inches(0.8) + idx * Inches(3.98)
        y = Inches(5.35)

        card = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, card_w12_b, Inches(1.4))
        card.fill.solid()
        card.fill.fore_color.rgb = C_TEAL if idx == 0 else C_CARD_WHITE
        card.line.color.rgb = C_TEAL

        tb = s12.shapes.add_textbox(x, y + Inches(0.15), card_w12_b, Inches(1.1))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.text = b_title
        p.font.name = "Calibri"
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = C_CARD_WHITE if idx == 0 else C_NAVY

        p2 = tf.add_paragraph()
        p2.alignment = PP_ALIGN.CENTER
        p2.text = b_sub
        p2.font.name = "Calibri"
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = C_CARD_WHITE if idx == 0 else C_MUTED

    # -------------------------------------------------------------
    # SLIDE 13: RECOMMENDATIONS & CONCLUSION
    # -------------------------------------------------------------
    s13 = prs.slides.add_slide(blank_layout)
    add_chrome(s13, "Section 3 · 7 Marks", "Recommendations, Limitations, and Conclusion", 13)

    sections_s13 = [
        ("STRATEGIC POLICY RECOMMENDATIONS",
         "1. Mandatory IMO Classification of Resin Pellets:\n   Classify pre-production plastic pellets (nurdles) as Hazardous Cargo under the IMDG code, requiring secure below-deck container stowage.\n2. Standardize Dual-Mesh Sampling (INC-5 Treaty):\n   Mandate a unified protocol combining 50 um fine filtration (for microfibers) and 333 um manta trawls across all international monitoring cruises.\n3. Expand Southern Hemisphere Sensor Coverage:\n   Fund and deploy autonomous microplastic optical sensors on the global Argo Buoy array in the Indian and Southern Ocean data blindspots."),

        ("MAIN CONCLUSION & ANSWER TO PROBLEM STATEMENT",
         "• Responsible data visualization successfully decouples research effort from ecological reality.\n• When data is partitioned by setting and normalized for sampling density, true contamination hot spots shift from heavily-monitored tourist coasts to pelagic convergence gyres (Pacific) and industrial estuaries.\n• Ethical visualization protects public trust and ensures finite environmental cleanup capital targets genuine ecological emergencies."),

        ("STUDY LIMITATIONS & FUTURE WORK",
         "• Data Limitations: Historical records lack automated spectroscopic polymer identification (FTIR/Raman), and citizen science survey frequency is variable.\n• Future Improvement: Integrating satellite-derived ocean surface circulation models (HYCOM / Copernicus) with real-time autonomous buoys to predict microplastic drift trajectories.")
    ]

    card_h13 = Inches(1.75)
    for idx, (title, body) in enumerate(sections_s13):
        y = Inches(1.25) + idx * Inches(1.88)
        card = s13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), y, Inches(11.7), card_h13)
        card.fill.solid()
        card.fill.fore_color.rgb = C_CARD_BG
        card.line.color.rgb = C_BORDER

        tb = s13.shapes.add_textbox(Inches(0.95), y + Inches(0.08), Inches(11.4), card_h13 - Inches(0.16))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = title
        p.font.name = "Calibri"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = C_NAVY
        p.space_after = Pt(2)

        for line in body.split("\n"):
            p = tf.add_paragraph()
            p.text = line
            p.font.name = "Calibri"
            p.font.size = Pt(9.5)
            p.font.color.rgb = C_DARK
            p.space_after = Pt(1)

    # -------------------------------------------------------------
    # SLIDE 14: DASHBOARD DEMONSTRATION & VIVA
    # -------------------------------------------------------------
    s14 = prs.slides.add_slide(blank_layout)
    add_chrome(s14, "Section 3 · 7 Marks", "Dashboard Demonstration and Viva Defense Checklist", 14)

    # Left: Checklist
    c14_l = s14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.25), Inches(6.8), Inches(5.6))
    c14_l.fill.solid()
    c14_l.fill.fore_color.rgb = C_CARD_BG
    c14_l.line.color.rgb = C_BORDER

    tb14_l = s14.shapes.add_textbox(Inches(0.95), Inches(1.35), Inches(6.5), Inches(5.3))
    tf14_l = tb14_l.text_frame
    tf14_l.word_wrap = True

    p = tf14_l.paragraphs[0]
    p.text = "LIVE DASHBOARD DEMONSTRATION WORKFLOW"
    p.font.name = "Calibri"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p.space_after = Pt(8)

    demo_steps = [
        ("Step 1: Open Power BI Desktop (.pbip) Project",
         "Launch 'Marine_Microplastics_Executive.pbip' or double-click 'power_bi_interactive_dashboard.html'."),
        ("Step 2: Demonstrate Marine Setting Unit Isolation",
         "Select 'Marine Setting = Ocean water' on Page 1. Show that all visuals instantly filter to pieces/m³ exclusively with zero cross-unit contamination."),
        ("Step 3: Expose Northern Hemisphere Sampling Bias",
         "Demonstrate that 94.2% of records cluster in the North Atlantic and Gulf of Mexico, while the Indian Ocean (2.7%) and Southern Ocean (0.1%) remain blindspots."),
        ("Step 4: Explore Basin & Severity Deep-Dive",
         "Navigate to Page 2. Filter to 'Pacific Ocean' to prove that median concentration (1.84 pcs/m³) is over 4x higher than the over-sampled Atlantic Ocean."),
        ("Step 5: Present the Forensic Ethical Redesign",
         "Navigate to Page 3. Compare the truncated Y-axis chart (starting at 0.200) with the zero-baseline redesign to show how easily visual perception is manipulated."),
        ("Step 6: Defend Rigorous Data Decisions",
         "Explain why non-parametric statistics (median/IQR) and strict unit partitioning are mandatory for heavy-tailed environmental datasets.")
    ]
    for step_title, step_desc in demo_steps:
        p = tf14_l.add_paragraph()
        p.text = f"{step_title}: "
        p.font.name = "Calibri"
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = C_TEAL
        run = p.add_run()
        run.text = step_desc
        run.font.bold = False
        run.font.color.rgb = C_DARK
        p.space_after = Pt(4)

    # Right: Expected Viva Questions & Answers
    c14_r = s14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.8), Inches(1.25), Inches(4.7), Inches(5.6))
    c14_r.fill.solid()
    c14_r.fill.fore_color.rgb = C_CARD_WHITE
    c14_r.line.color.rgb = C_TEAL
    c14_r.line.width = Pt(1.5)

    tb14_r = s14.shapes.add_textbox(Inches(7.95), Inches(1.35), Inches(4.4), Inches(5.3))
    tf14_r = tb14_r.text_frame
    tf14_r.word_wrap = True

    p = tf14_r.paragraphs[0]
    p.text = "CORE VIVA DEFENSE PREPARATION"
    p.font.name = "Calibri"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p.space_after = Pt(8)

    viva_qas = [
        ("Q: Why did you not convert pieces/10 min into pieces/m³?",
         "A: It is physically impossible without knowing tow velocity, water depth, and wave dynamics. Nurdle Patrol is a timed shoreline search; pooling it with volumetric water tows would produce scientifically invalid pseudo-data."),
        ("Q: Why use Median and IQR instead of Mean and Std Dev?",
         "A: Environmental microplastic counts span 6 orders of magnitude (0.001 to >10,000) with high zero-rates. The arithmetic mean is heavily skewed by a few extreme outliers, whereas the median represents true typical exposure."),
        ("Q: How does Power BI ensure data integrity across units?",
         "A: Through a certified Star Schema where DAX measures apply strict context filtering and DAX switches enforce unit gating automatically."),
        ("Q: What is the single most actionable finding?",
         "A: Pre-production plastic pellets (nurdles) create intense coastal hotspots that can be immediately mitigated if the IMO classifies pellets as hazardous cargo.")
    ]
    for q, a in viva_qas:
        p = tf14_r.add_paragraph()
        p.text = f"{q}\n"
        p.font.name = "Calibri"
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = C_TEAL
        run = p.add_run()
        run.text = a
        run.font.bold = False
        run.font.color.rgb = C_DARK
        p.space_after = Pt(6)

    out_path = "data/raw/Marine_Microplastic_Pollution_Case_Study_Presentation.pptx"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    prs.save(out_path)
    print(f"Presentation saved successfully to: {out_path} ({len(prs.slides)} slides)")

if __name__ == "__main__":
    create_deck()
