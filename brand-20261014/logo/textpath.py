"""Shape text with HarfBuzz and return it as an SVG path (outlines, no font needed)."""
import os
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

FONTS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "fonts")
_cache = {}

def _font(name):
    if name not in _cache:
        path = os.path.join(FONTS, name)
        blob = hb.Blob.from_file_path(path)
        face = hb.Face(blob)
        _cache[name] = (hb.Font(face), TTFont(path), face.upem)
    return _cache[name]

def text_path(text, size, font="Mitr-SemiBold.ttf", tracking=0.0):
    """Return (d, width, bbox) with the baseline at y=0 and x starting at 0, in px."""
    hbfont, tt, upem = _font(font)
    buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties()
    hb.shape(hbfont, buf, {"kern": True, "liga": True})
    gs = tt.getGlyphSet(); order = tt.getGlyphOrder()
    s = size / upem
    pen = SVGPathPen(gs); bp = BoundsPen(gs)
    x = 0
    n = len(buf.glyph_infos)
    for i, (info, pos) in enumerate(zip(buf.glyph_infos, buf.glyph_positions)):
        g = order[info.codepoint]
        tp = TransformPen(pen, (s, 0, 0, -s, (x + pos.x_offset) * s, -pos.y_offset * s))
        gs[g].draw(tp)
        gs[g].draw(TransformPen(bp, (s, 0, 0, -s, (x + pos.x_offset) * s, -pos.y_offset * s)))
        x += pos.x_advance + (tracking * upem if i < n - 1 and pos.x_advance else 0)
    return pen.getCommands(), x * s, bp.bounds  # bounds: xmin, ymin, xmax, ymax (y down)
