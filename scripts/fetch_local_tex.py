"""Fetch missing, public TeX Live packages into this project's private tree.

Does not modify the system TeX installation. Archives are data only; paths are
validated before extraction. Network access is required only for this helper.
"""
from pathlib import Path
import concurrent.futures
import io
import tarfile
import urllib.request
import sys

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / 'vendor' / 'texmf'
PACKAGES = ['setspace', 'csquotes', 'comment', 'anyfontsize', 'mwe',
            'footmisc', 'fancyvrb', 'makecell', 'hologo', 'manfnt',
            'bbding', 'apptools', 'adforn', 'bookmark', 'mathtools']

def fetch(name):
    base = 'https://mirrors.ctan.org/systems/texlive/tlnet/archive/'
    request = urllib.request.Request(base + name + '.tar.xz',
                                     headers={'User-Agent': 'DiffusionEbook/1.0'})
    with urllib.request.urlopen(request, timeout=90) as response:
        data = response.read()
    count = 0
    with tarfile.open(fileobj=io.BytesIO(data), mode='r:xz') as archive:
        for member in archive.getmembers():
            if not member.isfile():
                continue
            parts = Path(member.name).parts
            if not parts or parts[0] not in {'texmf-dist', 'tex', 'fonts', 'bibtex', 'tlpkg'}:
                continue
            relative = Path(*parts[1:]) if parts[0] == 'texmf-dist' else Path(*parts)
            destination = (TARGET / relative).resolve()
            if not destination.is_relative_to(TARGET.resolve()):
                raise ValueError('Unsafe archive path: ' + member.name)
            source = archive.extractfile(member)
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(source.read())
            count += 1
    return name, count

if __name__ == '__main__':
    TARGET.mkdir(parents=True, exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        jobs = {pool.submit(fetch, name): name for name in (sys.argv[1:] or PACKAGES)}
        for job in concurrent.futures.as_completed(jobs):
            try:
                print(*job.result(), flush=True)
            except Exception as error:
                print('FAILED', jobs[job], str(error), flush=True)
