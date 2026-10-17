"""Check source navigation and the final PDF; produce a reviewable report."""
from pathlib import Path
import collections
import json
import re
import sys
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]
files=[ROOT/'main.tex',*sorted((ROOT/'chapters').glob('*.tex')),
       *sorted((ROOT/'appendices').glob('*.tex'))]
texts={str(p.relative_to(ROOT)):p.read_text(encoding='utf-8') for p in files}
source='\n'.join(texts.values())
labels=re.findall(r'\\label\{([^}]+)\}',source)
refs=set(re.findall(r'\\(?:ref|eqref|pageref|autoref)\{([^}]+)\}',source))
refs |= set(re.findall(r'\\hyperref\[([^]]+)\]',source))
refs |= set(re.findall(r'\\term\{[^}]+\}\{([^}]+)\}',source))
cites=set(key.strip() for block in re.findall(r'\\(?:cite|parencite|textcite)(?:\[[^]]*\])*\{([^}]+)\}',source) for key in block.split(','))
bibkeys=re.findall(r'@\w+\{([^,]+),',(ROOT/'references.bib').read_text(encoding='utf-8'))
report={
 'main_chapters':sum(len(re.findall(r'\\chapter\{',text)) for name,text in texts.items() if name.startswith('chapters')),
 'chinese_character_counts':{name:len(re.findall(r'[\u4e00-\u9fff]',text)) for name,text in texts.items()},
 'labels':len(labels),'cited_sources':len(cites),
 'missing_references':sorted(refs-set(labels)),
 'missing_citations':sorted(cites-set(bibkeys)),
 'duplicate_labels':[key for key,n in collections.Counter(labels).items() if n>1],
 'figures':len(re.findall(r'\\begin\{figure\}',source)),
 'tables':len(re.findall(r'\\begin\{(?:table|longtable)\}',source)),
 'exercise_boxes':len(re.findall(r'\\begin\{exercisebox\}',source)),
 'placeholder_hits':re.findall(r'TODO|TBD|待补充|待插入|PLACEHOLDER',source),
}
log=(ROOT/'build'/'main.log').read_text(encoding='utf-8',errors='replace')
report['latex']={
 'undefined_warning':bool(re.search(r'There were undefined references|Citation .* undefined|Reference .* undefined',log)),
 'rerun_warning':bool(re.search(r'Rerun to get cross-references|Please \(re\)run Biber',log)),
 'missing_characters':re.findall(r'Missing character:.*',log),
 'overfull_hboxes':re.findall(r'Overfull \\hbox \(([^)]+)\)',log),
 'overfull_vboxes':re.findall(r'Overfull \\vbox \(([^)]+)\)',log),
}
pdf=PdfReader(ROOT/'build'/'main.pdf')
report['pdf_pages']=len(pdf.pages)
report['named_destinations']=len(pdf.named_destinations)
destinations=set(pdf.named_destinations)
link_count=0
external_count=0
unresolved=set()
for page in pdf.pages:
 for raw in page.get('/Annots',[]):
  annotation=raw.get_object()
  if annotation.get('/Subtype')!='/Link':
   continue
  link_count+=1
  action=annotation.get('/A',{})
  if action.get('/S')=='/URI':
   external_count+=1
  target=annotation.get('/Dest') or (action.get('/D') if action.get('/S')=='/GoTo' else None)
  if isinstance(target,str) and target not in destinations:
   unresolved.add(target)
report['pdf_links']=link_count
report['external_links']=external_count
report['unresolved_named_links']=sorted(unresolved)
out=ROOT/'qa'/'book-audit.json'
out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
critical=(report['main_chapters']!=4 or report['missing_references'] or report['missing_citations'] or report['duplicate_labels'] or report['placeholder_hits'] or report['latex']['undefined_warning'] or report['latex']['missing_characters'] or report['unresolved_named_links'])
sys.exit(1 if critical else 0)
