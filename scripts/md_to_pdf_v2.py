#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Convert vocabulary.md to PDF while preserving markdown style
using markdown -> HTML -> PDF (xhtml2pdf)
"""
from pathlib import Path
import markdown
from xhtml2pdf import pisa


def convert_md_to_pdf(md_path, output_path):
    # Read markdown
    md_text = Path(md_path).read_text(encoding='utf-8')

    # Convert markdown to HTML
    html_body = markdown.markdown(
        md_text,
        extensions=['tables', 'fenced_code', 'toc']
    )

    # Build full HTML with CSS that mimics markdown style
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <style>
        @page {{
            size: A4;
            margin: 2cm 1.5cm;
        }}
        @font-face {{
            font-family: "ArialUnicode";
            src: url("/Library/Fonts/Arial Unicode.ttf");
        }}
        body {{
            font-family: "ArialUnicode", "Arial Unicode MS", "Helvetica Neue", Arial, sans-serif;
            font-size: 10pt;
            line-height: 1.5;
            color: #333;
        }}
        h1 {{
            font-size: 18pt;
            color: #2c3e50;
            border-bottom: 2px solid #4a90e2;
            padding-bottom: 8px;
            margin-top: 20px;
        }}
        h2 {{
            font-size: 14pt;
            color: #34495e;
            margin-top: 18px;
            padding: 6px 10px;
            background-color: #ecf0f1;
            border-left: 4px solid #4a90e2;
        }}
        h3 {{
            font-size: 12pt;
            color: #4a90e2;
            margin-top: 14px;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 10px 0;
            font-size: 9pt;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 6px 8px;
            text-align: left;
            vertical-align: top;
        }}
        th {{
            background-color: #4a90e2;
            color: white;
            font-weight: bold;
        }}
        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        code {{
            background-color: #f4f4f4;
            padding: 2px 5px;
            border-radius: 3px;
            font-family: Consolas, Monaco, monospace;
            font-size: 9pt;
        }}
        strong {{
            color: #2c3e50;
        }}
        blockquote {{
            border-left: 4px solid #4a90e2;
            margin: 10px 0;
            padding: 8px 15px;
            background-color: #f8f9fa;
            color: #666;
        }}
        hr {{
            border: none;
            border-top: 1px solid #ddd;
            margin: 15px 0;
        }}
        p {{
            margin: 8px 0;
        }}
    </style>
</head>
<body>
    {html_body}
</body>
</html>"""

    # Convert HTML to PDF
    with open(output_path, 'wb') as pdf_file:
        pisa_status = pisa.CreatePDF(html, dest=pdf_file)

    if pisa_status.err:
        print(f"PDF generation completed with {pisa_status.err} errors")
    else:
        print(f"PDF generated: {output_path}")


if __name__ == '__main__':
    base_dir = Path('/Users/qianduoduo/.openclaw/workspace/english-listening/listening/class-4')
    md_path = base_dir / 'vocabulary.md'
    output_path = base_dir / 'vocabulary.pdf'
    convert_md_to_pdf(md_path, output_path)
