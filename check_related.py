import os, re

blog_dir = os.path.join(os.path.dirname(__file__), "blog")
fname = 'ai-agent-cho-fb-ban-hang.html'
fpath = os.path.join(blog_dir, fname)
content = open(fpath, encoding='utf-8').read()

# Find positions of related-articles in content
positions = []
start = 0
while True:
    idx = content.find('related-articles', start)
    if idx < 0:
        break
    positions.append(idx)
    start = idx + 1

print(f"Found 'related-articles' at {len(positions)} positions: {positions}")
for pos in positions:
    print(f"\n--- At position {pos} ---")
    print(repr(content[pos:pos+200]))
