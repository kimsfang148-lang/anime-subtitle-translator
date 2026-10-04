import argparse
import cv2
import numpy as np
import pyautogui
from googletrans import Translator
import easyocr


class RealTimeSubtitleTranslator:
    def __init__(self, target_lang="ko", region=None):
        self.target_lang = target_lang
        self.region = region
        self.reader = easyocr.Reader(['ko', 'en', 'ja'], gpu=False)
        self.translator = Translator()

    def capture_frame(self):
        screenshot = pyautogui.screenshot()
        frame = np.array(screenshot)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        if self.region is not None:
            x, y, w, h = self.region
            frame = frame[y:y+h, x:x+w]
            return frame

        h, w, _ = frame.shape
        top = int(h * 0.7)
        left = int(w * 0.08)
        right = int(w * 0.92)
        bottom = h
        return frame[top:bottom, left:right]

    def read_subtitles(self, frame):
        try:
            raw = self.reader.readtext(frame, detail=0, paragraph=True)
        except Exception:
            raw = []

        texts = []
        for text in raw:
            text = str(text).strip()
            if not text:
                continue
            if len(text) < 2:
                continue
            if text.startswith('http') or text.startswith('www'):
                continue
            texts.append(text)
        return texts

    def translate_text(self, text):
        try:
            result = self.translator.translate(text, src='auto', dest=self.target_lang)
            return result.text
        except Exception:
            return text

    def run(self):
        cv2.namedWindow('Translated Subtitle', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Translated Subtitle', 1000, 220)

        print('실시간 자막 번역 시작. 종료하려면 q를 누르세요.')
        try:
            while True:
                frame = self.capture_frame()
                texts = self.read_subtitles(frame)

                if texts:
                    translated = []
                    for text in texts[:4]:
                        translated.append(f'{text} -> {self.translate_text(text)}')
                    text_to_show = '\n'.join(translated)
                else:
                    text_to_show = '자막 감지 중...'

                canvas = np.zeros((220, 1000, 3), dtype=np.uint8)
                cv2.putText(
                    canvas,
                    text_to_show,
                    (20, 60),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 0),
                    2,
                    cv2.LINE_AA,
                )
                cv2.imshow('Translated Subtitle', canvas)

                if cv2.waitKey(200) & 0xFF == ord('q'):
                    break
        finally:
            cv2.destroyAllWindows()


def parse_region(value):
    if value is None:
        return None
    try:
        parts = [int(p) for p in value.split(',')]
        if len(parts) != 4:
            raise ValueError
        return tuple(parts)
    except ValueError:
        raise argparse.ArgumentTypeError('영역은 x,y,w,h 형식이어야 합니다. 예: 100,500,800,200')


def main():
    parser = argparse.ArgumentParser(description='실시간 애니 자막 번역기 (OCR + 번역)')
    parser.add_argument('--lang', default='ko', choices=['ko', 'en', 'ja'], help='번역 대상 언어')
    parser.add_argument('--region', type=parse_region, help='캡처 영역: x,y,w,h 예: 100,500,800,200')
    args = parser.parse_args()

    translator = RealTimeSubtitleTranslator(target_lang=args.lang, region=args.region)
    translator.run()


if __name__ == '__main__':
    main()
