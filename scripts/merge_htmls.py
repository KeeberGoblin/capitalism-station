#!/usr/bin/env python3
import os
import re
import sys
import hashlib
import html as htmllib
from pathlib import Path

# Regexes to extract content
RE_LI   = re.compile(r"<li\b[^>]*>(.*?)</li>", re.I | re.S)
RE_P    = re.compile(r"<p\b[^>]*>(.*?)</p>", re.I | re.S)
RE_HEAD = re.compile(r"<h[1-3]\b[^>]*>(.*?)</h[1-3]>", re.I | re.S)
RE_IMG  = re.compile(r"<img\b[^>]*\bsrc=[\"']([^\"']+)[\"'][^>]*>", re.I)
RE_TAG  = re.compile(r"<[^>]+>")

# Directories to skip when walking the repo
SKIP_DIRS = {
    ".git", ".github", ".idea", ".vscode", ".venv", "venv",
    "node_modules", "dist", "build", "out", "target", "bin", "obj", "__pycache__"
}

PLACEHOLDER_DATA_URI = (
    "data:image/png;base64,"
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGNgYAAAAAMAASsJTYQAAAAASUVORK5CYII="
)

def slugify(text: str) -> str:
    t = text.strip().lower()
    t = re.sub(r"\s+", "-", t)
    t = re.sub(r"[^a-z0-9\-_.]", "", t)
    return t

def text_from_html(fragment: str) -> str:
    t = RE_TAG.sub("", fragment)
    return htmllib.unescape(t).strip()

def discover_html_files(root: Path, output_file: Path) -> list[Path]:
    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        outdir = output_file.parent
        dirnames[:] = [d for d in dirnames if Path(dirpath, d) != outdir]
        for fn in filenames:
            if fn.lower().endswith((".html", ".htm")):
                p = Path(dirpath, fn)
                # Skip the output file itself
                try:
                    if p.resolve() == output_file.resolve():
                        continue
                except Exception:
                    pass
                files.append(p)
    return files

def index_images(root: Path):
    pngs: dict[str, list[Path]] = {}
    svgs: dict[str, list[Path]] = {}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            p = Path(dirpath, fn)
            stem = p.stem.lower()
            stem_sanit = re.sub(r"[^a-z0-9]+", "-", stem)
            if fn.lower().endswith(".png"):
                for key in {stem, stem_sanit}:
                    pngs.setdefault(key, []).append(p)
            elif fn.lower().endswith(".svg"):
                for key in {stem, stem_sanit}:
                    svgs.setdefault(key, []).append(p)
    return pngs, svgs

def sha1_of_path(p: Path) -> str:
    try:
        h = hashlib.sha1()
        with open(p, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()[:12]
    except Exception:
        # Fallback to hashing the path string
        return hashlib.sha1(str(p).encode("utf-8")).hexdigest()[:12]

def convert_svg_to_png(svg_path: Path, png_out: Path, size_px: int = 24) -> bool:
    try:
        import cairosvg
    except ImportError:
        print("Error: cairosvg is not installed. Run: pip install -r requirements.txt", file=sys.stderr)
        return False
    try:
        png_out.parent.mkdir(parents=True, exist_ok=True)
        cairosvg.svg2png(
            url=str(svg_path),
            write_to=str(png_out),
            output_width=size_px,
            output_height=size_px,
            background_color="rgba(0,0,0,0)",
        )
        return True
    except Exception as e:
        print(f"Failed to convert {svg_path} -> {png_out}: {e}", file=sys.stderr)
        return False

def resolve_repo_path(src: str, file_dir: Path) -> Path | None:
    s = src.strip()
    if s.startswith(("http://", "https://", "data:")):
        return None
    # Absolute-like path relative to repo root
    if s.startswith("/"):
        cand = (Path.cwd() / s.lstrip("/")).resolve()
        return cand if cand.exists() else None
    # Relative to the HTML file
    cand = (file_dir / s).resolve()
    if cand.exists():
        return cand
    # Try relative to repo root
    cand = (Path.cwd() / s).resolve()
    return cand if cand.exists() else None

def pick_best(paths: list[Path]) -> Path:
    # Prefer shorter, then alphabetical for stability
    return sorted(paths, key=lambda p: (len(str(p)), str(p).lower()))[0]

def extract_items_from_file(path: Path) -> list[dict]:
    html = path.read_text(encoding="utf-8", errors="ignore")
    items = []

    lis = RE_LI.findall(html)
    if lis:
        for li in lis:
            imgm = RE_IMG.search(li)
            src = imgm.group(1).strip() if imgm else None
            text = text_from_html(li)
            if text:
                items.append({"text": text, "img_src": src})
        return items

    ps = RE_P.findall(html)
    if ps:
        for pfrag in ps:
            imgm = RE_IMG.search(pfrag)
            src = imgm.group(1).strip() if imgm else None
            text = text_from_html(pfrag)
            if text:
                items.append({"text": text, "img_src": src})
        return items

    hs = RE_HEAD.findall(html)
    for h in hs:
        text = text_from_html(h)
        if text:
            items.append({"text": text, "img_src": None})
    return items

def ensure_png_for_icon(icon_path: Path, output_icons_dir: Path, size_px: int = 24) -> Path | None:
    if icon_path.suffix.lower() == ".png":
        return icon_path
    if icon_path.suffix.lower() == ".svg":
        digest = sha1_of_path(icon_path)
        out_png = output_icons_dir / f"{icon_path.stem}-{digest}-{size_px}px.png"
        if out_png.exists():
            return out_png
        ok = convert_svg_to_png(icon_path, out_png, size_px=size_px)
        return out_png if ok else None
    return None

def find_icon_for_text(text: str, png_index: dict, svg_index: dict) -> Path | None:
    slug = slugify(text)
    candidates = []
    for key in {
        slug,
        slug.replace("-", "_"),
        slug.replace("-", ""),
        slug.split("-")[0] if "-" in slug else slug,
    }:
        if key in png_index:
            candidates.extend(png_index[key])
        if key in svg_index:
            candidates.extend(svg_index[key])
    if candidates:
        return pick_best(candidates)
    return None

def build_merged_html(items: list[dict], title: str) -> str:
    css = """
    :root { color-scheme: light dark; }
    body { font-family: system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, 'Noto Sans', 'Helvetica Neue', Arial, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol', sans-serif;
           margin: 24px; line-height: 1.45; }
    h1 { font-size: 1.6rem; margin: 0 0 16px 0; }
    ul.items { list-style: none; margin: 0; padding: 0; }
    .item { display: flex; align-items: center; gap: 10px; padding: 8px 10px; border-radius: 8px; }
    .item:nth-child(odd) { background: color-mix(in oklab, Canvas 92%, CanvasText 8%); }
    .item:nth-child(even){ background: color-mix(in oklab, Canvas 96%, CanvasText 4%); }
    .icon { width: 24px; height: 24px; object-fit: contain; flex: 0 0 24px; image-rendering: -webkit-optimize-contrast; }
    .text { flex: 1; }
    .src { opacity: 0.6; font-size: 0.82rem; margin-left: auto; }
    footer { margin-top: 18px; opacity: 0.7; font-size: 0.85rem; }
    """
    parts = []
    parts.append("<!doctype html>")
    parts.append("<html lang=\"en\">")
    parts.append("<head>")
    parts.append("<meta charset=\"utf-8\">")
    parts.append("<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">")
    parts.append(f"<title>{htmllib.escape(title)}</title>")
    parts.append("<style>")
    parts.append(css)
    parts.append("</style>")
    parts.append("</head>")
    parts.append("<body>")
    parts.append(f"<h1>{htmllib.escape(title)}</h1>")
    parts.append("<ul class=\"items\">")
    for item in items:
        icon = item.get("icon_src", PLACEHOLDER_DATA_URI)
        label = htmllib.escape(item.get("text", ""))
        srcfile = htmllib.escape(item.get("source", ""))
        parts.append("<li class=\"item\">")
        parts.append(f"  <img class=\"icon\" src=\"{icon}\" alt=\"\">")
        parts.append(f"  <div class=\"text\">{label}</div>")
        parts.append(f"  <div class=\"src\">{srcfile}</div>")
        parts.append("</li>")
    parts.append("</ul>")
    parts.append("<footer>Generated by scripts/merge_htmls.py</footer>")
    parts.append("</body></html>")
    return "\n".join(parts)

def main():
    repo_root = Path.cwd()
    output_dir = repo_root / "html"
    icons_dir = output_dir / "icons"
    output_dir.mkdir(parents=True, exist_ok=True)
    icons_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "merged.html"

    html_files = discover_html_files(repo_root, output_file)
    if not html_files:
        print("No HTML files found.")
        return

    png_index, svg_index = index_images(repo_root)

    all_items = []
    for f in sorted(html_files, key=lambda p: str(p).lower()):
        file_items = extract_items_from_file(f)
        if not file_items:
            continue
        fdir = f.parent
        for it in file_items:
            text = it.get("text", "").strip()
            img_src = it.get("img_src")
            icon_path: Path | None = None

            # 1) Image from the item itself (if any)
            if img_src:
                rp = resolve_repo_path(img_src, fdir)
                if rp and rp.exists():
                    icon_path = rp

            # 2) If none, try repository match by text
            if not icon_path and text:
                icon_path = find_icon_for_text(text, png_index, svg_index)

            # Convert to PNG if necessary
            if icon_path:
                ensured = ensure_png_for_icon(icon_path, icons_dir, size_px=24)
                if ensured and ensured.exists():
                    icon_rel_for_html = os.path.relpath(ensured, start=output_dir)
                elif icon_path.suffix.lower() == ".png":
                    icon_rel_for_html = os.path.relpath(icon_path, start=output_dir)
                else:
                    icon_rel_for_html = PLACEHOLDER_DATA_URI
            else:
                icon_rel_for_html = PLACEHOLDER_DATA_URI

            all_items.append({
                "text": text if text else "(untitled)",
                "icon_src": icon_rel_for_html,
                "source": os.path.relpath(f, start=repo_root),
            })

    if not all_items:
        print("No items could be extracted from the HTML files.")
        return

    merged = build_merged_html(all_items, title="Merged List")
    output_file.write_text(merged, encoding="utf-8")
    print(f"Wrote {output_file} with {len(all_items)} items from {len(html_files)} HTML files.")

if __name__ == "__main__":
    main()