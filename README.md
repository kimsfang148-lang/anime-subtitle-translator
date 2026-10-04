# Anime Subtitle Translator

This project contains two approaches:

## 1) File-based subtitle translation
This version reads `.srt` files and translates each subtitle block while preserving timestamps.

Usage:

```bash
python main.py "D:\anime_subtitles" -t ko
```

## 2) Real-time subtitle OCR translation
This version captures the bottom portion of the screen, detects subtitle text with OCR, and translates it into Korean.

Usage:

```bash
python realtime_ocr_translator.py --lang ko
```

Optional capture region:

```bash
python realtime_ocr_translator.py --lang ko --region 100,500,900,200
```

## Install

```bash
pip install -r requirements.txt
```

## Notes
- Real-time OCR works best when the subtitle is in the lower part of the screen and the text is large and clear.
- For anime streams, the subtitle box usually appears near the bottom; tune the `--region` value if needed.
- This is an OCR-based approach, so subtitle recognition may be imperfect depending on font, size, and video quality.
