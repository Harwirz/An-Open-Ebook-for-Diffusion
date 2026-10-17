"""Assemble already-rendered pages into labeled layout review sheets."""
from pathlib import Path
from PIL import Image,ImageDraw
from pypdf import PdfReader
import argparse

ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser()
parser.add_argument('--pages',default='qa/pages')
parser.add_argument('--sheets',default='qa/sheets')
args=parser.parse_args()
pages=sorted((ROOT/args.pages).glob('page-*.png'))
expected=len(PdfReader(ROOT/'build'/'main.pdf').pages)
if len(pages)!=expected:
    raise ValueError(f'Expected {expected} rendered pages, found {len(pages)}')
target=ROOT/args.sheets
target.mkdir(parents=True,exist_ok=True)
for start in range(0,len(pages),12):
    subset=pages[start:start+12]
    width,height=600,820
    sheet=Image.new('RGB',(3*width,4*height),(226,230,230))
    draw=ImageDraw.Draw(sheet)
    for index,path in enumerate(subset):
        im=Image.open(path).convert('RGB')
        im.thumbnail((width-16,height-28))
        x=(index%3)*width+8
        y=(index//3)*height+24
        sheet.paste(im,(x,y))
        draw.text((x,y-18),f'PDF page {start+index+1}',fill=(20,40,40))
    output=target/f'pages-{start+1:03d}-{start+len(subset):03d}.png'
    sheet.save(output)
    print(output.name)
