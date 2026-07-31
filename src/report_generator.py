from pathlib import Path
from html import escape
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def generate_reports(frame: pd.DataFrame, profile: dict, insights: str, output_dir: str | Path) -> dict[str, str]:
    """Generate professional HTML, Markdown, Excel, and PDF deliverables."""
    root = Path(output_dir); html_dir=root/"html"; pdf_dir=root/"pdf"; excel_dir=root/"excel"
    for directory in (html_dir,pdf_dir,excel_dir): directory.mkdir(parents=True, exist_ok=True)
    html_path = html_dir/"executive_report.html"
    html_path.write_text(f"<html><head><title>Data Report</title></head><body><h1>Executive Data Report</h1><h2>Data Quality Score: {profile['quality_score']}/100</h2><h2>Executive Summary</h2><p>{escape(insights)}</p><h2>Key KPIs</h2><pre>{escape(str(profile['shape']))}</pre><h2>Sample Records</h2>{frame.head(20).to_html(index=False)}</body></html>", encoding="utf-8")
    markdown_path = html_dir/"executive_report.md"; markdown_path.write_text(f"# Executive Data Report\n\n## Data Quality Score\n{profile['quality_score']}/100\n\n## Executive Summary\n{insights}\n", encoding="utf-8")
    excel_path=excel_dir/"data_report.xlsx"
    with pd.ExcelWriter(excel_path, engine="xlsxwriter") as writer:
        frame.to_excel(writer, sheet_name="Cleaned Data", index=False)
        pd.DataFrame([profile["shape"]]).to_excel(writer, sheet_name="KPIs", index=False)
        pd.DataFrame(profile["missing"].items(), columns=["column","missing"]).to_excel(writer, sheet_name="Quality", index=False)
    pdf_path=pdf_dir/"executive_report.pdf"; pdf=canvas.Canvas(str(pdf_path), pagesize=letter); pdf.setTitle("Executive Data Report"); text=pdf.beginText(48,750); text.setFont("Helvetica",11)
    for line in ["Executive Data Report", f"Data Quality Score: {profile['quality_score']}/100", "", *insights.splitlines()]:
        text.textLine(line[:110])
    pdf.drawText(text); pdf.save()
    return {"html": str(html_path), "markdown": str(markdown_path), "excel": str(excel_path), "pdf": str(pdf_path)}
