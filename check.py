"""Check static routes, content constraints, and the downloadable CV."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import fitz

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
cv=fitz.open(root/'Omar-Nabail-CV.pdf')
text=' '.join(p.get_text() for p in cv)
assert 'Available for' not in text and 'preparing for B2 exam' in text
assert 'LANGUAGES' in text and 'English: C1' in text
print(f'PASS: {len(docs)} pages, all local links and anchors, one H1 per page, removed claims, updated CV.')
