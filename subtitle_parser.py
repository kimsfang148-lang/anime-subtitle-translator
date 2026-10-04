import re


def parse_srt(content):
    """Return a list of subtitle blocks: [{index, timestamp, text}]"""
    cleaned = content.strip()
    if not cleaned:
        return []

    blocks = re.split(r'\n\s*\n', cleaned)
    subtitles = []

    for block in blocks:
        lines = block.strip().splitlines()
        if len(lines) < 3:
            continue

        index = lines[0].strip()
        timestamp = lines[1].strip()
        text = "\n".join(lines[2:]).strip()

        if not text:
            continue

        subtitles.append({
            "index": index,
            "timestamp": timestamp,
            "text": text,
        })

    return subtitles


def build_srt(subtitles):
    """Serialize subtitle blocks into SRT format."""
    if not subtitles:
        return ""

    result = []
    for block in subtitles:
        result.append(f"{block['index']}\n{block['timestamp']}\n{block['text']}")

    return "\n\n".join(result) + "\n"
