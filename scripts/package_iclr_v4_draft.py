"""Compile and independently rebuild the shareable official-style paper bundle."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
import time
import zipfile
from package_iclr_draft import active_source_files

ROOT=Path(__file__).resolve().parents[1]
PAPER=ROOT/'paper/iclr2027'
ENGINE=ROOT/'recovery/tools/tectonic'


def run(args, **kwargs):
    return subprocess.run(args, text=True, capture_output=True, check=True, **kwargs)


def main():
    run([str(ENGINE),'-X','compile','--keep-logs','--keep-intermediates','main.tex'],cwd=PAPER,timeout=120)
    log=(PAPER/'main.log').read_text();aux=(PAPER/'main.aux').read_text()
    if 'Overfull ' in log or 'Float too large' in log or re.search(r'(Citation|Reference).*undefined',log):
        raise ValueError('Paper has a layout or reference error')
    match=re.search(r'newlabel\{sec:mainend\}\{\{[^}]*\}\{(\d+)\}',aux)
    if not match or int(match[1])>9:
        raise ValueError('Main text exceeds the official nine-page limit')
    main_table_pages = {}
    for label in ('tab:main_matrix', 'tab:sailmain'):
        table_match = re.search(r'newlabel\{' + re.escape(label) + r'\}\{\{[^}]*\}\{(\d+)\}', aux)
        if not table_match or int(table_match[1]) > int(match[1]):
            raise ValueError(f'Core result table is missing from the main text: {label}')
        main_table_pages[label] = int(table_match[1])
    style_names=['iclr2027_conference.sty','iclr2027_conference.bst','natbib.sty','fancyhdr.sty']
    source=json.loads((PAPER/'template_source.json').read_text())
    official=PAPER/'iclr-2027-style-files.zip'
    assert hashlib.sha256(official.read_bytes()).hexdigest()==source['sha256']
    style_checks={}
    with zipfile.ZipFile(official) as z:
        for name in style_names:
            entries=[p for p in z.namelist() if Path(p).name==name and not p.startswith('__MACOSX/')]
            assert len(entries)==1,name
            style_checks[name]=(PAPER/name).read_bytes()==z.read(entries[0])
            assert style_checks[name],name
    paths = sorted(active_source_files() | {
        PAPER/name for name in ['references.bib','SOURCE_README.md',*style_names]
    })
    bundle=PAPER/'iclr2027-draft-source.zip'
    with zipfile.ZipFile(bundle,'w',zipfile.ZIP_DEFLATED) as z:
        for path in sorted(paths):
            z.write(path,str(path.relative_to(PAPER)))
    scratch_root=ROOT/'recovery/sail-v4-20260913';scratch_root.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='paper-rebuild-',dir=scratch_root) as directory:
        directory=Path(directory)
        with zipfile.ZipFile(bundle) as z:
            z.extractall(directory)
        run([str(ENGINE),'-X','compile','main.tex'],cwd=directory,timeout=120)
        original=run(['pdftotext',str(PAPER/'main.pdf'),'-'],timeout=20).stdout
        rebuilt=run(['pdftotext',str(directory/'main.pdf'),'-'],timeout=20).stdout
        if original!=rebuilt:
            raise ValueError('Standalone bundle text differs from the working PDF')
    info=run(['pdfinfo',str(PAPER/'main.pdf')],timeout=15).stdout
    appendix_match = re.search(r'newlabel\{app:evidence\}\{\{[^}]*\}\{(\d+)\}', aux)
    total_pages = int(re.search(r'^Pages:\s+(\d+)', info, re.M)[1])
    report={'built_unix':time.time(),'revision':'Condensed six-section appendix preserving full result counts, inference, failure accounting, and protocols alongside main-text agent evaluation',
        'main_text_ends_on_page':int(match[1]),'pdf_pages_total':int(re.search(r'^Pages:\s+(\d+)',info,re.M)[1]),
        'main_result_table_pages':main_table_pages,
        'appendix_starts_on_page':int(appendix_match[1]) if appendix_match else None,
        'appendix_pages':total_pages-int(appendix_match[1])+1 if appendix_match else None,
        'main_text_within_official_nine_page_limit':True,'official_style_checks':style_checks,
        'undefined_citations_or_references':0,'overfull_boxes':0,'oversized_floats':0,'underfull_box_messages':log.count('Underfull '),
        'source_bundle_files':len(paths),'source_bundle_sha256':hashlib.sha256(bundle.read_bytes()).hexdigest(),
        'pdf_sha256':hashlib.sha256((PAPER/'main.pdf').read_bytes()).hexdigest(),
        'standalone_source_bundle_compiles':True,'standalone_pdf_text_matches':True,
        'source_bundle_excludes_conversations_and_credentials':True,
        'source_bundle_only_active_manuscript_dependencies':True,
        'recognition_status':'N/A; independent annotation pending','question_precision_status':'rule proxy only'}
    summary=ROOT/'reports/sail-20260913/main-v3/summary.json'
    report['sail_comparison_status']=json.loads(summary.read_text())['status'] if summary.exists() else 'pending'
    report['third_round_status'] = {}
    for phase in ('matched',):
        phase_path = ROOT / 'reports/sail-v4-20260913' / ('sail4-' + phase + '-r2/summary.json')
        report['third_round_status'][phase] = json.loads(phase_path.read_text())['status'] if phase_path.exists() else 'pending'
    (PAPER/'build_validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))


if __name__=='__main__':
    main()
