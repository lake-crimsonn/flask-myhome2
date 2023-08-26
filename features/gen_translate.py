from PIL import Image, ImageDraw, ImageFont
from paddleocr import PaddleOCR, draw_ocr
import os
import numpy as np
from sklearn.cluster import DBSCAN
from translate import Translator
import textwrap3


def img_open(image):
    img = Image.open('static/img/' + image).convert('RGB')
    img.show()


def check_boxes(image, result):
    img = Image.open(image).convert('RGB')

    boxes = [temp[0] for temp in result]
    texts = [temp[1][0] for temp in result]
    scores = [temp[1][1] for temp in result]

    result_np = draw_ocr(img, boxes, texts, scores, font_path='data/webtoon/H2GTRM.TTF')
    result_np = Image.fromarray(result_np)

    # result_np.show()


def get_text(image):
    # img_open(image)
    # os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
    ocr = PaddleOCR(lang='korean')
    img_path = 'static/img/' + image
    result = ocr.ocr(img_path, cls=False)  # cls=False 텍스트 유형을 분류하지 않겠다. 제목, 본문, 목록과 같은 유형

    check_boxes(img_path, result)

    # 다루기 쉽게 다른 어레이에 담기
    # 문자박스 위치를 시작점(왼쪽 꼭지점)에서 width, height로 얼마나 떨어져 있는지로 표현
    boxes = []
    for i, r in enumerate(result):
        x1, y1 = r[0][0]  # 문자박스의 왼쪽 시작점
        x2, y2 = r[0][2]  # 문자박스의 오른쪽 하단 끝점

        width = x2 - x1
        height = y2 - y1

        text, conf = r[1]  # 문자와 확률

        boxes.append([int(x1), int(y1), int(width), int(height), text, conf, i])

    return boxes


# 박스의 중심점 찾기
def calculate_center(box):
    center_x = box[0] + box[2] / 2  # x좌표 + width / 2
    center_y = box[1] + box[3] / 2
    return np.array([center_x, center_y])


def cluster_boxes(boxes, eps):
    centers = np.array([calculate_center(box) for box in boxes])  # 박스 하나씩 중심점 찾고 넘파이 어레이에 담기
    clustering = DBSCAN(eps=eps, min_samples=1).fit(centers)  # eps는 군집되는 정도
    labels = clustering.labels_
    print('labels', labels)

    clusters = {}
    for i, label in enumerate(labels):
        if label in clusters:
            clusters[label].append(i)
        else:
            clusters[label] = [i]

    clusters = list(clusters.values())

    ocr_result = []
    for c in clusters:
        sub_result = []

        for i, box in enumerate(boxes):
            if i in c:
                sub_result.append(box)

        ocr_result.append(sub_result)

    print(ocr_result[0])
    return ocr_result


def translate_sentence(arr):
    final_result = []
    for sub_result in arr:
        x1 = sub_result[0][0]
        y1 = sub_result[0][1]
        x2 = sub_result[-1][0] + sub_result[-1][2]
        y2 = sub_result[-1][1] + sub_result[-1][3]

        w = x2 - x1
        h = y2 - y1

        text = ''

        for r in sub_result:
            text += r[4] + ' '

        text = text.strip()

        final_result.append([x1, y1, w, h, text])

    translator = Translator(from_lang='ko', to_lang='en')

    for i, r in enumerate(final_result):
        text_en = translator.translate(r[4])

        final_result[i].append(text_en)
    print('-----------------------------------')
    print(final_result)
    return final_result


def blank_bubble(image, boxes):
    img = Image.open('static/img/' + image).convert('RGB')
    result_img = img.copy()
    draw = ImageDraw.Draw(result_img)

    for box in boxes:
        x1, y1, w, h, _, _, _ = box
        x2 = x1 + w
        y2 = y1 + h

        draw.rectangle([(x1, y1), (x2, y2)], outline='white', fill='white')

    return result_img


def put_trans(result_img, final_result):
    result_img2 = result_img.copy()  # 원본은 그대로 살려주기. 다른 언어로 변경가능할 수 있도록.
    draw = ImageDraw.Draw(result_img2)

    for r in final_result:
        x1, y1, w, h, text_ko, text_en = r

        text_position = (x1, y1)

        font = ImageFont.truetype("data/webtoon/LiberationMono-Regular.ttf", 15)
        wrapped_text = textwrap3.wrap(text_en, width=w/8)

        line_height = font.getbbox('text')[1] * 7  # 어떤 텍스트를 넣어도 상관없음.

        for line in wrapped_text:
            draw.text(text_position, line, fill='black', stroke_width=1, stroke_fill="black", font=font)
            text_position = (text_position[0], text_position[1] + line_height)

    return result_img2


def generate_translate(image):
    boxes = get_text(image)
    ocr_array = cluster_boxes(boxes, 150)
    trans = translate_sentence(ocr_array)
    black_img = blank_bubble(image, boxes)
    res = put_trans(black_img, trans)
    # res.show()
    return res


if __name__ == '__main__':
    generate_translate('webtoon1.png')
