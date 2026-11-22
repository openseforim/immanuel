"""Build the side-by-side page for one mahberet.

Usage: py -3.13 scripts/build_page.py 2 "The Second Maḥberet" "Tamar and Beriah"

Inputs (in data/):
  mahberet-NN.he.json     from extract_hebrew.py
  mahberet-NN.en.txt      one English line for each Hebrew line; a blank line
                          between blocks; directives: @prose @saying @verse @gap
  mahberet-NN.notes.json  notes for the marks "⚠n"
Output: docs/mahberet-NN.html
The script stops if the English and Hebrew block or line counts do not agree.
"""
import html
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent


def read_english(path: Path):
    """Return a list of (kind, gap_before, [lines])."""
    blocks, kind, gap, cur = [], "prose", False, []

    def flush():
        nonlocal cur, gap
        if cur:
            blocks.append((kind, gap, cur))
            cur, gap = [], False

    for raw in path.read_text(encoding="utf-8").split("\n"):
        line = raw.strip()
        if not line:
            flush()
        elif line == "@gap":
            flush()
            gap = True
        elif line.startswith("@"):
            flush()
            kind = line[1:]
        else:
            cur.append(line)
    flush()
    return blocks


def fmt_en(text: str) -> str:
    text = html.escape(text, quote=False)
    text = re.sub(r"\[([^\]]+)\]", r'<span class="ref">[\1]</span>', text)
    text = re.sub(r"\s*⚠(\d+)", r'<a class="warn" href="#n\1" id="r\1" title="uncertain rendering">⚠\1</a>', text)
    return text


def main() -> None:
    num = int(sys.argv[1])
    title, subtitle = sys.argv[2], sys.argv[3]
    stem = f"mahberet-{num:02d}"
    he = json.loads((ROOT / "data" / f"{stem}.he.json").read_text(encoding="utf-8"))
    en = read_english(ROOT / "data" / f"{stem}.en.txt")
    notes = json.loads((ROOT / "data" / f"{stem}.notes.json").read_text(encoding="utf-8"))

    hb = he["blocks"]
    if len(hb) != len(en):
        print(f"block count: Hebrew {len(hb)}, English {len(en)}")
    bad = 0
    for i, (h, e) in enumerate(zip(hb, en)):
        if len(h) != len(e[2]):
            bad += 1
            print(f"block {i}: Hebrew {len(h)} lines, English {len(e[2])} lines: {e[2][0][:50]}")
    if bad or len(hb) != len(en):
        sys.exit("alignment errors; no page written")

    rows, line_no, saying_no = [], 0, 0
    for h, (kind, gap, e) in zip(hb, en):
        cls = f"blk {kind}" + (" gap" if gap else "")
        label = ""
        if kind == "saying":
            saying_no += 1
            label = f'<span class="sn">{saying_no}</span>'
        rows.append(f'<section class="{cls}">{label}')
        for hl, el in zip(h, e):
            line_no += 1
            rows.append(
                f'<div class="row" id="l{line_no}"><a class="ln" href="#l{line_no}">{line_no}</a>'
                f'<p class="en">{fmt_en(el)}</p>'
                f'<p class="he" lang="he" dir="rtl">{html.escape(hl, quote=False)}</p></div>'
            )
        rows.append("</section>")

    note_rows = "\n".join(
        f'<li id="n{k}"><a href="#r{k}">⚠{k}</a> <span lang="he" dir="rtl" class="he-inline">{html.escape(v["he"])}</span>'
        f' — {html.escape(v["note"], quote=False)}</li>'
        for k, v in notes.items()
    )

    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} — Immanuel of Rome, Maḥberot</title>
<link rel="stylesheet" href="style.css">
<script>var osT=localStorage.getItem('os-theme');osT&&osT!='auto'&&document.documentElement.setAttribute('data-theme',osT)</script>
<link rel="stylesheet" href="/assets/os.css">
<script src="/assets/os.js" defer></script>
</head>
<body>
<header>
<p class="crumb"><a href="index.html">Immanuel of Rome, <i>Maḥberot</i></a></p>
<h1>{html.escape(title)}</h1>
<p class="sub">{html.escape(subtitle)} · <span lang="he" dir="rtl">{html.escape(he["title"])}</span></p>
<p class="meta">{line_no} lines. One row is one rhyme unit of the Hebrew rhymed prose, or one line of verse.
References in <span class="ref">[gray brackets]</span> are the translator's identifications and are not verified.
<a class="warn" href="#notes">⚠</a> marks an uncertain rendering.
Hebrew text: <a href="https://benyehuda.org/read/36886">Project Ben-Yehuda</a>, from the edition of Dov Yarden (1957).</p>
</header>
<main>
{chr(10).join(rows)}
</main>
<footer id="notes">
<h2>Uncertain renderings</h2>
<ul class="notes">
{note_rows}
</ul>
<p><a href="index.html">Back to the project page</a></p>
</footer>
</body>
</html>
"""
    out = ROOT / "docs" / f"{stem}.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(page, encoding="utf-8")
    print(f"wrote {out}: {len(hb)} blocks, {line_no} lines, {saying_no} sayings")


if __name__ == "__main__":
    main()
