#!/usr/bin/env python3
# Fix Article JSON-LD blocks that have non-ASCII content
# Replace headline/description with ASCII-only versions
import os, re, unicodedata

BLOG_DIR = os.path.join(os.path.dirname(__file__), "blog")

# Vietnamese diacritic -> ASCII mapping
VIET_MAP = {
    'à':'a','á':'a','â':'a','ã':'a','ä':'a','å':'a','ă':'a','ặ':'a','ắ':'a','ằ':'a','ẳ':'a','ẵ':'a','ậ':'a','ầ':'a','ẩ':'a','ẫ':'a','ấ':'a',
    'è':'e','é':'e','ê':'e','ế':'e','ề':'e','ệ':'e','ể':'e','ễ':'e',
    'ì':'i','í':'i','î':'i','ĩ':'i','ị':'i',
    'ò':'o','ó':'o','ô':'o','õ':'o','ö':'o','ợ':'o','ớ':'o','ờ':'o','ổ':'o','ỡ':'o','ộ':'o','ồ':'o','ổ':'o','ỗ':'o','ố':'o','ọ':'o','ỏ':'o','ỗ':'o',
    'ù':'u','ú':'u','û':'u','ũ':'u','ư':'u','ừ':'u','ứ':'u','ự':'u','ủ':'u','ữ':'u',
    'ỳ':'y','ý':'y','ỷ':'y','ỹ':'y','ỵ':'y',
    'đ':'d','Đ':'D',
    'À':'A','Á':'A','Â':'A','Ã':'A','Ä':'A','Å':'A','Ă':'A','Ặ':'A','Ắ':'A','Ằ':'A','Ẳ':'A','Ẵ':'A','Ậ':'A','Ầ':'A','Ấ':'A',
    'È':'E','É':'E','Ê':'E','Ế':'E','Ề':'E','Ệ':'E','Ể':'E','Ễ':'E',
    'Ì':'I','Í':'I','Î':'I','Ĩ':'I','Ị':'I',
    'Ò':'O','Ó':'O','Ô':'O','Õ':'O','Ö':'O','Ợ':'O','Ớ':'O','Ờ':'O','Ổ':'O','Ộ':'O','Ồ':'O','Ổ':'O','Ố':'O','Ọ':'O','Ỏ':'O',
    'Ù':'U','Ú':'U','Û':'U','Ũ':'U','Ư':'U','Ừ':'U','Ứ':'U','Ự':'U','Ủ':'U','Ữ':'U',
    'Ỳ':'Y','Ý':'Y','Ỷ':'Y','Ỹ':'Y','Ỵ':'Y',
    '\u2014': '--', '\u2013': '-',  # em-dash, en-dash
    '\u2019': "'", '\u2018': "'",   # curly quotes
    '\u201c': '"', '\u201d': '"',   # curly double quotes
    '\u00a0': ' ',                   # non-breaking space
    '\u00ab': '"', '\u00bb': '"',   # guillemets
    '\u2026': '...',                 # ellipsis
}

def ascii_only(text):
    result = []
    for ch in text:
        if ord(ch) <= 127:
            result.append(ch)
        elif ch in VIET_MAP:
            result.append(VIET_MAP[ch])
        else:
            # Try NFD decomposition + strip combining chars
            normalized = unicodedata.normalize('NFD', ch)
            ascii_part = ''.join(c for c in normalized if ord(c) <= 127)
            if ascii_part:
                result.append(ascii_part)
            else:
                result.append('')
    return ''.join(result)

def fix_article_jsonld(content, fname):
    # Find Article JSON-LD blocks added by us (contain trolythongminh.io.vn as author)
    script_pat = re.compile(
        r'(<script type="application/ld\+json">)(.*?)(</script>)',
        re.DOTALL
    )
    
    changed = False
    
    def fix_block(m):
        nonlocal changed
        open_tag, block, close_tag = m.group(1), m.group(2), m.group(3)
        
        # Only fix Article type blocks with our author
        if '"@type": "Article"' not in block:
            return m.group(0)
        if 'trolythongminh.io.vn' not in block:
            return m.group(0)
        
        # Check if it has non-ASCII
        has_non_ascii = any(ord(c) > 127 for c in block)
        if not has_non_ascii:
            return m.group(0)
        
        # Fix: convert all non-ASCII in the block to ASCII
        fixed_block = ascii_only(block)
        changed = True
        return open_tag + fixed_block + close_tag
    
    new_content = script_pat.sub(fix_block, content)
    return new_content, changed

files = [f for f in os.listdir(BLOG_DIR) if f.endswith('.html') and f != 'index.html']
fixed_count = 0

for fname in sorted(files):
    fpath = os.path.join(BLOG_DIR, fname)
    content = open(fpath, encoding='utf-8').read()
    new_content, changed = fix_article_jsonld(content, fname)
    if changed:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        fixed_count += 1
        print(f"Fixed: {fname}")

print(f"\nFixed {fixed_count} files")
