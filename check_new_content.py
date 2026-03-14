import os, re

blog_dir = os.path.join(os.path.dirname(__file__), "blog")

# These are files that previously had NO related section - I added one
newly_added_related = [
    '5-viec-nen-de-ai-lam.html',
    'ai-agent-hoc-business-the-nao.html',
    'ai-agent-la-gi.html',
    'ban-la-1-nguoi-ai-lam-cua-ca-team.html',
    'bao-mat-ai-agent.html',
    'bat-dau-voi-ai-agent-tu-dau.html',
    'case-study-kansai-osaka.html',
    'loi-founders-hay-mac-khi-dung-ai.html',
    'nganh-nao-phu-hop-ai-agent-viet-nam.html',
    'onboarding-ai-agent-48h.html',
    'so-sanh-nhan-vien-vs-ai.html',
    'tai-sao-chatgpt-khong-phai-nhan-vien.html',
]

# Check the newly added related sections
issues = []
for fname in newly_added_related:
    fpath = os.path.join(blog_dir, fname)
    content = open(fpath, encoding='utf-8').read()
    
    # Find all related-articles divs - we want the LAST one (the one we added)
    positions = []
    start = 0
    while True:
        idx = content.find('related-articles">', start)
        if idx < 0:
            break
        positions.append(idx)
        start = idx + 1
    
    if positions:
        last_pos = positions[-1]
        section = content[last_pos:last_pos+600]
        print(f"\n{fname}:")
        print(section)
        # Check for non-ASCII
        for ch in section:
            if ord(ch) > 127:
                issues.append(f'NON-ASCII in NEW related of {fname}: {repr(ch)}')
                break
    else:
        issues.append(f'NO related-articles found in {fname}')

print(f"\n\n=== Issues in newly-added related sections: {len(issues)} ===")
for issue in issues:
    print(' ', issue)

# Also check the JSON-LD we added - look at a specific file
print("\n\n=== Checking NEW JSON-LD in ai-agent-cho-bao-hiem-nhan-tho.html ===")
fpath = os.path.join(blog_dir, 'ai-agent-cho-bao-hiem-nhan-tho.html')
content = open(fpath, encoding='utf-8').read()
# Find all JSON-LD blocks
pat = 'application/ld+json">'
positions = []
start = 0
while True:
    idx = content.find(pat, start)
    if idx < 0:
        break
    positions.append(idx)
    start = idx + 1
print(f"Found {len(positions)} JSON-LD blocks")
for i, pos in enumerate(positions):
    block = content[pos:pos+400]
    print(f"\n--- Block {i+1} ---")
    print(block)
    # Check for non-ASCII
    for ch in block:
        if ord(ch) > 127:
            print(f"  NON-ASCII: {repr(ch)} (U+{ord(ch):04X})")
            break
