"""Generate a combined HTML report from all executed notebooks."""

import base64
import json
import struct
from pathlib import Path

_DTYPE_FMT = {
    "f8": ("d", 8), "f4": ("f", 4), "i4": ("i", 4), "i2": ("h", 2),
    "i1": ("b", 1), "u4": ("I", 4), "u2": ("H", 2), "u1": ("B", 1),
    "i8": ("q", 8), "u8": ("Q", 8),
}


def _decode_bdata(obj):
    """Recursively decode Plotly 6.x bdata binary arrays to plain lists."""
    if isinstance(obj, dict):
        if "bdata" in obj and "dtype" in obj:
            dtype = obj["dtype"]
            raw = base64.b64decode(obj["bdata"])
            if dtype in _DTYPE_FMT:
                fmt_char, size = _DTYPE_FMT[dtype]
                n = len(raw) // size
                return list(struct.unpack(f"<{n}{fmt_char}", raw))
            return obj
        return {k: _decode_bdata(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_decode_bdata(item) for item in obj]
    return obj


ROOT = Path(__file__).resolve().parent.parent
NOTEBOOKS_DIR = ROOT / "notebooks"
DOCS_DIR = ROOT / "docs"
DOCS_DIR.mkdir(parents=True, exist_ok=True)

SECTIONS = [
    ("Data Collection", [
        "01_usa_data_collection.ipynb",
        "02_india_data_collection.ipynb",
        "03_china_data_collection.ipynb",
    ]),
    ("Pay Comparisons", [
        "04_usa_pay.ipynb",
        "05_india_pay.ipynb",
        "06_china_pay.ipynb",
        "07_pay_cross_country.ipynb",
    ]),
    ("Job Volume", [
        "08_usa_volume.ipynb",
        "09_india_volume.ipynb",
        "10_china_volume.ipynb",
        "11_volume_cross_country.ipynb",
    ]),
    ("Growth Trends", [
        "12_usa_growth.ipynb",
        "13_india_growth.ipynb",
        "14_china_growth.ipynb",
        "15_growth_cross_country.ipynb",
    ]),
    ("SWE vs the World", [
        "16_swe_vs_peers_usa.ipynb",
        "17_swe_vs_peers_india.ipynb",
        "18_swe_vs_peers_china.ipynb",
        "19_swe_vs_world_summary.ipynb",
        "20_purchasing_power.ipynb",
    ]),
]


def extract_outputs(nb_path: Path) -> str:
    nb = json.loads(nb_path.read_text())
    parts = []
    for cell in nb.get("cells", []):
        if cell["cell_type"] == "markdown":
            source = "".join(cell.get("source", []))
            html_lines = []
            in_list = False
            for line in source.split("\n"):
                if line.startswith("- "):
                    if not in_list:
                        html_lines.append("<ul>")
                        in_list = True
                    html_lines.append(f"<li>{line[2:]}</li>")
                else:
                    if in_list:
                        html_lines.append("</ul>")
                        in_list = False
                    if line.startswith("### "):
                        html_lines.append(f"<h4>{line[4:]}</h4>")
                    elif line.startswith("## "):
                        html_lines.append(f"<h3>{line[3:]}</h3>")
                    elif line.startswith("# "):
                        html_lines.append(f"<h2>{line[2:]}</h2>")
                    elif line.strip():
                        html_lines.append(f"<p>{line}</p>")
            if in_list:
                html_lines.append("</ul>")
            parts.append("\n".join(html_lines))
        elif cell["cell_type"] == "code":
            for output in cell.get("outputs", []):
                if output.get("output_type") == "stream":
                    text = "".join(output.get("text", []))
                    if text.strip():
                        parts.append(f"<pre>{text}</pre>")
                elif output.get("output_type") in ("display_data", "execute_result"):
                    data = output.get("data", {})
                    if "application/vnd.plotly.v1+json" in data:
                        fig_data = _decode_bdata(data["application/vnd.plotly.v1+json"])
                        fig_json = json.dumps(fig_data)
                        div_id = f"plotly-{id(output)}"
                        parts.append(
                            f'<div id="{div_id}" style="width:100%;height:500px"></div>'
                            f"<script>Plotly.newPlot('{div_id}', {fig_json});</script>"
                        )
                    elif "text/html" in data:
                        table_html = "".join(data["text/html"])
                        parts.append(f'<div class="table-wrap">{table_html}</div>')
    return "\n".join(parts)


def build_html(sections: list) -> str:
    nav_items = "".join(
        f'<li><a href="#section-{i}">{title}</a></li>'
        for i, (title, _) in enumerate(sections)
    )
    content_blocks = []
    for i, (title, notebooks) in enumerate(sections):
        block = f'<section id="section-{i}"><h2>{title}</h2>'
        for nb_name in notebooks:
            nb_path = NOTEBOOKS_DIR / nb_name
            if not nb_path.exists():
                block += f"<p><em>{nb_name} not yet executed.</em></p>"
                continue
            block += extract_outputs(nb_path)
        block += "</section>"
        content_blocks.append(block)

    content = "\n".join(content_blocks)
    plotly_cdn = "https://cdn.plot.ly/plotly-latest.min.js"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Software Engineering Job Markets: USA, India &amp; China</title>
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>💻</text></svg>">
<script src="{plotly_cdn}"></script>
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
         max-width: 1200px; margin: 0 auto; padding: 20px; color: #333; }}
  h2 {{ border-bottom: 2px solid #4a90d9; padding-bottom: 8px; margin-top: 40px; }}
  h3 {{ color: #2c5f8a; margin-top: 30px; }}
  nav ul {{ list-style: none; padding: 0; display: flex; gap: 16px; flex-wrap: wrap; }}
  nav a {{ color: #4a90d9; text-decoration: none; }}
  nav a:hover {{ text-decoration: underline; }}
  pre {{ background: #f5f5f5; padding: 12px; border-radius: 4px; overflow-x: auto; }}
  li {{ margin: 4px 0; }}
  .table-wrap {{ overflow-x: auto; max-width: 100%; margin: 12px 0; }}
  .table-wrap table {{ border-collapse: collapse; font-size: 0.8em; }}
  .table-wrap th, .table-wrap td {{ border: 1px solid #ddd; padding: 3px 8px;
         text-align: right; white-space: nowrap; }}
  .table-wrap th {{ background: #f0f4f8; }}
</style>
</head>
<body>
<h1>Software Engineering Job Markets: USA, India &amp; China</h1>
<nav><ul>{nav_items}</ul></nav>
{content}
</body>
</html>"""


def main():
    html = build_html(SECTIONS)
    out = DOCS_DIR / "index.html"
    out.write_text(html)
    print(f"Report written to {out}")
    print(f"Size: {len(html):,} bytes")


if __name__ == "__main__":
    main()
