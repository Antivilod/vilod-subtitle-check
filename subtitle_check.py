"""Read-only SRT structural and timing checks. UTF-8 input only."""
import argparse
import json
import re
from pathlib import Path

VERSION = '0.3.0'
TIME = re.compile(r'^(\d{2,}):([0-5]\d):([0-5]\d),(\d{3}) --> (\d{2,}):([0-5]\d):([0-5]\d),(\d{3})$')


def milliseconds(parts):
    h,m,s,ms = map(int, parts)
    return ((h*60+m)*60+s)*1000+ms


def check(text, max_line_length=None, max_cps=None, min_duration_ms=None):
    if min_duration_ms is not None and min_duration_ms <= 0:
        raise ValueError('min_duration_ms must be positive')
    if max_line_length is not None and max_line_length <= 0:
        raise ValueError('max_line_length must be positive')
    if max_cps is not None and (not 0 < max_cps < float('inf')):
        raise ValueError('max_cps must be finite and positive')
    text = text.lstrip('\ufeff').replace('\r\n','\n').replace('\r','\n')
    blocks = re.split(r'\n[ \t]*\n', text.strip()) if text.strip() else []
    issues, seen, high_end, previous_start = [], set(), -1, -1
    if not blocks: issues.append({'block':0,'type':'empty_file'})
    for number, block in enumerate(blocks, 1):
        lines = block.split('\n')
        if len(lines)<2 or not re.fullmatch(r'[0-9]{1,9}', lines[0].strip()):
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
        if min_duration_ms is not None and 0 < end - start < min_duration_ms:
            issues.append({'block':number,'type':'duration_too_short','milliseconds':end-start})
        if start<previous_start: issues.append({'block':number,'type':'out_of_order'})
        if start<high_end: issues.append({'block':number,'type':'overlap'})
        if not any(line.strip() for line in lines[2:]):
            issues.append({'block':number,'type':'empty_caption'})
        if max_line_length is not None:
            for line_number, line in enumerate(lines[2:], 1):
                if len(line) > max_line_length:
                    issues.append({'block':number,'type':'line_too_long',
                                   'line':line_number,'characters':len(line)})
        if max_cps is not None and end > start:
            characters = sum(len(line.strip()) for line in lines[2:])
            cps = characters * 1000 / (end - start)
            if cps > max_cps:
                issues.append({'block':number,'type':'reading_speed',
                               'characters_per_second':round(cps, 2)})
        previous_start = start
        if end>start: high_end = max(high_end,end)
    return {'ok':not issues,'blocks':len(blocks),'issues':issues}


def main(argv=None):
    p = argparse.ArgumentParser(description='Vilod Subtitle Check - inspect SRT without modifying it')
    p.add_argument('--version', action='version', version=VERSION)
    p.add_argument('--max-line-length', type=int, help='Optional positive character limit per caption line')
    p.add_argument('--max-cps', type=float, help='Optional finite positive characters-per-second limit')
    p.add_argument('--min-duration-ms', type=int, help='Flag positive durations below this threshold')
    p.add_argument('file'); a=p.parse_args(argv)
    if a.max_line_length is not None and a.max_line_length <= 0:
        p.error('--max-line-length must be positive')
    if a.max_cps is not None and not 0 < a.max_cps < float('inf'):
        p.error('--max-cps must be finite and positive')
    if a.min_duration_ms is not None and a.min_duration_ms <= 0:
        p.error('--min-duration-ms must be positive')
    try: result=check(Path(a.file).read_text(encoding='utf-8-sig'), a.max_line_length, a.max_cps, a.min_duration_ms)
    except (ValueError,OSError): p.exit(2,'Cannot read UTF-8 subtitle file.\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 0 if result['ok'] else 1


if __name__ == '__main__': raise SystemExit(main())
