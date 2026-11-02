"""Read-only SRT structural and timing checks. UTF-8 input only."""
import argparse
import json
import re
from pathlib import Path

VERSION = '0.1.0'
TIME = re.compile(r'^(\d{2,}):([0-5]\d):([0-5]\d),(\d{3}) --> (\d{2,}):([0-5]\d):([0-5]\d),(\d{3})$')


def milliseconds(parts):
    h,m,s,ms = map(int, parts)
    return ((h*60+m)*60+s)*1000+ms


def check(text):
    text = text.lstrip('\ufeff').replace('\r\n','\n').replace('\r','\n')
    blocks = re.split(r'\n[ \t]*\n', text.strip()) if text.strip() else []
    issues, seen, high_end, previous_start = [], set(), -1, -1
    if not blocks: issues.append({'block':0,'type':'empty_file'})
    for number, block in enumerate(blocks, 1):
        lines = block.split('\n')
        if len(lines)<2 or not lines[0].strip().isdigit():
            issues.append({'block':number,'type':'invalid_index_or_block'})
            continue
        index = int(lines[0].strip())
        if index in seen: issues.append({'block':number,'type':'duplicate_index'})
        if index != number: issues.append({'block':number,'type':'nonsequential_index'})
        seen.add(index)
        match = TIME.fullmatch(lines[1].strip())
        if not match:
            issues.append({'block':number,'type':'invalid_timestamp'})
            continue
        start, end = milliseconds(match.groups()[:4]), milliseconds(match.groups()[4:])
        if end<=start: issues.append({'block':number,'type':'nonpositive_duration'})
        if start<previous_start: issues.append({'block':number,'type':'out_of_order'})
        if start<high_end: issues.append({'block':number,'type':'overlap'})
        if not any(line.strip() for line in lines[2:]):
            issues.append({'block':number,'type':'empty_caption'})
        previous_start = start
        if end>start: high_end = max(high_end,end)
    return {'ok':not issues,'blocks':len(blocks),'issues':issues}


def main(argv=None):
    p = argparse.ArgumentParser(description='Vilod Subtitle Check - inspect SRT without modifying it')
    p.add_argument('--version', action='version', version=VERSION)
    p.add_argument('file'); a=p.parse_args(argv)
    try: result=check(Path(a.file).read_text(encoding='utf-8-sig'))
    except (ValueError,OSError): p.exit(2,'Cannot read UTF-8 subtitle file.\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 0 if result['ok'] else 1


if __name__ == '__main__': raise SystemExit(main())
