#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Convert vocabulary.md to PDF
"""
import re
from pathlib import Path
from fpdf import FPDF


class PDF(FPDF):
    def header(self):
        self.set_font('DejaVu', 'B', 14)
        self.cell(0, 10, 'Listening Class 4 生词总结', ln=True, align='C')
        self.set_font('DejaVu', '', 9)
        self.cell(0, 6, '材料：Joining the Leisure Club + New Staff at Theatre', ln=True, align='C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('DejaVu', '', 8)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')


def parse_markdown(md_path):
    """Parse markdown into sections and tables"""
    text = Path(md_path).read_text(encoding='utf-8')
    lines = text.split('\n')

    sections = []
    current_section = {'title': '', 'level': 0, 'tables': []}
    current_table = None

    i = 0
    while i < len(lines):
        line = lines[i]

        # Headers
        if line.startswith('# '):
            if current_section.get('tables') or current_section.get('title'):
                sections.append(current_section)
            current_section = {'title': line[2:].strip(), 'level': 1, 'tables': []}
            current_table = None
        elif line.startswith('## '):
            if current_section.get('tables') or current_section.get('title'):
                sections.append(current_section)
            current_section = {'title': line[3:].strip(), 'level': 2, 'tables': []}
            current_table = None
        elif line.startswith('### '):
            if current_section.get('tables') or current_section.get('title'):
                sections.append(current_section)
            current_section = {'title': line[4:].strip(), 'level': 3, 'tables': []}
            current_table = None

        # Table rows
        elif line.startswith('|') and '---' not in line:
            cells = [c.strip() for c in line.strip('|').split('|')]
            cells = [c for c in cells if c]  # remove empty from leading/trailing
            if cells:
                if current_table is None:
                    current_table = {'headers': cells, 'rows': []}
                    current_section['tables'].append(current_table)
                else:
                    # Skip if this is the separator line
                    if not all(c.replace('-', '').replace(':', '').strip() == '' for c in cells):
                        current_table['rows'].append(cells)
        else:
            # Non-table line resets table tracking
            if line.strip() and current_table is not None:
                current_table = None

        i += 1

    if current_section.get('tables') or current_section.get('title'):
        sections.append(current_section)

    return sections


def clean_text(text):
    """Remove markdown bold markers"""
    return text.replace('**', '').strip()


def create_pdf(md_path, output_path):
    sections = parse_markdown(md_path)

    pdf = PDF()
    # Add Unicode fonts (Arial Unicode supports Chinese and IPA phonetics)
    pdf.add_font('DejaVu', '', '/Library/Fonts/Arial Unicode.ttf')
    pdf.add_font('DejaVu', 'B', '/Library/Fonts/Arial Unicode.ttf')
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    for section in sections:
        title = section['title']
        level = section['level']
        tables = section['tables']

        if not title:
            continue

        # Section title
        if level == 1:
            pdf.set_font('DejaVu', 'B', 16)
            pdf.ln(3)
            pdf.cell(0, 10, clean_text(title), ln=True)
            pdf.ln(2)
        elif level == 2:
            pdf.set_font('DejaVu', 'B', 13)
            pdf.set_fill_color(230, 240, 250)
            pdf.cell(0, 8, clean_text(title), ln=True, fill=True)
            pdf.ln(1)
        elif level == 3:
            pdf.set_font('DejaVu', 'B', 11)
            pdf.cell(0, 7, clean_text(title), ln=True)

        # Tables
        for table in tables:
            if not table['rows']:
                continue

            headers = [clean_text(h) for h in table['headers']]
            rows = [[clean_text(cell) for cell in row] for row in table['rows']]

            # Determine column widths based on number of columns and content type
            num_cols = len(headers)
            page_width = pdf.w - pdf.l_margin - pdf.r_margin

            if num_cols == 4:
                # Phrase table: 短语 | 音标 | 含义 | 例句
                col_widths = [page_width * 0.22, page_width * 0.22, page_width * 0.18, page_width * 0.38]
                font_size = 8
            elif num_cols == 5:
                # Word table: 单词 | 音标 | 词性 | 含义 | 例句
                col_widths = [page_width * 0.18, page_width * 0.20, page_width * 0.08, page_width * 0.16, page_width * 0.38]
                font_size = 8
            else:
                col_widths = [page_width / num_cols] * num_cols
                font_size = 8

            # Draw table
            pdf.set_font('DejaVu', 'B', font_size)
            pdf.set_fill_color(74, 144, 226)
            pdf.set_text_color(255, 255, 255)

            # Header row
            row_height = 6
            for j, header in enumerate(headers):
                pdf.cell(col_widths[j], row_height, header, border=1, fill=True, align='C')
            pdf.ln()

            # Data rows
            pdf.set_font('DejaVu', '', font_size)
            pdf.set_text_color(0, 0, 0)

            for row in rows:
                # Calculate required row height
                max_lines = 1
                for j, cell in enumerate(row):
                    if j < len(col_widths):
                        lines = pdf.get_string_width(cell) / col_widths[j]
                        max_lines = max(max_lines, lines)

                cell_height = max(row_height, row_height * (int(max_lines) + 1))

                x_start = pdf.get_x()
                y_start = pdf.get_y()

                for j, cell in enumerate(row):
                    if j < len(col_widths):
                        pdf.multi_cell(col_widths[j], row_height, cell, border=1, align='L')
                        pdf.set_xy(pdf.get_x() + col_widths[j], y_start)

                pdf.set_xy(x_start, y_start + cell_height)

                # Add new page if needed
                if pdf.get_y() > pdf.h - 30:
                    pdf.add_page()

            pdf.ln(2)

    pdf.output(output_path)
    print(f"PDF generated: {output_path}")


if __name__ == '__main__':
    base_dir = Path('/Users/qianduoduo/.openclaw/workspace/english-listening/listening/class-4')
    md_path = base_dir / 'vocabulary.md'
    output_path = base_dir / 'vocabulary.pdf'
    create_pdf(md_path, output_path)
