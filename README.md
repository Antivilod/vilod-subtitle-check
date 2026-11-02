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

Python 3.10+, standard library only. Initial preview 0.1.0. No installation
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
