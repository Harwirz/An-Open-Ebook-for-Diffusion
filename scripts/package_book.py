"""Package the ebook's LaTeX sources and private dependencies."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import json

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / '扩散模型电子书-LaTeX源码.zip'
files = [ROOT / name for name in (
    'main.tex', 'book-style.tex', 'elegantbook.cls',
    'ELEGANTBOOK-LICENSE.txt', 'references.bib', 'README.md')]
for directory in ('chapters', 'appendices', 'references', 'scripts', 'vendor'):
    files.extend(path for path in (ROOT / directory).rglob('*')
                 if path.is_file() and '__pycache__' not in path.parts)
files.extend(path for path in (ROOT / 'qa').iterdir()
             if path.is_file() and path.suffix in ('.md', '.json'))
files = sorted(set(files))
with ZipFile(TARGET, 'w', compression=ZIP_DEFLATED, compresslevel=9) as archive:
    for path in files:
        archive.write(path, path.relative_to(ROOT).as_posix())
with ZipFile(TARGET) as archive:
    bad = archive.testzip()
    if bad is not None:
        raise RuntimeError(f'Archive integrity check failed: {bad}')
    required = {'main.tex', 'book-style.tex', 'references.bib', 'README.md'}
    if not required.issubset(set(archive.namelist())):
        raise RuntimeError('An essential source is missing.')
print(json.dumps({'file': TARGET.name, 'entries': len(files),
                  'bytes': TARGET.stat().st_size}, ensure_ascii=True))
