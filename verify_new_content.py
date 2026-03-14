import os, re

blog_dir = os.path.join(os.path.dirname(__file__), "blog")
files = [f for f in os.listdir(blog_dir) if f.endswith('.html') and f != 'index.html']

issues = []
clean = 0

for fname in sorted(files):
    fpath = os.path.join(blog_dir, fname)
    content = open(fpath, encoding='utf-8').read()
    
    # Find the Article JSON-LD block specifically (the one with @type Article)
    # We want blocks that contain both @type Article AND our author pattern
    pat = r'application/ld\+json">\s*\{[^}]*"@type":\s*"Article".*?\}'
    # Use a more targeted approach: find the block we added
    # Our block has: trolythongminh.io.vn as author
    
    # Find all JSON-LD script blocks
    script_pat = r'<script type="application/ld\+json">(.*?)</script>'
    for m in re.finditer(script_pat, content, re.DOTALL):
        block = m.group(1)
        if '"@type": "Article"' in block or '"@type":"Article"' in block:
            if 'trolythongminh.io.vn' in block:
                # This is our newly added Article schema
                has_non_ascii = False
                for ch in block:
                    if ord(ch) > 127:
                        issues.append(f'NON-ASCII in NEW Article JSON-LD: {fname} -- {repr(ch)}')
                        has_non_ascii = True
                        break
                if not has_non_ascii:
                    clean += 1

print(f"Clean Article JSON-LD blocks: {clean}")
print(f"Issues: {len(issues)}")
for issue in issues:
    print(' ', issue)

# Also verify the related sections we added contain only ASCII
print("\n--- Verifying related sections content ---")
# Check ALL files - the related-grid content we added
rel_issues = []
rel_clean = 0
for fname in sorted(files):
    fpath = os.path.join(blog_dir, fname)
    content = open(fpath, encoding='utf-8').read()
    
    # Find related-grid divs
    grid_pat = r'<div class="related-grid">(.*?)</div>'
    for m in re.finditer(grid_pat, content, re.DOTALL):
        grid = m.group(1)
        # Check if this grid has our ASCII pattern (no diacritics in link text)
        if 'Khac Hoan Toan' in grid or 'Bai viet lien quan' in content:
            has_non_ascii = False
            for ch in grid:
                if ord(ch) > 127:
                    rel_issues.append(f'NON-ASCII in related-grid: {fname} -- {repr(ch)}')
                    has_non_ascii = True
                    break
            if not has_non_ascii:
                rel_clean += 1

print(f"Clean related-grid blocks (ASCII): {rel_clean}")
print(f"Issues in related-grid: {len(rel_issues)}")
for issue in rel_issues[:10]:
    print(' ', issue)
