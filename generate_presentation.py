# -*- coding: utf-8 -*-
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Professional Theme Colors
    C_NAVY = RGBColor(30, 41, 59)          # #1E293B
    C_INDIGO = RGBColor(79, 70, 229)       # #4F46E5
    C_CYAN = RGBColor(14, 165, 233)        # #0EA5E9
    C_BG_CARD = RGBColor(248, 250, 252)    # #F8FAFC
    C_LIGHT_BLUE = RGBColor(238, 242, 255) # #EEF2FF
    C_LIGHT_CYAN = RGBColor(240, 249, 255) # #F0F9FF
    C_TEXT_DARK = RGBColor(15, 23, 42)     # #0F172A
    C_TEXT_MUTED = RGBColor(100, 116, 139) # #64748B
    C_WHITE = RGBColor(255, 255, 255)
    C_BORDER = RGBColor(203, 213, 225)
    C_ACCENT_GREEN = RGBColor(16, 185, 129)# #10B981

    def add_header(slide, title_text, category_text="HIREMATCH AI - PHASE 2 AND 3"):
        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(1.0))
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p_cat = tf.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.name = "Calibri"
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = C_INDIGO
        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.name = "Calibri"
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = C_NAVY

    def add_bullet_cards(slide, title, category, cards):
        add_header(slide, title, category)
        count = len(cards)
        gap = 0.3
        total_width = 11.733
        card_w = (total_width - (gap * (count - 1))) / count
        card_h = 5.2
        top_y = 1.6
        for i, (head, points) in enumerate(cards):
            left_x = 0.8 + i * (card_w + gap)
            shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left_x), Inches(top_y), Inches(card_w), Inches(card_h))
            shape.fill.solid()
            shape.fill.fore_color.rgb = C_BG_CARD
            shape.line.color.rgb = C_BORDER
            shape.line.width = Pt(1)
            tb = slide.shapes.add_textbox(Inches(left_x + 0.25), Inches(top_y + 0.25), Inches(card_w - 0.5), Inches(card_h - 0.5))
            tf = tb.text_frame
            tf.word_wrap = True
            tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
            p_head = tf.paragraphs[0]
            p_head.text = head
            p_head.font.name = "Calibri"
            p_head.font.size = Pt(15)
            p_head.font.bold = True
            p_head.font.color.rgb = C_INDIGO
            for pt in points:
                p = tf.add_paragraph()
                p.text = f"-  {pt}"
                p.font.name = "Calibri"
                p.font.size = Pt(12)
                p.font.color.rgb = C_TEXT_DARK
                p.space_before = Pt(8)

    def add_table_slide(slide, title, category, headers, rows, col_widths=None):
        add_header(slide, title, category)
        num_rows = len(rows) + 1
        num_cols = len(headers)
        table_top = Inches(1.6)
        table_left = Inches(0.8)
        table_width = Inches(11.733)
        table_height = Inches(0.4 * num_rows)
        table_shape = slide.shapes.add_table(num_rows, num_cols, table_left, table_top, table_width, table_height)
        table = table_shape.table
        if col_widths:
            for idx, w in enumerate(col_widths):
                table.columns[idx].width = Inches(w)
        for col_idx, header in enumerate(headers):
            cell = table.cell(0, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = C_NAVY
            cell.text = header
            p = cell.text_frame.paragraphs[0]
            p.font.name = "Calibri"
            p.font.size = Pt(12)
            p.font.bold = True
            p.font.color.rgb = C_WHITE
            p.alignment = PP_ALIGN.LEFT
        for row_idx, row_data in enumerate(rows):
            for col_idx, text in enumerate(row_data):
                cell = table.cell(row_idx + 1, col_idx)
                cell.fill.solid()
                cell.fill.fore_color.rgb = C_BG_CARD if row_idx % 2 == 0 else C_WHITE
                cell.text = str(text)
                p = cell.text_frame.paragraphs[0]
                p.font.name = "Calibri"
                p.font.size = Pt(11)
                p.font.color.rgb = C_TEXT_DARK
                p.alignment = PP_ALIGN.LEFT

    # Helper: Add Box with Label
    def add_box(slide, x, y, w, h, text, bg_color=C_LIGHT_BLUE, border_color=C_INDIGO, text_color=C_TEXT_DARK, bold=True, font_size=11, shape_type=MSO_SHAPE.ROUNDED_RECTANGLE):
        s = slide.shapes.add_shape(shape_type, Inches(x), Inches(y), Inches(w), Inches(h))
        s.fill.solid()
        s.fill.fore_color.rgb = bg_color
        s.line.color.rgb = border_color
        s.line.width = Pt(1.5)
        tf = s.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = Inches(0.08)
        p = tf.paragraphs[0]
        p.text = text
        p.font.name = "Calibri"
        p.font.size = Pt(font_size)
        p.font.bold = bold
        p.font.color.rgb = text_color
        p.alignment = PP_ALIGN.CENTER
        return s

    # =========================================================================
    # SLIDE 1: TITLE
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = C_NAVY
    bg1.line.fill.background()
    tb1 = s1.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.3), Inches(4.0))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    p_badge = tf1.paragraphs[0]
    p_badge.text = "COLLEGE CAPSTONE PROJECT - PHASE 2 AND 3"
    p_badge.font.name = "Calibri"
    p_badge.font.size = Pt(13)
    p_badge.font.bold = True
    p_badge.font.color.rgb = C_CYAN
    p_title = tf1.add_paragraph()
    p_title.text = "HireMatch AI"
    p_title.font.name = "Calibri"
    p_title.font.size = Pt(40)
    p_title.font.bold = True
    p_title.font.color.rgb = C_WHITE
    p_title.space_before = Pt(8)
    p_sub = tf1.add_paragraph()
    p_sub.text = "AI-Based Resume Screening, Job Matching and Candidate Ranking System"
    p_sub.font.name = "Calibri"
    p_sub.font.size = Pt(18)
    p_sub.font.color.rgb = RGBColor(203, 213, 225)
    p_sub.space_before = Pt(8)
    p_team = tf1.add_paragraph()
    p_team.text = "System Architecture | Use Case Specifications | DFD | ER Modeling | Database Design\nTeam: Mahi Jha (AI/NLP and Coordination) | Ekta (Frontend UI) | Tanishka (Backend and Database)"
    p_team.font.name = "Calibri"
    p_team.font.size = Pt(13)
    p_team.font.color.rgb = RGBColor(148, 163, 184)
    p_team.space_before = Pt(28)

    # =========================================================================
    # SLIDE 2: APPROACH
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_bullet_cards(s2, "Architectural Approach - Function-Oriented Design", "SYSTEM DESIGN", [
        ("Design Paradigm", ["Modular, function-oriented data flow architecture.", "AI and matching operate as pure functional pipelines.", "Stateless REST API services via FastAPI.", "Clear decoupling between AI, API Gateway, and Storage."]),
        ("Justification of Diagrams", ["As per evaluation criteria, function-oriented systems are modeled via DFDs and ER diagrams.", "Data Flow Diagrams (Level 0 and 1) show multi-stage document processing.", "Entity-Relationship diagrams define relational persistence in SQLite.", "Eliminates unnecessary object state coupling in computational pipelines."]),
        ("Key Architectural Goals", ["Fault-tolerant batch processing (up to 20 resumes).", "Explainable AI: matched vs missing skills explicitly isolated.", "High throughput document parsing via PyMuPDF C-bindings.", "Sub-second vector semantic scoring with local embeddings."])
    ])

    # =========================================================================
    # SLIDE 3: VISUAL SYSTEM ARCHITECTURE DIAGRAM
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Three-Tier System Architecture Diagram", "SYSTEM ARCHITECTURE")
    # Tier 1
    add_box(s3, 1.0, 1.6, 11.3, 1.3, "TIER 1: PRESENTATION LAYER (Web Client - HTML5 / CSS3 / Vanilla JavaScript)", C_LIGHT_BLUE, C_INDIGO, C_INDIGO, True, 13)
    add_box(s3, 1.4, 2.1, 5.0, 0.6, "Job Seeker Portal (Single PDF Analysis)", C_WHITE, C_BORDER, C_TEXT_DARK, False, 11)
    add_box(s3, 6.9, 2.1, 5.0, 0.6, "Recruiter Dashboard (Batch Upload & Ranking)", C_WHITE, C_BORDER, C_TEXT_DARK, False, 11)

    # Arrow 1->2
    add_box(s3, 6.2, 2.95, 0.9, 0.35, "REST JSON", C_LIGHT_CYAN, C_CYAN, C_NAVY, True, 9, MSO_SHAPE.DOWN_ARROW)

    # Tier 2
    add_box(s3, 1.0, 3.35, 11.3, 2.1, "TIER 2: APPLICATION & AI/NLP ENGINE (FastAPI Gateway - Python 3.12)", C_LIGHT_CYAN, C_CYAN, C_NAVY, True, 13)
    add_box(s3, 1.3, 3.85, 2.5, 1.4, "Document Parsing\n(PyMuPDF C-Bindings)\nPDF -> UTF-8 Text", C_WHITE, C_BORDER, C_TEXT_DARK, False, 11)
    add_box(s3, 4.1, 3.85, 2.6, 1.4, "Skill Extractor\n(Boundary Regex)\nAlias Normalization", C_WHITE, C_BORDER, C_TEXT_DARK, False, 11)
    add_box(s3, 7.0, 3.85, 2.6, 1.4, "Semantic Matcher\nSentenceTransformers\n(100-word chunking)", C_WHITE, C_BORDER, C_TEXT_DARK, False, 11)
    add_box(s3, 9.9, 3.85, 2.1, 1.4, "Batch Ranking\nSorting Algorithm\nLeaderboard Output", C_WHITE, C_BORDER, C_TEXT_DARK, False, 11)

    # Arrow 2->3
    add_box(s3, 6.2, 5.5, 0.9, 0.35, "SQLite SQL", C_LIGHT_BLUE, C_INDIGO, C_NAVY, True, 9, MSO_SHAPE.DOWN_ARROW)

    # Tier 3
    add_box(s3, 1.0, 5.9, 11.3, 1.1, "TIER 3: PERSISTENCE LAYER (Relational Database - SQLite hirematch.db)", C_LIGHT_BLUE, C_INDIGO, C_INDIGO, True, 13)
    add_box(s3, 1.4, 6.35, 5.0, 0.5, "Table: analysis_results (Scores, Skills, Rank)", C_WHITE, C_BORDER, C_TEXT_DARK, False, 11)
    add_box(s3, 6.9, 6.35, 5.0, 0.5, "Table: shortlists (Selected Candidates, Notes)", C_WHITE, C_BORDER, C_TEXT_DARK, False, 11)

    # =========================================================================
    # SLIDE 4: VISUAL USE CASE DIAGRAM
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "System Use Case Diagram", "USE CASE MODELING")
    
    # System boundary box
    s_boundary = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(3.2), Inches(1.6), Inches(7.0), Inches(5.3))
    s_boundary.fill.solid()
    s_boundary.fill.fore_color.rgb = C_BG_CARD
    s_boundary.line.color.rgb = C_INDIGO
    s_boundary.line.width = Pt(1.5)
    tf_b = s_boundary.text_frame
    p_b = tf_b.paragraphs[0]
    p_b.text = "HIREMATCH AI PLATFORM BOUNDARY"
    p_b.font.size = Pt(11)
    p_b.font.bold = True
    p_b.font.color.rgb = C_INDIGO
    p_b.alignment = PP_ALIGN.CENTER

    # Left Actor: Job Seeker
    add_box(s4, 0.8, 2.7, 2.0, 2.8, "ACTOR:\nJOB SEEKER\n\n(Uploads Resume,\nSelf-Evaluation,\nViews Feedback)", C_LIGHT_BLUE, C_INDIGO, C_NAVY, True, 12, MSO_SHAPE.ROUNDED_RECTANGLE)

    # Right Actor: Recruiter
    add_box(s4, 10.6, 2.7, 2.0, 2.8, "ACTOR:\nRECRUITER\n\n(Batch Upload,\nRole Filtering,\nCandidate Ranking,\nShortlisting)", C_LIGHT_CYAN, C_CYAN, C_NAVY, True, 12, MSO_SHAPE.ROUNDED_RECTANGLE)

    # Use Case Ovals inside boundary
    add_box(s4, 3.6, 2.1, 2.9, 0.75, "UC-01: Upload PDF Resume", C_WHITE, C_INDIGO, C_TEXT_DARK, True, 11, MSO_SHAPE.OVAL)
    add_box(s4, 6.9, 2.1, 2.9, 0.75, "UC-02: Enter Job Description", C_WHITE, C_INDIGO, C_TEXT_DARK, True, 11, MSO_SHAPE.OVAL)
    add_box(s4, 3.6, 3.1, 2.9, 0.75, "UC-03: Single Resume Analysis", C_WHITE, C_INDIGO, C_TEXT_DARK, True, 11, MSO_SHAPE.OVAL)
    add_box(s4, 6.9, 3.1, 2.9, 0.75, "UC-04: Batch Upload (1-20)", C_WHITE, C_CYAN, C_TEXT_DARK, True, 11, MSO_SHAPE.OVAL)
    add_box(s4, 3.6, 4.1, 2.9, 0.75, "UC-05: View Skills & Gap Tips", C_WHITE, C_INDIGO, C_TEXT_DARK, True, 11, MSO_SHAPE.OVAL)
    add_box(s4, 6.9, 4.1, 2.9, 0.75, "UC-06: Rank Candidates", C_WHITE, C_CYAN, C_TEXT_DARK, True, 11, MSO_SHAPE.OVAL)
    add_box(s4, 5.2, 5.1, 3.2, 0.75, "UC-07: Shortlist & Persist Candidate", C_WHITE, C_ACCENT_GREEN, C_TEXT_DARK, True, 11, MSO_SHAPE.OVAL)

    # Indicator connectors
    add_box(s4, 2.8, 3.2, 0.4, 0.3, "-->", C_LIGHT_BLUE, C_BORDER, C_INDIGO, True, 10, MSO_SHAPE.RIGHT_ARROW)
    add_box(s4, 10.1, 3.7, 0.4, 0.3, "<--", C_LIGHT_CYAN, C_BORDER, C_CYAN, True, 10, MSO_SHAPE.LEFT_ARROW)

    # =========================================================================
    # SLIDE 5: ACTORS TABLE
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_table_slide(s5, "Actors and Their Roles Specification", "USE CASE SPECIFICATION",
        ["Actor", "Type", "Scope of Interaction", "Core System Responsibilities"],
        [
            ["Job Seeker", "Primary Actor", "Single Resume Portal", "Uploads personal CV, pastes target JD, views individual match score and skill gaps."],
            ["Recruiter", "Primary Actor", "Recruiter Dashboard", "Uploads multiple candidate resumes in batch, triggers ranking algorithm, marks candidates as shortlisted."],
            ["FastAPI Gateway", "System / Secondary", "REST Controller", "Validates binary PDF headers, handles CORS, routes payloads to AI modules, sends JSON responses."],
            ["AI / NLP Engine", "Internal Processor", "Computational Core", "Extracts canonical skills via regex, performs sentence-transformer chunk embeddings, sorts candidate leaderboard."],
            ["SQLite Database", "Data Store", "Persistence Layer", "Stores candidate analysis results, matching metrics, and persistent recruiter shortlist records."]
        ],
        [1.8, 1.8, 2.3, 5.8]
    )

    # =========================================================================
    # SLIDES 6, 7, 8: USE CASE SPECS
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_table_slide(s6, "Use Case Specification: UC-01 (Single Resume Screening)", "USE CASE DETAILS",
        ["Specification Field", "Description / System Contract"],
        [
            ["Use Case ID and Name", "UC-01: Analyze Single Resume Alignment"],
            ["Primary Actor", "Job Seeker (Candidate)"],
            ["Preconditions", "1. Resume must be a valid, unencrypted PDF. 2. Job description text is provided."],
            ["Trigger", "User clicks 'Analyze Resume' button on client interface."],
            ["Main Success Scenario", "1. Backend validates PDF magic byte (%PDF-).\n2. PyMuPDF extracts readable text string.\n3. Skill extractor runs alias normalization and boundary regex.\n4. Transformer calculates chunked cosine similarity.\n5. Returns Match %, Semantic Score, Matched/Missing skills, and tailored suggestions."],
            ["Alternative Flows", "A1: Uploaded file is not PDF -> HTTP 400 'PDF files only'.\nA2: Scanned/Image PDF without text -> HTTP 422 'No readable text found'.\nA3: Empty Job Description -> HTTP 400 'Job description cannot be empty'.\nA4: Zero technical skills in JD -> Returns match_score: null with clear note."],
            ["Postconditions", "Comprehensive analysis report rendered on Job Seeker screen without persisting personally identifiable data."]
        ],
        [2.8, 8.9]
    )

    s7 = prs.slides.add_slide(blank_layout)
    add_table_slide(s7, "Use Case Specification: UC-02 (Batch Screening and Ranking)", "USE CASE DETAILS",
        ["Specification Field", "Description / System Contract"],
        [
            ["Use Case ID and Name", "UC-02: Batch Resume Screening and Candidate Ranking"],
            ["Primary Actor", "Recruiter / Hiring Manager"],
            ["Preconditions", "1. Recruiter selects between 1 to 20 PDF resumes. 2. Target Job Description is entered."],
            ["Trigger", "Recruiter clicks 'Analyze Candidates' on Recruiter Dashboard."],
            ["Main Success Scenario", "1. Client submits multipart FormData containing array of files.\n2. Backend validates each file and extracts text.\n3. Candidates batch processed via analyze_multiple_resumes().\n4. Candidates sorted descending by (Valid Score > Skill Match % > Semantic Score).\n5. Ranked list (Rank 1, 2, 3...) with detailed scores returned to frontend."],
            ["Fault-Tolerant Flow", "A1: Corrupted or unreadable PDF within the batch is marked as 'Status: Failed' with error description, allowing remaining valid resumes to be ranked uninterrupted.\nA2: More than 20 files uploaded -> Blocked with HTTP 400 limit alert."],
            ["Postconditions", "Ranked candidate leaderboard displayed with matched skills, missing skills, and shortlisting triggers."]
        ],
        [2.8, 8.9]
    )

    s8 = prs.slides.add_slide(blank_layout)
    add_table_slide(s8, "Use Case Specification: UC-03 (Candidate Shortlisting)", "USE CASE DETAILS",
        ["Specification Field", "Description / System Contract"],
        [
            ["Use Case ID and Name", "UC-03: Candidate Shortlisting and Status Persistence"],
            ["Primary Actor", "Recruiter"],
            ["Preconditions", "Batch candidate ranking has completed and results are active on dashboard."],
            ["Trigger", "Recruiter clicks 'Shortlist' action button next to a candidate's record."],
            ["Main Success Scenario", "1. Client sends candidate filename, JD, score, and optional notes to backend.\n2. Backend executes SQLite INSERT transaction into shortlists table.\n3. Database auto-generates record ID and UTC timestamp.\n4. Backend returns HTTP 200 OK confirmation.\n5. UI reflects updated state ('Shortlisted' badge / disabled action)."],
            ["Alternative Flows", "A1: Database locked or I/O error -> System catches OSError and returns HTTP 500 with retry notice."],
            ["Postconditions", "Candidate record permanently persisted in SQLite hirematch.db and visible in shortlisted tab."]
        ],
        [2.8, 8.9]
    )

    # =========================================================================
    # SLIDE 9: VISUAL DFD LEVEL 0 (CONTEXT DIAGRAM)
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Data Flow Diagram (DFD) - Level 0 Context Diagram", "DATA FLOW MODELING")

    # Left Entity
    add_box(s9, 0.8, 2.7, 2.6, 2.2, "EXTERNAL ENTITY:\nJOB SEEKER\n\n(Uploads Resume,\nTarget JD)", C_LIGHT_BLUE, C_INDIGO, C_NAVY, True, 13)

    # Center Process Bubble (Circle)
    add_box(s9, 4.8, 2.2, 3.8, 3.2, "PROCESS 0.0:\n\nHIREMATCH AI\nRESUME SCREENING\nSYSTEM\n\n(Ingestion, NLP,\nScoring, Ranking)", C_NAVY, C_INDIGO, C_WHITE, True, 14, MSO_SHAPE.OVAL)

    # Right Entity
    add_box(s9, 10.0, 2.7, 2.6, 2.2, "EXTERNAL ENTITY:\nRECRUITER\n\n(Batch Resumes,\nRole Specs, Shortlist)", C_LIGHT_CYAN, C_CYAN, C_NAVY, True, 13)

    # Left Flows
    add_box(s9, 3.4, 2.9, 1.4, 0.4, "Resume PDF + JD", C_WHITE, C_BORDER, C_TEXT_DARK, False, 9)
    add_box(s9, 3.4, 3.4, 0.9, 0.3, "-->", C_LIGHT_BLUE, C_BORDER, C_INDIGO, True, 9, MSO_SHAPE.RIGHT_ARROW)

    add_box(s9, 3.4, 4.0, 1.4, 0.4, "Match Analytics", C_WHITE, C_BORDER, C_TEXT_DARK, False, 9)
    add_box(s9, 3.4, 4.5, 0.9, 0.3, "<--", C_LIGHT_BLUE, C_BORDER, C_INDIGO, True, 9, MSO_SHAPE.LEFT_ARROW)

    # Right Flows
    add_box(s9, 8.6, 2.9, 1.4, 0.4, "Batch Resumes", C_WHITE, C_BORDER, C_TEXT_DARK, False, 9)
    add_box(s9, 9.1, 3.4, 0.9, 0.3, "<--", C_LIGHT_CYAN, C_BORDER, C_CYAN, True, 9, MSO_SHAPE.LEFT_ARROW)

    add_box(s9, 8.6, 4.0, 1.4, 0.4, "Ranked Leaderboard", C_WHITE, C_BORDER, C_TEXT_DARK, False, 9)
    add_box(s9, 8.6, 4.5, 0.9, 0.3, "-->", C_LIGHT_CYAN, C_BORDER, C_CYAN, True, 9, MSO_SHAPE.RIGHT_ARROW)

    # =========================================================================
    # SLIDE 10: VISUAL DFD LEVEL 1 (PROCESS DECOMPOSITION)
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Data Flow Diagram (DFD) - Level 1 Process Decomposition", "DATA FLOW MODELING")

    # Process 1.0
    add_box(s10, 0.8, 1.8, 2.4, 1.5, "1.0 PDF PARSING\n\nInput: PDF Bytes\nOutput: Text String\n(PyMuPDF fitz)", C_WHITE, C_INDIGO, C_TEXT_DARK, True, 10, MSO_SHAPE.OVAL)
    add_box(s10, 3.3, 2.3, 0.7, 0.3, "Text", C_LIGHT_BLUE, C_BORDER, C_INDIGO, True, 8, MSO_SHAPE.RIGHT_ARROW)

    # Process 2.0
    add_box(s10, 4.1, 1.8, 2.4, 1.5, "2.0 SKILL EXTRACT\n\nRegex Word Boundaries\nAlias Normalization\nCanonical Skills", C_WHITE, C_INDIGO, C_TEXT_DARK, True, 10, MSO_SHAPE.OVAL)
    add_box(s10, 6.6, 2.3, 0.7, 0.3, "Skills", C_LIGHT_BLUE, C_BORDER, C_INDIGO, True, 8, MSO_SHAPE.RIGHT_ARROW)

    # Process 3.0
    add_box(s10, 4.1, 3.8, 2.4, 1.5, "3.0 SEMANTIC MODEL\n\n100-word Chunking\nall-MiniLM-L6-v2\nDense Embeddings", C_WHITE, C_CYAN, C_TEXT_DARK, True, 10, MSO_SHAPE.OVAL)
    add_box(s10, 6.6, 4.3, 0.7, 0.3, "Vectors", C_LIGHT_CYAN, C_BORDER, C_CYAN, True, 8, MSO_SHAPE.RIGHT_ARROW)

    # Process 4.0
    add_box(s10, 7.4, 2.6, 2.5, 1.8, "4.0 SCORING &\nRANKING ENGINE\n\nSkill Match % +\nTop-3 Cosine Similarity\nSort & Assign Rank", C_LIGHT_BLUE, C_INDIGO, C_NAVY, True, 11, MSO_SHAPE.OVAL)
    add_box(s10, 10.0, 3.3, 0.6, 0.3, "Store", C_LIGHT_BLUE, C_BORDER, C_INDIGO, True, 8, MSO_SHAPE.RIGHT_ARROW)

    # Data Store D1
    add_box(s10, 10.7, 2.8, 2.0, 1.4, "[D1] ANALYSIS RESULTS\n\nScores, Skills,\nRankings, Metrics", C_LIGHT_CYAN, C_CYAN, C_NAVY, True, 10, MSO_SHAPE.RECTANGLE)

    # Process 5.0
    add_box(s10, 7.4, 5.0, 2.5, 1.4, "5.0 SHORTLISTING\n\nRecruiter Action\nStatus = Shortlisted", C_WHITE, C_ACCENT_GREEN, C_TEXT_DARK, True, 10, MSO_SHAPE.OVAL)
    add_box(s10, 10.0, 5.5, 0.6, 0.3, "Save", C_LIGHT_BLUE, C_BORDER, C_ACCENT_GREEN, True, 8, MSO_SHAPE.RIGHT_ARROW)

    # Data Store D2
    add_box(s10, 10.7, 5.0, 2.0, 1.4, "[D2] SHORTLISTS STORE\n\nCandidate Decisions,\nNotes, Timestamps", C_LIGHT_BLUE, C_ACCENT_GREEN, C_NAVY, True, 10, MSO_SHAPE.RECTANGLE)

    # =========================================================================
    # SLIDE 11: VISUAL ER DIAGRAM
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "Entity-Relationship (ER) Diagram", "DATABASE DESIGN")

    # Table 1: ANALYSIS_RESULTS
    add_box(s11, 1.0, 1.8, 4.6, 5.0, "", C_BG_CARD, C_INDIGO, C_TEXT_DARK, True, 10, MSO_SHAPE.ROUNDED_RECTANGLE)
    add_box(s11, 1.0, 1.8, 4.6, 0.7, "ENTITY: ANALYSIS_RESULTS", C_NAVY, C_INDIGO, C_WHITE, True, 13)
    tb_er1 = s11.shapes.add_textbox(Inches(1.2), Inches(2.6), Inches(4.2), Inches(4.0))
    tf_er1 = tb_er1.text_frame
    tf_er1.word_wrap = True
    attrs1 = [
        "PK  id : INTEGER (AUTOINCREMENT)",
        "    filename : TEXT",
        "    job_description : TEXT",
        "    skill_match_score : REAL (Nullable)",
        "    semantic_similarity_score : INTEGER",
        "    matched_skills : TEXT",
        "    missing_skills : TEXT",
        "    rank : INTEGER (Nullable)",
        "    created_at : TIMESTAMP"
    ]
    for idx, att in enumerate(attrs1):
        p = tf_er1.paragraphs[0] if idx == 0 else tf_er1.add_paragraph()
        p.text = att
        p.font.name = "Calibri"
        p.font.size = Pt(11)
        p.font.bold = True if "PK" in att else False
        p.font.color.rgb = C_INDIGO if "PK" in att else C_TEXT_DARK
        p.space_before = Pt(6)

    # Center Connector: 1:N
    add_box(s11, 6.0, 3.6, 1.5, 1.0, "< 1 : N >\nShortlisted\nAs", C_LIGHT_BLUE, C_CYAN, C_NAVY, True, 11, MSO_SHAPE.DIAMOND)

    # Table 2: SHORTLISTS
    add_box(s11, 7.9, 1.8, 4.4, 4.5, "", C_BG_CARD, C_ACCENT_GREEN, C_TEXT_DARK, True, 10, MSO_SHAPE.ROUNDED_RECTANGLE)
    add_box(s11, 7.9, 1.8, 4.4, 0.7, "ENTITY: SHORTLISTS", C_ACCENT_GREEN, C_ACCENT_GREEN, C_WHITE, True, 13)
    tb_er2 = s11.shapes.add_textbox(Inches(8.1), Inches(2.6), Inches(4.0), Inches(3.5))
    tf_er2 = tb_er2.text_frame
    tf_er2.word_wrap = True
    attrs2 = [
        "PK  id : INTEGER (AUTOINCREMENT)",
        "    filename : TEXT",
        "    job_description : TEXT",
        "    skill_match_score : REAL",
        "    status : TEXT ('Shortlisted')",
        "    notes : TEXT (Optional)",
        "    shortlisted_at : TIMESTAMP"
    ]
    for idx, att in enumerate(attrs2):
        p = tf_er2.paragraphs[0] if idx == 0 else tf_er2.add_paragraph()
        p.text = att
        p.font.name = "Calibri"
        p.font.size = Pt(11)
        p.font.bold = True if "PK" in att else False
        p.font.color.rgb = C_ACCENT_GREEN if "PK" in att else C_TEXT_DARK
        p.space_before = Pt(6)

    # =========================================================================
    # SLIDE 12: DB SCHEMA
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_table_slide(s12, "Database Schema and Data Dictionary (SQLite)", "DATABASE DESIGN",
        ["Table", "Column Name", "Data Type", "Constraints", "Description"],
        [
            ["analysis_results", "id", "INTEGER", "PRIMARY KEY AUTOINCREMENT", "Unique record identifier"],
            ["analysis_results", "filename", "TEXT", "NOT NULL", "Original resume file name"],
            ["analysis_results", "skill_match_score", "REAL", "NULLABLE", "Calculated skill match percentage (0-100)"],
            ["analysis_results", "semantic_similarity", "INTEGER", "NOT NULL", "Dense vector cosine similarity score (0-100)"],
            ["analysis_results", "matched_skills", "TEXT", "NOT NULL", "Serialized list of intersecting skills"],
            ["analysis_results", "rank", "INTEGER", "NULLABLE", "Batch ranking position (1, 2, 3...)"],
            ["shortlists", "id", "INTEGER", "PRIMARY KEY AUTOINCREMENT", "Unique shortlist entry identifier"],
            ["shortlists", "filename", "TEXT", "NOT NULL", "Shortlisted candidate resume identifier"],
            ["shortlists", "status", "TEXT", "DEFAULT 'Shortlisted'", "Recruitment funnel progression status"],
            ["shortlists", "shortlisted_at", "TIMESTAMP", "DEFAULT CURRENT_TIMESTAMP", "Action audit timestamp"]
        ],
        [1.8, 2.2, 1.4, 2.8, 3.5]
    )

    # =========================================================================
    # SLIDE 13: AI/NLP INNOVATION
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    add_bullet_cards(s13, "AI/NLP Pipeline Deep-Dive and Innovation", "AI/NLP ENGINEERING", [
        ("Canonical Skill Normalization", ["Solves keyword mismatch via dictionary-based alias substitution.", "Regex pattern handles boundaries cleanly.", "Maps 'PowerBI' -> 'Power BI', 'MS Excel' -> 'Excel', 'JS' -> 'JavaScript', 'Data Analytics' -> 'Data Analysis'.", "Eliminates substring false positives (e.g., 'BI' inside 'PowerBI')."]),
        ("Long-Resume Chunking Solution", ["The Problem: SentenceTransformers truncate long resumes (>512 tokens), dropping cosine score falsely to 18%.", "Our Solution: Divide resume into 100-word logical chunks.", "Compute cosine similarity for all chunks against JD.", "Average the Top-3 highest scoring chunks.", "Result: Calibrated, realistic semantic score (42-87/100)."]),
        ("Dual-Scoring Philosophy", ["We strictly DO NOT combine scores arbitrarily (e.g. 0.5*Skill + 0.5*Semantic).", "Skill Match Score = Explicit hard technical requirement compliance.", "Semantic Score = Contextual and domain vocabulary alignment.", "Offers explainability instead of deceptive black-box numbers."])
    ])

    # =========================================================================
    # SLIDE 14: REST API ARCHITECTURE
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    add_table_slide(s14, "FastAPI REST API Architecture and Endpoints", "API INTEGRATION",
        ["HTTP Method", "Endpoint Route", "Input Payload", "Response Payload and Status"],
        [
            ["GET", "/health", "None", "{'status': 'healthy'} (HTTP 200)"],
            ["POST", "/upload-resume", "UploadFile (PDF)", "{'message': 'Uploaded', 'filename': str, 'size_bytes': int}"],
            ["POST", "/extract-resume-text", "UploadFile (PDF)", "{'filename': str, 'text': str, 'characters': int}"],
            ["POST", "/analyze-resume", "file: UploadFile, job_description: Form(str)", "{'skill_match_score': int, 'semantic_similarity': int, 'matched': [], 'missing': [], 'suggestions': []}"],
            ["POST", "/analyze-multiple-resumes", "files: list[UploadFile], job_description: Form(str)", "{'total_analyzed': int, 'results': [ranked_candidates], 'invalid_files': []}"],
            ["POST", "/shortlist-candidate", "JSON {filename, job_description, score, notes}", "{'message': 'Candidate shortlisted', 'id': int}"]
        ],
        [1.6, 2.7, 3.2, 4.2]
    )

    # =========================================================================
    # SLIDE 15: TEST RESULTS
    # =========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    add_bullet_cards(s15, "Experimental Verification and Test Results", "TESTING AND VALIDATION", [
        ("Test 1: Alias Extraction Verification", ["Input: 'PowerBI, MS Excel, JS, ML and Python experience.'", "Extracted: ['Python', 'JavaScript', 'Excel', 'Power BI', 'Machine Learning'].", "Verified: 100% accurate alias normalization without substring corruption."]),
        ("Test 2: Real PDF Resume (4,407 Chars)", ["Input: Real candidate PDF resume parsed via PyMuPDF.", "Extracted 15 technical skills cleanly.", "JD Match: 4 out of 9 required skills matched (44% Match Score).", "Semantic Score: 42/100 (Chunking successfully prevented truncation drop)."]),
        ("Test 3: Edge Case and Fault Tolerance", ["Empty Resume / Blank JD: Blocked cleanly with HTTP 400 (ValueError).", "JD with 0 recognized skills: Returned skill_match_score: None (Prevented ZeroDivisionError).", "Corrupted PDF in batch: Skipped gracefully with status 'Failed'; valid resumes ranked."])
    ])

    # =========================================================================
    # SLIDE 16: TEAM RESPONSIBILITIES
    # =========================================================================
    s16 = prs.slides.add_slide(blank_layout)
    add_table_slide(s16, "Team Structure and Individual Contributions", "TEAM RESPONSIBILITIES",
        ["Team Member", "Assigned Role", "Core Responsibilities", "Delivered Milestones"],
        [
            ["Mahi Jha", "AI/NLP Engineer and Project Coordinator", "AI Matching Logic, Semantic Modeling, Overall Architecture Sync", "1. Skill Extractor with boundary regex\n2. Chunking Semantic Matcher\n3. Batch Ranking Engine\n4. Real PDF and Edge-case test suites."],
            ["Ekta", "Frontend Developer", "UI/UX Design, Client-side Form Handling, Dashboard Presentation", "1. HTML5 structure and modern CSS styling\n2. Candidate single-analysis upload form\n3. Recruiter batch screening dashboard\n4. Dynamic ranked candidate table rendering."],
            ["Tanishka", "Backend and Database Engineer", "FastAPI Endpoints, SQLite Database Integration, Persistence Models", "1. SQLite connection (hirematch.db)\n2. Database tables schema design\n3. Shortlist persistence endpoints\n4. FastAPI multipart request handling."]
        ],
        [1.8, 2.2, 3.2, 4.5]
    )

    # =========================================================================
    # SLIDE 17: STATUS
    # =========================================================================
    s17 = prs.slides.add_slide(blank_layout)
    add_bullet_cards(s17, "Current Implementation Status and Demo Readiness", "PROJECT MILESTONES", [
        ("AI / NLP Module (100% Complete)", ["Skill Extraction and Normalization: Verified.", "Chunked Semantic Similarity: Verified.", "Batch Ranking Engine: Verified.", "Edge-case and Exception Handling: Verified."]),
        ("Backend and Ingestion (100% Complete)", ["PyMuPDF binary text extraction: Working.", "Single analysis route (/analyze-resume): Working.", "Batch screening route (/analyze-multiple-resumes): Working.", "OpenAPI 3.0.2 Swagger fix implemented."]),
        ("Database and UI (In Progress)", ["SQLite database connection initialized.", "Shortlist persistence schema defined.", "Frontend HTML/CSS layout prepared.", "Next: Connecting frontend AJAX fetch to batch endpoints."])
    ])

    # =========================================================================
    # SLIDE 18: CONCLUSION
    # =========================================================================
    s18 = prs.slides.add_slide(blank_layout)
    add_bullet_cards(s18, "Conclusion and Immediate Next Steps", "SUMMARY", [
        ("System Value Proposition", ["Transparent decision-support system for high-volume recruitment.", "Eliminates resume screening fatigue while safeguarding against biased black-box decisions.", "Provides actionable feedback for candidates to improve job market alignment."]),
        ("Immediate Next Steps", ["Integrate SQLite shortlist functions into backend API.", "Bind Recruiter Dashboard JavaScript fetch calls to /analyze-multiple-resumes.", "Conduct full end-to-end integration test from browser upload to database persistence."]),
        ("Future Scope", ["Optical Character Recognition (OCR) support for scanned/image resumes.", "Automated experience and education weighting.", "Multi-lingual resume parsing capability."])
    ])

    output_path = "HireMatch_AI_Presentation.pptx"
    prs.save(output_path)
    print(f"SUCCESS: Presentation with diagrams saved as '{output_path}'!")

if __name__ == "__main__":
    create_deck()
