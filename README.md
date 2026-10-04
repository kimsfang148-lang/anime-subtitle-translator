# Anime Subtitle Translator

This project translates `.srt` subtitle files into Korean automatically.

## Features
- Detects subtitle language automatically (`ja`, `en`, `ko`)
- Keeps original timestamps and subtitle order
- Saves output as a new `.srt` file
- Can process one file or every `.srt` in a directory

## Install

```bash
pip install -r requirements.txt
```

## Usage

Single file:

```bash
python main.py example.srt -t ko
```

Directory:

```bash
python main.py subtitles/ -t ko
```

If you want to translate into English instead:

```bash
python main.py example.srt -t en
```

## Notes
- This uses Google Translate via `googletrans`.
- For best results, use a clean `.srt` file without broken subtitle blocks.
- Real anime subtitles may contain styling tags or special characters, so the output should still be checked before publishing.
