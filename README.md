# Vilod Subtitle Check

Read-only checker for UTF-8 SRT subtitles. Detects malformed timestamps,
nonpositive duration, overlapping cues, ordering problems, repeated or
nonsequential indices and empty captions.

## Example

`python subtitle_check.py example.srt`

Prints a JSON report with block numbers and issue types without caption text.
Exit codes: 0 = no issues, 1 = issues found, 2 = file or encoding error.
Only the basic SRT format is supported. Timestamp syntax is HH:MM:SS,mmm --> HH:MM:SS,mmm.
VTT, positioning extensions, translation quality, readability and video/audio
synchronization checks are not supported. Legitimate overlapping dialogue may
be flagged; findings require interpretation. No automatic fixes are made.

## По-русски

Проверяет структуру и таймкоды SRT. Не изменяет субтитры. Выводит номера блоков
с ошибками. Не оценивает качество перевода и совпадение с реальным видео.

## Requirements and status

Python 3.10+, standard library only. Source preview 0.2.0. No installation
of external packages is required. Linux tests passed; Windows is not yet verified.
No network calls, telemetry or accounts. Input content is not anonymized.
Review reports before sharing. No EXE or graphical interface is included.

## Testing

From this tool folder: `python -m unittest discover -v`.
On Windows use `py` instead of `python` if required.

## License

MIT. Copyright (c) 2026 Vilod. See LICENSE.

## Download and run

Use GitHub Code > Download ZIP, extract it, and run the commands above from the extracted folder. The download contains Python source, not an installer. Keep real input files and generated reports outside the repository.

## Скачать и запустить

Нажмите Code > Download ZIP, распакуйте архив и откройте терминал в папке программы. Нужен Python 3.10 или новее. Команды выше запускаются без установки сторонних библиотек. Это исходники, не EXE-установщик.

## Optional caption limits in 0.2.0

```sh
python subtitle_check.py --max-line-length 42 --max-cps 20 example.srt
```

Limits are disabled by default. Exceeding a limit adds an issue and returns exit code 1. The numbers above are examples, not a subtitle standard. Line length counts all Unicode code points, including spaces and markup. Reading speed sums trimmed caption line lengths (without line separators), divided by duration. Markup is not stripped. No caption text is printed. Nine unit tests passed on Linux.

Необязательные проверки длины строки и скорости чтения включаются флагами. Порог выбирает пользователь; это подсказки для ручной проверки, а не оценка качества перевода.
