import os
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

LOGO_PATH = os.path.join("assets", "logo", "zp-logo.png")
FONT_PATH = os.path.join("assets", "fonts", "Orbitron-VariableFont_wght.ttf")
FONT_NAME = "Orbitron"
REPORTS_DIR = "reports"

COLOR_PRIMARY = HexColor("#8A2BE2")
COLOR_SECTION = HexColor("#0097A7")
COLOR_BACKGROUND = white
COLOR_TEXT = HexColor("#1A1A1A")
COLOR_BORDER = HexColor("#CCCCCC")

COLOR_LOW = HexColor("#2E7D32")
COLOR_MEDIUM = HexColor("#F9A825")
COLOR_HIGH = HexColor("#C62828")

THREAT_COLORS = {
    "LOW": COLOR_LOW,
    "MEDIUM": COLOR_MEDIUM,
    "HIGH": COLOR_HIGH,
}

PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN = 18 * mm
PAGE_BORDER_MARGIN = 9 * mm


def _register_font():
    if FONT_NAME not in pdfmetrics.getRegisteredFontNames():
        if not os.path.isfile(FONT_PATH):
            raise FileNotFoundError(f"Font file not found at {FONT_PATH}")
        pdfmetrics.registerFont(TTFont(FONT_NAME, FONT_PATH))


def _ensure_reports_dir():
    if not os.path.isdir(REPORTS_DIR):
        os.makedirs(REPORTS_DIR, exist_ok=True)


def _draw_rounded_box(pdf, x, y, width, height, stroke_color, fill_color=None,
                       line_width=1.0, radius=6):
    pdf.saveState()
    pdf.setStrokeColor(stroke_color)
    pdf.setLineWidth(line_width)
    if fill_color is not None:
        pdf.setFillColor(fill_color)
        pdf.roundRect(x, y, width, height, radius, stroke=1, fill=1)
    else:
        pdf.roundRect(x, y, width, height, radius, stroke=1, fill=0)
    pdf.restoreState()


def _draw_page_border(pdf):
    pdf.saveState()
    pdf.setStrokeColor(COLOR_PRIMARY)
    pdf.setLineWidth(1.4)
    pdf.roundRect(
        PAGE_BORDER_MARGIN,
        PAGE_BORDER_MARGIN,
        PAGE_WIDTH - 2 * PAGE_BORDER_MARGIN,
        PAGE_HEIGHT - 2 * PAGE_BORDER_MARGIN,
        8,
        stroke=1,
        fill=0,
    )
    pdf.restoreState()


def _fill_background(pdf):
    pdf.setFillColor(COLOR_BACKGROUND)
    pdf.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, stroke=0, fill=1)


def _draw_header(pdf, y_cursor):
    if os.path.isfile(LOGO_PATH):
        try:
            logo = ImageReader(LOGO_PATH)
            logo_width, logo_height = logo.getSize()
            aspect = logo_height / float(logo_width)
            display_width = 45 * mm
            display_height = display_width * aspect
            logo_x = (PAGE_WIDTH - display_width) / 2
            logo_y = y_cursor - display_height
            pdf.drawImage(
                logo,
                logo_x,
                logo_y,
                width=display_width,
                height=display_height,
                mask="auto",
            )
            y_cursor = logo_y - 6 * mm
        except Exception:
            y_cursor -= 8 * mm

    pdf.setFillColor(COLOR_PRIMARY)
    pdf.setFont(FONT_NAME, 22)
    pdf.drawCentredString(PAGE_WIDTH / 2, y_cursor, "ZEXXPHISH")
    y_cursor -= 7.5 * mm

    pdf.setFillColor(COLOR_SECTION)
    pdf.setFont(FONT_NAME, 12)
    pdf.drawCentredString(PAGE_WIDTH / 2, y_cursor, "Advanced Phishing Analyzer")
    y_cursor -= 8 * mm

    pdf.setFillColor(COLOR_PRIMARY)
    pdf.setFont(FONT_NAME, 16)
    pdf.drawCentredString(PAGE_WIDTH / 2, y_cursor, "URL PHISHING ANALYSIS REPORT")
    y_cursor -= 6.5 * mm

    pdf.setFillColor(COLOR_TEXT)
    pdf.setFont(FONT_NAME, 9)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, y_cursor, "Version 1.0.0 | Developed by ZEXXF"
    )
    y_cursor -= 8 * mm

    pdf.setStrokeColor(COLOR_PRIMARY)
    pdf.setLineWidth(1.2)
    pdf.line(MARGIN, y_cursor, PAGE_WIDTH - MARGIN, y_cursor)
    y_cursor -= 8 * mm

    return y_cursor


def _draw_section_title(pdf, y_cursor, title):
    pdf.setFillColor(COLOR_SECTION)
    pdf.setFont(FONT_NAME, 12)
    pdf.drawString(MARGIN, y_cursor, title)
    y_cursor -= 3 * mm
    pdf.setStrokeColor(COLOR_SECTION)
    pdf.setLineWidth(0.8)
    pdf.line(MARGIN, y_cursor, PAGE_WIDTH - MARGIN, y_cursor)
    y_cursor -= 6.5 * mm
    return y_cursor


def _draw_summary_section(pdf, y_cursor, result):
    y_cursor = _draw_section_title(pdf, y_cursor, "Scan Summary")

    findings = result.get("findings") or []
    threat_level = str(result.get("threat_level", "UNKNOWN")).upper()
    threat_color = THREAT_COLORS.get(threat_level, COLOR_TEXT)
    risk_score = result.get("risk_score", "N/A")

    badge_width = 42 * mm
    badge_height = 10 * mm
    badge_gap = 6 * mm
    badges_top = y_cursor

    risk_badge_x = PAGE_WIDTH - MARGIN - badge_width
    threat_badge_x = risk_badge_x - badge_gap - badge_width

    _draw_rounded_box(
        pdf,
        threat_badge_x,
        badges_top - badge_height,
        badge_width,
        badge_height,
        stroke_color=threat_color,
        fill_color=threat_color,
        line_width=1.0,
        radius=5,
    )
    pdf.setFillColor(white)
    pdf.setFont(FONT_NAME, 10)
    pdf.drawCentredString(
        threat_badge_x + badge_width / 2,
        badges_top - badge_height + 3 * mm,
        f"Threat: {threat_level}",
    )

    _draw_rounded_box(
        pdf,
        risk_badge_x,
        badges_top - badge_height,
        badge_width,
        badge_height,
        stroke_color=COLOR_PRIMARY,
        fill_color=COLOR_PRIMARY,
        line_width=1.0,
        radius=5,
    )
    pdf.setFillColor(white)
    pdf.setFont(FONT_NAME, 10)
    pdf.drawCentredString(
        risk_badge_x + badge_width / 2,
        badges_top - badge_height + 3 * mm,
        f"Risk Score: {risk_score}",
    )

    pdf.setFillColor(COLOR_TEXT)
    pdf.setFont(FONT_NAME, 8)
    pdf.drawCentredString(
        threat_badge_x + badge_width / 2,
        badges_top - badge_height - 5 * mm,
        f"Indicators Found: {len(findings)}",
    )

    box_height = 32 * mm
    box_top = badges_top - badge_height - 10 * mm
    box_bottom = box_top - box_height
    _draw_rounded_box(
        pdf,
        MARGIN,
        box_bottom,
        PAGE_WIDTH - 2 * MARGIN,
        box_height,
        stroke_color=COLOR_PRIMARY,
        line_width=1.2,
    )

    inner_x = MARGIN + 8 * mm
    inner_y = box_top - 8 * mm
    line_gap = 7 * mm

    fields = [
        ("URL", str(result.get("url", "N/A"))),
        ("Domain", str(result.get("domain", "N/A"))),
        ("HTTPS", "Yes" if result.get("https") else "No"),
        (
            "Generated Timestamp",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        ),
    ]

    for label, value in fields:
        pdf.setFont(FONT_NAME, 9)
        pdf.setFillColor(COLOR_SECTION)
        pdf.drawString(inner_x, inner_y, f"{label}:")
        pdf.setFont(FONT_NAME, 9)
        pdf.setFillColor(COLOR_TEXT)
        pdf.drawString(inner_x + 40 * mm, inner_y, value)
        inner_y -= line_gap

    return box_bottom - 8 * mm


def _draw_findings_section(pdf, y_cursor, result, page_state):
    y_cursor = _draw_section_title(pdf, y_cursor, "Findings")

    findings = result.get("findings") or []
    if not findings:
        pdf.setFillColor(COLOR_TEXT)
        pdf.setFont(FONT_NAME, 9)
        pdf.drawString(MARGIN + 4 * mm, y_cursor, "No findings reported.")
        y_cursor -= 7 * mm
        return y_cursor

    pdf.setFont(FONT_NAME, 9)
    for finding in findings:
        y_cursor = _check_page_break(pdf, y_cursor, page_state)
        pdf.setFillColor(COLOR_PRIMARY)
        pdf.setFont(FONT_NAME, 14)
        pdf.drawString(MARGIN + 2 * mm, y_cursor - 1, "•")
       
        pdf.setFillColor(COLOR_TEXT)
        pdf.setFont(FONT_NAME, 9)
        pdf.drawString(MARGIN + 8 * mm, y_cursor, finding)
        y_cursor -= 6 * mm

    return y_cursor - 3 * mm


def _draw_recommendation_section(pdf, y_cursor, result, page_state):
    y_cursor = _check_page_break(pdf, y_cursor, page_state, required_space=36 * mm)
    y_cursor = _draw_section_title(pdf, y_cursor, "Recommendations")

    recommendation = str(result.get("recommendation", "No recommendation provided."))

    pdf.setFont(FONT_NAME, 9)
    max_width = PAGE_WIDTH - 2 * MARGIN - 16 * mm
    wrapped_lines = _wrap_text(pdf, recommendation, FONT_NAME, 9, max_width)

    line_height = 5.5 * mm
    box_padding = 5 * mm
    box_height = box_padding * 2 + line_height * len(wrapped_lines)
    box_top = y_cursor
    box_bottom = box_top - box_height

    _draw_rounded_box(
        pdf,
        MARGIN,
        box_bottom,
        PAGE_WIDTH - 2 * MARGIN,
        box_height,
        stroke_color=COLOR_SECTION,
        line_width=1.2,
    )

    text_y = box_top - box_padding - 4
    pdf.setFillColor(COLOR_TEXT)
    for line in wrapped_lines:
        pdf.drawString(MARGIN + 8 * mm, text_y, line)
        text_y -= line_height

    return box_bottom - 8 * mm


def _wrap_text(pdf, text, font_name, font_size, max_width):
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        candidate = f"{current_line} {word}".strip()
        if pdf.stringWidth(candidate, font_name, font_size) <= max_width:
            current_line = candidate
        else:
            if current_line:
                lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    if not lines:
        lines = [""]

    return lines


def _check_page_break(pdf, y_cursor, page_state, required_space=15 * mm):
    if y_cursor - required_space < MARGIN + 15 * mm:
        _draw_footer(pdf, page_state)
        pdf.showPage()
        page_state["page"] += 1
        _fill_background(pdf)
        _draw_page_border(pdf)
        return PAGE_HEIGHT - MARGIN
    return y_cursor


def _draw_footer(pdf, page_state):
    pdf.saveState()
    pdf.setStrokeColor(COLOR_BORDER)
    pdf.setLineWidth(0.5)
    pdf.line(MARGIN, MARGIN, PAGE_WIDTH - MARGIN, MARGIN)
    pdf.setFillColor(COLOR_TEXT)
    pdf.setFont(FONT_NAME, 8)
    pdf.drawCentredString(
        PAGE_WIDTH / 2,
        MARGIN - 6 * mm,
        "Generated by ZEXXPHISH v1.0.0 | Developed by ZEXXF",
    )
    pdf.drawRightString(
        PAGE_WIDTH - MARGIN,
        MARGIN - 6 * mm,
        f"Page {page_state['page']}",
    )
    pdf.restoreState()


def generate_pdf_report(result):
    try:
        _register_font()
        _ensure_reports_dir()

        domain = str(result.get("domain", "unknown")).replace("/", "_")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(
            REPORTS_DIR, f"ZEXXPHISH_Report_{domain}_{timestamp}.pdf"
        )

        pdf = canvas.Canvas(filename, pagesize=A4)
        _fill_background(pdf)
        _draw_page_border(pdf)

        page_state = {"page": 1}

        y_cursor = PAGE_HEIGHT - MARGIN
        y_cursor = _draw_header(pdf, y_cursor)
        y_cursor = _draw_summary_section(pdf, y_cursor, result)
        y_cursor = _draw_findings_section(pdf, y_cursor, result, page_state)
        y_cursor = _draw_recommendation_section(pdf, y_cursor, result, page_state)

        _draw_footer(pdf, page_state)
        pdf.save()

        return filename
    except FileNotFoundError as error:
        raise RuntimeError(f"Required asset missing: {error}") from error
    except Exception as error:
        raise RuntimeError(f"Failed to generate PDF report: {error}") from error