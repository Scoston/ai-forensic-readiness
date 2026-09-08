#!/usr/bin/env python3
"""Render the two Markdown review documents as printable, source-traceable PDFs."""
from __future__ import annotations

import hashlib
import html
import json
import re
import textwrap
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Preformatted, PageBreak

ROOT = Path(__file__).resolve().parents[1]
NAVY = colors.HexColor("#142C42")
TEAL = colors.HexColor("#176B73")
GRAY = colors.HexColor("#EAF0F4")


def inline(text, source):
    text = text.replace("\u2014", "-").replace("\u2013", "-").replace("\u2011", "-")
    text = html.escape(text)
    def link(match):
        label, target = match.groups()
        if not target.startswith(("https://", "http://")):
            target = "https://github.com/Scoston/ai-forensic-readiness/blob/main/" + (source.parent / target).resolve().relative_to(ROOT).as_posix()
        return f'<link href="{target}" color="#176B73">{label}</link>'
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link, text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"`([^`]+)`", r'<font name="Courier">\1</font>', text)
    return text


def render(source, output):
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="BodyAFR", fontName="Helvetica", fontSize=9.4, leading=12.5,
                              textColor=NAVY, spaceAfter=6, splitLongWords=True))
    styles.add(ParagraphStyle(name="TitleAFR", fontName="Helvetica-Bold", fontSize=23, leading=27,
                              textColor=NAVY, spaceAfter=16))
    styles.add(ParagraphStyle(name="HeadingAFR", fontName="Helvetica-Bold", fontSize=12.4, leading=16,
                              textColor=TEAL, spaceBefore=12, spaceAfter=7, keepWithNext=True))
    styles.add(ParagraphStyle(name="CellAFR", fontName="Helvetica", fontSize=8.1, leading=11,
                              textColor=NAVY, splitLongWords=True))
    styles.add(ParagraphStyle(name="CodeAFR", fontName="Courier", fontSize=7.5, leading=10,
                              backColor=GRAY, borderPadding=7, spaceBefore=4, spaceAfter=9))
    story = []
    lines = source.read_text(encoding="utf-8").splitlines()
    index = 0
    while index < len(lines):
        line = lines[index].strip()
        if not line:
            index += 1
            continue
        if line.startswith("```"):
            block = []
            index += 1
            while index < len(lines) and not lines[index].startswith("```"):
                block.extend(textwrap.wrap(lines[index], width=91, break_long_words=True, break_on_hyphens=False) or [""])
                index += 1
            story.append(Preformatted("\n".join(block), styles["CodeAFR"]))
        elif line.startswith("|"):
            rows = []
            while index < len(lines) and lines[index].strip().startswith("|"):
                row = lines[index].strip()
                if not re.fullmatch(r"[| :\-]+", row):
                    rows.append([Paragraph(inline(cell.strip(), source), styles["CellAFR"]) for cell in row.strip("|").split("|")])
                index += 1
            width = 7 * inch
            weights = [0.23, 0.36, 0.41] if len(rows[0]) == 3 else [1 / len(rows[0])] * len(rows[0])
            table = Table(rows, colWidths=[width * w for w in weights], repeatRows=1, hAlign="LEFT")
            table.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), GRAY), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                                       ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#CDD8E0")),
                                       ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                                       ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
            story.extend([table, Spacer(1, 8)])
            continue
        elif line.startswith("# "):
            story.append(Paragraph(inline(line[2:], source), styles["TitleAFR"]))
        elif line.startswith("## "):
            if source.stem == "practitioner-briefing" and line == "## How an enterprise can use it":
                story.append(PageBreak())
            story.append(Paragraph(inline(line[3:], source), styles["HeadingAFR"]))
        else:
            paragraph = [line]
            while index + 1 < len(lines) and lines[index + 1].strip() and not lines[index + 1].startswith(("#", "|", "```")) and not re.match(r"\d+\. ", lines[index + 1]):
                index += 1
                paragraph.append(lines[index].strip())
            story.append(Paragraph(inline(" ".join(paragraph), source), styles["BodyAFR"]))
        index += 1

    def page(canvas, doc):
        canvas.setStrokeColor(TEAL)
        canvas.setLineWidth(1)
        canvas.line(0.75 * inch, 10.45 * inch, 7.75 * inch, 10.45 * inch)
        canvas.setFont("Helvetica", 7.5)
        canvas.setFillColor(NAVY)
        canvas.drawString(0.75 * inch, 10.58 * inch, "AI FORENSIC READINESS  /  DISCUSSION DRAFT")
        canvas.drawString(0.75 * inch, 0.43 * inch, "September 8, 2026  |  CC BY 4.0  |  Synthetic research")
        canvas.drawRightString(7.75 * inch, 0.43 * inch, str(doc.page))

    output.parent.mkdir(exist_ok=True)
    doc = SimpleDocTemplate(str(output), pagesize=letter, rightMargin=0.75 * inch, leftMargin=0.75 * inch,
                            topMargin=0.8 * inch, bottomMargin=0.75 * inch,
                            title=source.stem, author="Dr. Stephen Coston", invariant=1)
    doc.build(story, onFirstPage=page, onLaterPages=page)


def main():
    assets = []
    for source_name, output_name in [
        ("spec/AI-Forensic-Readiness-v0.2.md", "AI_Forensic_Readiness_v0.2.pdf"),
        ("research/practitioner-briefing.md", "AI_Forensic_Readiness_Practitioner_Briefing.pdf")]:
        source, output = ROOT / source_name, ROOT / "release" / output_name
        render(source, output)
        assets.append({"source": source_name, "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                       "pdf": output.relative_to(ROOT).as_posix(), "pdf_sha256": hashlib.sha256(output.read_bytes()).hexdigest()})
        print(output.relative_to(ROOT))
    (ROOT / "release/pdf-manifest.json").write_text(json.dumps({"renderer": "reportlab 4.4.9", "assets": assets}, indent=2) + "\n")


if __name__ == "__main__":
    main()
