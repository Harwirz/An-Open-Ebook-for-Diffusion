"""Deduplicate bibliography records by verified source identity.

Rewrites citation keys only, never prose or math. Keeps the individual source
bibliographies for provenance and produces references.bib for the final book.
"""
from pathlib import Path
import re
import json

ROOT = Path(__file__).resolve().parents[1]

def entries(source):
    for match in re.finditer(r'@\w+\s*\{([^,]+),',source):
        depth=1
        cursor=match.end()
        while cursor < len(source) and depth:
            char=source[cursor]
            if cursor==0 or source[cursor-1]!='\\':
                depth += (char=='{')-(char=='}')
            cursor+=1
        if depth:
            raise ValueError('Unbalanced bibliography: '+match.group(1))
        yield match.group(1).strip(),source[match.start():cursor]

def identity(record):
    arxiv = re.search(r'arxiv\.org/(?:abs|html|pdf)/(\d{4}\.\d{4,5})',record,re.I)
    if arxiv:
        return 'arxiv:'+arxiv.group(1)
    url = re.search(r'\burl\s*=\s*\{([^}]+)\}',record,re.I)
    if url:
        return 'url:'+url.group(1).rstrip('/').lower()
    title = re.search(r'\btitle\s*=\s*\{([^}]+)\}',record,re.I)
    if title:
        return 'title:'+re.sub(r'[^a-z0-9]','',title.group(1).lower())
    raise ValueError('Source identity missing')

rank={'r':0,'m':1,'c':2,'a':3}
all_records={}
for path in sorted((ROOT/'references').glob('*.bib')):
    all_records.update(dict(entries(path.read_text(encoding='utf-8'))))
groups={}
for key,record in all_records.items():
    groups.setdefault(identity(record),[]).append(key)
mapping={}
selected=[]
for group in groups.values():
    canonical=min(group,key=lambda key:(rank.get(key[0],9),key))
    selected.append(all_records[canonical])
    for key in group:
        mapping[key]=canonical

pattern=re.compile(r'(\\(?:cite|parencite|textcite)(?:\[[^]]*\])*\{)([^}]+)(\})')
changed=0
for path in [ROOT/'main.tex',*sorted((ROOT/'chapters').glob('*.tex')),
             *sorted((ROOT/'appendices').glob('*.tex'))]:
    source=path.read_text(encoding='utf-8')
    def replace(match):
        keys=[mapping.get(key.strip(),key.strip()) for key in match.group(2).split(',')]
        return match.group(1)+','.join(dict.fromkeys(keys))+match.group(3)
    revised=pattern.sub(replace,source)
    if source!=revised:
        path.write_text(revised,encoding='utf-8')
        changed+=1
(ROOT/'references.bib').write_text('% Consolidated verified bibliography.\n\n'+'\n\n'.join(selected)+'\n',encoding='utf-8')
(ROOT/'qa'/'citation-key-map.json').write_text(json.dumps(mapping,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'source_entries':len(all_records),'unique_entries':len(selected),'files_updated':changed}))
