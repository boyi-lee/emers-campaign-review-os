from pathlib import Path
import json
root=Path(__file__).resolve().parent
snapshot=json.loads((root/'data/snapshot.json').read_text())
css='\n'.join((root/'styles'/x).read_text() for x in ['tokens.css','report.css'])
js='\n'.join(p.read_text() for p in sorted((root/'src/sections').glob('*.js')))
# Escape closing tags inside data to avoid script termination.
payload=json.dumps(snapshot,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
html=(root/'src/template.html').read_text().replace('/* CSS */',css).replace('/* SNAPSHOT */',payload).replace('/* JS */',js)
(root/'dist').mkdir(exist_ok=True)
(root/'dist/index.html').write_text(html)
(root/'dist/snapshot.json').write_text(json.dumps(snapshot,ensure_ascii=False,indent=2))
(root/'dist/report.js').write_text(js)
print('Build OK',len(html),'characters')
