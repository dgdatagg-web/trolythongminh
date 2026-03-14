import os, re, sys

blog_dir = os.path.join(os.path.dirname(__file__), "blog")
files = [f for f in os.listdir(blog_dir) if f.endswith('.html') and f != 'index.html']

issues = []
for fname in sorted(files):
    fpath = os.path.join(blog_dir, fname)
    with open(fpath, 'rb') as f:
        raw = f.read()
    try:
        content = raw.decode('utf-8')
    except UnicodeDecodeError as e:
        issues.append(f'DECODE ERROR: {fname} -- {str(e)}')
        continue
    
    # Check for non-ASCII chars in JSON-LD section
    pat_jsonld = re.compile(r'application/ld\+json">(.*?)</script>', re.DOTALL)
    for m in pat_jsonld.finditer(content):
        text = m.group(1)
        for ch in text:
            if ord(ch) > 127:
                issues.append(f'NON-ASCII in JSON-LD: {fname} -- char={repr(ch)}')
                break
    
    # Check for non-ASCII in related-articles section
    pat_related = re.compile(r'class="related-articles">(.*?)</div>\s*\n', re.DOTALL)
    for m in pat_related.finditer(content):
        text = m.group(1)
        for ch in text:
            if ord(ch) > 127:
                issues.append(f'NON-ASCII in related: {fname} -- char={repr(ch)}')
                break

if issues:
    print('ENCODING ISSUES:')
    for issue in issues:
        print(' ', issue)
    print(f'TOTAL ISSUES: {len(issues)}')
else:
    print('ENCODING VERIFY PASS -- no issues found in JSON-LD + related sections')

total = len(files)
with_schema = 0
with_related = 0
for f in files:
    c = open(os.path.join(blog_dir, f), encoding='utf-8', errors='replace').read()
    if '"@type": "Article"' in c or '"@type":"Article"' in c:
        with_schema += 1
    if 'related-articles' in c and 'related-grid' in c:
        with_related += 1

print(f'Stats: {total} blog posts | {with_schema} with Article JSON-LD | {with_related} with related-articles')
