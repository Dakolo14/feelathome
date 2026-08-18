import re, base64

with open('index.html', 'r') as f:
    content = f.read()

# ── 1. Replace bento-card-img <img> tags with CSS divs ─────────────────────
def replace_bento_img(match):
    tag = match.group(0)
    alt_m = re.search(r'alt="([^"]+)"', tag)
    label = alt_m.group(1) if alt_m else 'Image'
    return f'<div class="img-placeholder bento-card-img-ph"><span class="ph-label">{label}</span><span class="ph-dims">400 x 400px</span></div>'

content = re.sub(r'<img\s[^>]*class="bento-card-img"[^>]*/>', replace_bento_img, content)

# ── 2. Replace the main desktop KV <img> ───────────────────────────────────
content = re.sub(
    r'<img\s[^>]*class="desktop-kv"[^>]*/>',
    '<div class="img-placeholder kv-ph"><span class="ph-label">Main KV — Desktop</span><span class="ph-dims">1400 x 400px</span></div>',
    content
)

# ── 3. Replace campaign banner <img> (Groceries & Campus) ──────────────────
content = re.sub(
    r'<img\s[^>]*alt="Groceries [^"]*"[^>]*/\s*>',
    '<div class="img-placeholder banner-ph"><span class="ph-label">Groceries &amp; Lunchbox Deals</span><span class="ph-dims">1400 x 700px</span></div>',
    content
)
content = re.sub(
    r'<img\s[^>]*alt="Recreation [^"]*"[^>]*/\s*>',
    '<div class="img-placeholder banner-ph"><span class="ph-label">Recreation &amp; Campus Deals</span><span class="ph-dims">1400 x 700px</span></div>',
    content
)

# ── 4. Replace Rate Us banner ───────────────────────────────────────────────
content = re.sub(r'<source\s[^>]*srcset="[^"]*"[^>]*/>', '', content)
content = re.sub(
    r'<img\s[^>]*alt="Rate Us[^"]*"[^>]*/\s*>',
    '<div class="img-placeholder rate-us-ph"><span class="ph-label">Rate Us Banner</span><span class="ph-dims">1400 x 200px (Desktop) / 633 x 200px (Mobile)</span></div>',
    content
)

# ── 5. Strip background-image from bento large/wide/square cards ───────────
def strip_bento_bg(match):
    tag = match.group(0)
    tag = re.sub(r"background-image:\s*url\([^)]+\);\s*", '', tag)
    tag = re.sub(r"background-size:[^;]+;\s*", '', tag)
    tag = re.sub(r"background-position:[^;]+;\s*", '', tag)
    tag = re.sub(
        r'class="(bento-large-card|bento-wide-card|bento-square-card)"',
        lambda m: f'class="{m.group(1)} bento-bg-ph"',
        tag
    )
    return tag

content = re.sub(r'<a\s[^>]*class="bento-(?:large|wide|square)-card"[^>]*>', strip_bento_bg, content)

# ── 6. Inject placeholder CSS once into first <style> block ────────────────
placeholder_css = """
      /* ── Placeholder Styles ───────────────────────────────── */
      .img-placeholder {
        background-color: #f0f0f0;
        border: 2px dashed #cccccc;
        border-radius: 8px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 6px;
        width: 100%;
        box-sizing: border-box;
        text-align: center;
        padding: 12px;
      }
      .img-placeholder .ph-label {
        font-family: Helvetica, Arial, sans-serif;
        font-size: 13px;
        font-weight: 600;
        color: #555;
        display: block;
      }
      .img-placeholder .ph-dims {
        font-family: Helvetica, Arial, sans-serif;
        font-size: 11px;
        color: #999;
        display: block;
      }
      .bento-card-img-ph {
        aspect-ratio: 1 / 1;
        border-radius: 12px;
      }
      .kv-ph {
        width: 100%;
        aspect-ratio: 1400 / 400;
        min-height: 140px;
        border-radius: 12px;
      }
      .banner-ph {
        width: 100%;
        aspect-ratio: 2 / 1;
        border-radius: 12px;
      }
      .rate-us-ph {
        width: 100%;
        min-height: 80px;
        border-radius: 8px;
      }
      .bento-bg-ph {
        background-color: #f0f0f0 !important;
        border: 2px dashed #cccccc !important;
      }
"""

content = content.replace('<style>', '<style>' + placeholder_css, 1)

with open('index.html', 'w') as f:
    f.write(content)

print('Done - all placeholders now use clean CSS divs.')
