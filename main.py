import argparse
from pathlib import Path

from subtitle_detector import detect_language_from_file, find_subtitle_files
from subtitle_parser import parse_srt, build_srt
from translator import translate_subtitle_text


def translate_file(file_path, target_lang="ko"):
    try:
        with open(file_path, "r", encoding="utf-8-sig") as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(file_path, "r", encoding="cp949") as f:
            content = f.read()

    blocks = parse_srt(content)
    if not blocks:
        raise ValueError(f"No subtitle blocks found in: {file_path}")

    src_lang = detect_language_from_file(file_path)
    if src_lang == "auto":
        src_lang = "en"

    translated_blocks = []
    for block in blocks:
        translated_text = translate_subtitle_text(block["text"], src_lang, target_lang)
        translated_blocks.append({
            "index": block["index"],
            "timestamp": block["timestamp"],
            "text": translated_text,
        })

    translated_content = build_srt(translated_blocks)

    output_path = Path(file_path)
    output_name = f"{output_path.stem}_{target_lang}{output_path.suffix}"
    output_file = output_path.with_name(output_name)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(translated_content)

    print(f"{file_path} -> {output_file}")
    print(f"source language detected: {src_lang}, target language: {target_lang}")
    return str(output_file)


def translate_directory(directory, target_lang="ko"):
    files = find_subtitle_files(directory)
    if not files:
        print(f"No .srt files found in: {directory}")
        return []

    results = []
    for file_path in files:
        results.append(translate_file(file_path, target_lang=target_lang))

    return results


def main():
    parser = argparse.ArgumentParser(description="Anime SRT subtitle translator")
    parser.add_argument("input", help="SRT file or directory containing .srt files")
    parser.add_argument("-t", "--target", default="ko", choices=["ko", "en", "ja"], help="Target language")
    args = parser.parse_args()

    input_path = Path(args.input)

    if input_path.is_dir():
        translate_directory(str(input_path), target_lang=args.target)
    elif input_path.is_file():
        translate_file(str(input_path), target_lang=args.target)
    else:
        raise FileNotFoundError(f"Input not found: {args.input}")


if __name__ == "__main__":
    main()
