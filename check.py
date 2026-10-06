"""Check static routes, content constraints, and the downloadable CV."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote

root = Path(__file__).parent / 'dist'
class Document(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.links=[]; self.ids=set(); self.h1=0
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        if 'id' in attrs: self.ids.add(attrs['id'])
        if tag=='h1': self.h1+=1
        for name in ['href','src']:
            if name in attrs: self.links.append(attrs[name])

docs={p.name:Document(p.read_text(encoding='utf-8')) for p in root.glob('*.html')}
for filename,doc in docs.items():
    assert doc.h1==1, filename
    for link in doc.links:
        u=urlsplit(link)
        if u.scheme or u.netloc: continue
        target=unquote(u.path) or filename
        assert (root/target).is_file(), (filename,link)
        if u.fragment: assert u.fragment in docs[target].ids,(filename,link)
    text=(root/filename).read_text(encoding='utf-8').lower()
    assert '25%' not in text and 'availability' not in text and 'available for' not in text
index=(root/'index.html').read_text(encoding='utf-8')
all_pages=' '.join(p.read_text(encoding='utf-8') for p in root.glob('*.html'))
assert '<strong>Omar Nabail</strong>' not in index
assert 'Featured project' not in index
assert 'Master’s thesis · In progress' not in index and 'Final experimental results are pending' not in index
assert 'JUL 2026 – PRESENT' in index and 'Local RAG with Hybrid Retrieval &amp; Reranking' in index
assert 'zero-shot, few-shot, and chain-of-thought' in all_pages
assert 'What this demonstrates' not in all_pages and 'Discuss this project' not in all_pages
assert 'No quantitative throughput' not in all_pages
assert 'figures should be read within the thesis evaluation context' not in all_pages
assert index.count('class="project-tech"') == 9
assert '<ul>' not in index[index.index('<details class="more-projects"'):index.index('</details>')]
source_cv=Path(__file__).parent/'assets'/'Omar-Nabail-CV.pdf'
assert (root/'Omar-Nabail-CV.pdf').read_bytes() == source_cv.read_bytes()
print(f'PASS: {len(docs)} pages, links, headings, requested copy changes, and exact CV verified.')
