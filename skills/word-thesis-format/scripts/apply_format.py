"""Apply the 自考毕业论文 default Word layout with python-docx.

Usage:
    python apply_format.py out.docx            # new blank doc with styles set
    python apply_format.py out.docx in.docx    # restyle an existing doc in place of styles
"""
import sys
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml.ns import qn
from docx.shared import Mm, Pt


def set_font(style_or_run, east_asia: str, latin: str = "Times New Roman",
             size: float | None = None, bold: bool | None = None):
    font = style_or_run.font
    font.name = latin
    if size is not None:
        font.size = Pt(size)
    if bold is not None:
        font.bold = bold
    rpr = style_or_run.element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = rpr.makeelement(qn("w:rFonts"), {})
        rpr.append(rfonts)
    rfonts.set(qn("w:ascii"), latin)
    rfonts.set(qn("w:hAnsi"), latin)
    rfonts.set(qn("w:eastAsia"), east_asia)
    # Theme fonts override the explicit ascii/eastAsia values when both are set.
    for theme_attr in ("w:asciiTheme", "w:hAnsiTheme", "w:eastAsiaTheme", "w:cstheme"):
        rfonts.attrib.pop(qn(theme_attr), None)


def para(style, align=None, before=0, after=0, first_line_chars=None):
    pf = style.paragraph_format
    pf.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    if align is not None:
        pf.alignment = align
    if first_line_chars:
        # 2 Chinese characters at 12pt = 24pt
        pf.first_line_indent = Pt(12 * first_line_chars)


def apply(doc: Document) -> Document:
    for sec in doc.sections:
        sec.page_width, sec.page_height = Mm(210), Mm(297)
        sec.top_margin = sec.bottom_margin = Mm(25)
        sec.left_margin = sec.right_margin = Mm(25)
        sec.header_distance = sec.footer_distance = Mm(15)
        sec.different_first_page_header_footer = True

    s = doc.styles
    normal = s["Normal"]
    set_font(normal, "宋体", size=12)
    para(normal, WD_ALIGN_PARAGRAPH.JUSTIFY, first_line_chars=2)

    # 段前/段后 1 行 ≈ 当前字号行高；这里按磅值近似
    h1 = s["Heading 1"]
    set_font(h1, "黑体", size=18, bold=True)
    para(h1, WD_ALIGN_PARAGRAPH.CENTER, before=18, after=18)
    h1.paragraph_format.first_line_indent = Pt(0)

    h2 = s["Heading 2"]
    set_font(h2, "黑体", size=15, bold=True)
    para(h2, WD_ALIGN_PARAGRAPH.LEFT, before=7.5, after=7.5)
    h2.paragraph_format.first_line_indent = Pt(0)

    h3 = s["Heading 3"]
    set_font(h3, "黑体", size=14, bold=True)
    para(h3, WD_ALIGN_PARAGRAPH.LEFT, before=7, after=7)
    h3.paragraph_format.first_line_indent = Pt(0)

    try:
        cap = s["Caption"]
    except KeyError:
        cap = s.add_style("Caption", 1)
    set_font(cap, "宋体", size=10.5, bold=False)
    para(cap, WD_ALIGN_PARAGRAPH.CENTER)
    cap.paragraph_format.first_line_indent = Pt(0)

    # Built-in Heading/Caption styles ship with a theme accent color.
    for st in (h1, h2, h3, cap):
        st.font.color.rgb = None
    return doc


def main():
    out = sys.argv[1]
    src = sys.argv[2] if len(sys.argv) > 2 else None
    doc = Document(src) if src else Document()
    apply(doc)
    doc.save(out)
    print(f"saved {out}")


if __name__ == "__main__":
    main()
