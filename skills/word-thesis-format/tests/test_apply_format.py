"""apply_format.py：页边距与 w:eastAsia。"""
import sys
from pathlib import Path

from docx import Document
from docx.oxml.ns import qn
from docx.shared import Mm

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS))

from apply_format import apply  # noqa: E402


def _rfonts(style):
    rpr = style.element.find(qn("w:rPr"))
    assert rpr is not None
    rfonts = rpr.find(qn("w:rFonts"))
    assert rfonts is not None
    return rfonts


def test_apply_sets_25mm_margins_and_east_asia():
    doc = Document()
    # 空白文档的 Normal 可能还没有 rPr。先种一个会盖住中文的主题字体。
    normal = doc.styles["Normal"]
    rpr = normal.element.get_or_add_rPr()
    seeded = rpr.find(qn("w:rFonts"))
    if seeded is None:
        seeded = rpr.makeelement(qn("w:rFonts"), {})
        rpr.append(seeded)
    seeded.set(qn("w:eastAsiaTheme"), "minorEastAsia")

    apply(doc)

    sec = doc.sections[0]
    # Word 以 twip 存长度，毫米来回换算会差 1 twip（635 EMU）。
    def near(actual, expected):
        assert abs(int(actual) - int(expected)) <= 635

    near(sec.page_width, Mm(210))
    near(sec.page_height, Mm(297))
    near(sec.top_margin, Mm(25))
    near(sec.bottom_margin, Mm(25))
    near(sec.left_margin, Mm(25))
    near(sec.right_margin, Mm(25))

    normal = _rfonts(doc.styles["Normal"])
    assert normal.get(qn("w:eastAsia")) == "宋体"
    assert normal.get(qn("w:eastAsiaTheme")) is None

    heading = _rfonts(doc.styles["Heading 1"])
    assert heading.get(qn("w:eastAsia")) == "黑体"
    assert heading.get(qn("w:eastAsiaTheme")) is None
