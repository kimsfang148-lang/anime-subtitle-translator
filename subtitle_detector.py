import os
import re
from pathlib import Path

def find_subtitle_files(directory="."):
    """
    자막 파일 자동 감지
    지원 형식: .srt, .ass, .ssa, .vtt, .sub
    """
    subtitle_extensions = [".srt", ".ass", ".ssa", ".vtt", ".sub"]
    found_files = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if Path(file).suffix.lower() in subtitle_extensions:
                full_path = os.path.join(root, file)
                found_files.append(full_path)
    
    return found_files

def detect_language(text):
    """
    자막의 언어 감지 (영어/일본어/한국어)
    """
    # 일본어 문자 범위
    japanese_pattern = r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]'
    # 한국어 문자 범위
    korean_pattern = r'[\uAC00-\uD7AF]'
    
    japanese_count = len(re.findall(japanese_pattern, text))
    korean_count = len(re.findall(korean_pattern, text))
    
    if japanese_count > korean_count and japanese_count > 0:
        return "ja"
    elif korean_count > 0:
        return "ko"
    else:
        return "en"

def parse_srt(content):
    """
    SRT 파일 파싱
    """
    blocks = content.strip().split('\n\n')
    subtitles = []
    
    for block in blocks:
        lines = block.strip().split('\n')
        if len(lines) >= 3:
            try:
                index = lines[0]
                timestamp = lines[1]
                text = '\n'.join(lines[2:])
                subtitles.append({
                    'index': index,
                    'timestamp': timestamp,
                    'text': text
                })
            except:
                continue
    
    return subtitles

def parse_ass(content):
    """
    ASS/SSA 파일 파싱
    """
    subtitles = []
    lines = content.split('\n')
    
    for line in lines:
        if line.startswith('Dialogue:'):
            parts = line.split(',', 9)
            if len(parts) >= 10:
                try:
                    start = parts[1].strip()
                    end = parts[2].strip()
                    text = parts[9].strip()
                    # ASS 형식 태그 제거
                    text = re.sub(r'\{[^}]*\}', '', text)
                    subtitles.append({
                        'start': start,
                        'end': end,
                        'text': text
                    })
                except:
                    continue
    
    return subtitles

def parse_vtt(content):
    """
    VTT 파일 파싱
    """
    blocks = content.strip().split('\n\n')
    subtitles = []
    
    for block in blocks:
        lines = block.strip().split('\n')
        if len(lines) >= 2:
            try:
                timestamp = lines[0]
                text = '\n'.join(lines[1:])
                subtitles.append({
                    'timestamp': timestamp,
                    'text': text
                })
            except:
                continue
    
    return subtitles

def extract_text_from_file(file_path):
    """
    자막 파일에서 모든 텍스트 추출
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            content = f.read()
    
    file_ext = Path(file_path).suffix.lower()
    
    if file_ext == '.srt':
        subtitles = parse_srt(content)
        text = ' '.join([sub['text'] for sub in subtitles])
    elif file_ext in ['.ass', '.ssa']:
        subtitles = parse_ass(content)
        text = ' '.join([sub['text'] for sub in subtitles])
    elif file_ext == '.vtt':
        subtitles = parse_vtt(content)
        text = ' '.join([sub['text'] for sub in subtitles])
    else:
        text = content
    
    return text, subtitles, file_ext
