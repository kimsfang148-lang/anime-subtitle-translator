from pathlib import Path
import re


def find_subtitle_files(directory):
    """Given a directory, return all .srt files recursively."""
    folder = Path(directory)
    if not folder.exists():
        return []

    return sorted(
        str(path)
        for path in folder.rglob("*.srt")
        if path.is_file()
    )


def detect_language(text):
    """Detect language among ja, ko, en. Returns 'auto' if unknown."""
    if text is None:
        return "auto"

    normalized = text.strip()
    if not normalized:
        return "auto"

    japanese = len(re.findall(r'[\u3040-\u30ff\u4e00-\u9fff]', normalized))
    korean = len(re.findall(r'[\uac00-\ud7af]', normalized))

    if japanese > 0 and japanese >= korean:
        return "ja"
    if korean > 0:
        return "ko"
    return "en"


def detect_language_from_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8-sig") as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(file_path, "r", encoding="cp949") as f:
            content = f.read()
    except OSError:
        return "auto"

    return detect_language(content)
