# src/reports/exporter.py
import os, csv, json, io
from typing import Dict, Any, List
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from src.config.settings import settings

class ReportExporter:
    """Exports generated reports into CSV, PDF (ReportLab), or JSON format."""

    @classmethod
    def export_csv(cls, report_data: Dict[str, Any]) -> str:
        output = io.StringIO()
        writer = csv.writer(output)
        
        writer.writerow(["SkillSprint AI — Enterprise Report"])
        writer.writerow(["Report Name", report_data.get("report_name", "Compliance Report")])
        writer.writerow(["Generated At", report_data.get("generated_at", "")])
        writer.writerow([])

        # Summary
        summary = report_data.get("summary", {})
        writer.writerow(["Metric", "Value"])
        for k, v in summary.items():
            writer.writerow([k.replace("_", " ").title(), v])
        writer.writerow([])

        # Recent Plans
        plans = report_data.get("recent_plans", [])
        if plans:
            writer.writerow(["Plan ID", "Employee", "Role", "Status", "Coverage %", "Traceability %"])
            for p in plans:
                writer.writerow([p["plan_id"], p["employee"], p["role"], p["status"], p["coverage_score"], p["traceability_score"]])

        return output.getvalue()

    @classmethod
    def export_pdf(cls, report_data: Dict[str, Any], target_path: str) -> str:
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        doc = SimpleDocTemplate(target_path, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            'RepTitle', parent=styles['Heading1'], fontSize=16, leading=20, textColor=colors.HexColor('#0f172a'), spaceAfter=8
        )
        meta_style = ParagraphStyle('RepMeta', parent=styles['Normal'], fontSize=9, textColor=colors.HexColor('#475569'))
        body_style = ParagraphStyle('RepBody', parent=styles['Normal'], fontSize=9, textColor=colors.HexColor('#1e293b'))

        elements = []
        elements.append(Paragraph(report_data.get("report_name", "SkillSprint AI Compliance Report"), title_style))
        elements.append(Paragraph(f"Generated: {report_data.get('generated_at', '')} | Platform: ApexNova Global Technologies", meta_style))
        elements.append(Spacer(1, 15))

        # Metrics Table
        summary = report_data.get("summary", {})
        table_data = [["Compliance Metric", "Value"]]
        for k, v in summary.items():
            table_data.append([k.replace("_", " ").title(), str(v)])

        t = Table(table_data, colWidths=[280, 200])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1'))
        ]))
        elements.append(t)
        elements.append(Spacer(1, 20))

        # Recent Plans
        plans = report_data.get("recent_plans", [])
        if plans:
            p_table_data = [["Plan ID", "Employee", "Role", "Status", "Coverage", "Traceability"]]
            for p in plans:
                p_table_data.append([str(p["plan_id"]), p["employee"][:18], p["role"][:18], p["status"], f"{p['coverage_score']}%", f"{p['traceability_score']}%"])
            pt = Table(p_table_data, colWidths=[50, 110, 110, 110, 50, 50])
            pt.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#334155')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1'))
            ]))
            elements.append(pt)

        doc.build(elements)
        return target_path
